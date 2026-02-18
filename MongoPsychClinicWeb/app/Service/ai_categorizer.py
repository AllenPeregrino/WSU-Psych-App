# MongoPsychClinicWeb/app/Service/ai_categorizer.py

import os
import json
from openai import OpenAI
from collections import defaultdict
from app.Model.models import AICategoryFeedback

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _flatten_list(v):
    """Convert None / scalar / list into a flat list of strings."""
    if not v:
        return []
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    return [str(v)]


def _survey_summary(s):
    """Build a compact text summary of the survey for the model."""
    parts = []
    parts.append(f"Valence: {getattr(s, 'situation', '')}")
    parts.append(f"What happened: {getattr(s, 'what_happened', '')}")
    parts.append(f"Meaning of event: {getattr(s, 'thoughts_meaning_of_event', '')}")

    parts.append("Thoughts (pos): " + ", ".join(_flatten_list(getattr(s, "thoughts_pos", []))))
    parts.append("Thoughts (neg): " + ", ".join(_flatten_list(getattr(s, "thoughts_neg", []))))
    parts.append("Feelings (pos): " + ", ".join(_flatten_list(getattr(s, "feelings_pos", []))))
    parts.append("Feelings (neg): " + ", ".join(_flatten_list(getattr(s, "feelings_neg", []))))
    parts.append("Behaviors: " + ", ".join(_flatten_list(getattr(s, "behaviors_mc", []))))

    return "\n".join(parts)

def _feedback_stats_for_user(user, max_items=200):
    """
    Returns:
      accept_rate[label] = float in [0,1]
      corrections[label] = dict(correct_label -> count)
    """
    accept = defaultdict(int)
    reject = defaultdict(int)
    corrections = defaultdict(lambda: defaultdict(int))

    if not user:
        return {}, {}

    qs = AICategoryFeedback.objects(user=user).order_by("-created_at")[:max_items]
    for fb in qs:
        suggested = (fb.suggested_label or "").strip()
        chosen = (fb.chosen_label or "").strip()

        if not suggested:
            continue

        if fb.was_accepted:
            accept[suggested] += 1
        else:
            reject[suggested] += 1
            if chosen:
                corrections[suggested][chosen] += 1

    accept_rate = {}
    for lbl in set(list(accept.keys()) + list(reject.keys())):
        a = accept[lbl]
        r = reject[lbl]
        accept_rate[lbl] = a / (a + r) if (a + r) > 0 else 0.0

    return accept_rate, corrections


def suggest_category_and_matches(current_survey, user_signatures, prior_surveys_for_user, k=3):
    """
    Return (best_signature_id, other_signature_ids, new_label_string_or_None).

    - If there are existing Signature labels, the model can choose one of them.
    - If none fit (or there are no signatures at all), the model proposes a new label.
    - If JSON parsing fails or the model gives nothing useful, we synthesize a fallback label
      so ai_new_label is NEVER None.
    """
    # Map signature labels -> ids
    signature_labels = []
    id_for_label = {}

    for sig in user_signatures:
        label = getattr(sig, "ifThen", "").strip()
        if not label:
            continue
        signature_labels.append(label)
        id_for_label[label] = str(sig.id)

    labels_str = "\n".join(f"- {lbl}" for lbl in signature_labels) if signature_labels else "(none)"

    # ---- feedback memory (lightweight "learning") ----
    accept_rate, corrections = _feedback_stats_for_user(getattr(current_survey, "user", None))

    feedback_lines = []
    if accept_rate:
        feedback_lines.append("User feedback on past AI suggestions (higher is better):")
        # show top 8 most-seen labels
        # (we sort by number of observations = accept+reject)
        # compute obs counts properly:
        # (use corrections+accept_rate approximate is fine, but let's do it cleanly)
        # We'll rebuild from stored feedback docs quickly:
        # NOTE: to keep it simple, show accept_rate only
        for lbl, rate in sorted(accept_rate.items(), key=lambda x: x[1], reverse=True)[:8]:
            feedback_lines.append(f"- {lbl}: accept_rate={rate:.2f}")

    # Show some common corrections (if any)
    corr_lines = []
    for suggested_lbl, to_map in corrections.items():
        if not to_map:
            continue
        top_to = sorted(to_map.items(), key=lambda x: x[1], reverse=True)[:2]
        for correct_lbl, ct in top_to:
            corr_lines.append(f"- If '{suggested_lbl}' is rejected, user often chooses '{correct_lbl}' ({ct}x).")

    feedback_str = ""
    if feedback_lines or corr_lines:
        feedback_str = "\n".join(feedback_lines + ([""] if feedback_lines and corr_lines else []) + corr_lines)
    else:
        feedback_str = "(no feedback yet)"


    system_msg = (
    "You help categorize therapy diary entries into short situation category names. "
    "Category names should be concise topic-style phrases (noun phrases). "
    "Even if existing categories use 'If…then…', DO NOT generate new categories in that format. "
    "Return ONLY JSON, no extra text."
    )

    user_msg = (
        "Here is a summary of the user's situation:\n\n"
        f"{_survey_summary(current_survey)}\n\n"
        "Existing category labels (may be '(none)'):\n"
        f"{labels_str}\n\n"
        "Feedback memory (use this to bias your choice toward labels the user accepts):\n"
        f"{feedback_str}\n\n"
        "Decide on a category for this situation.\n\n"
        "Rules:\n"
        "- If one of the existing labels fits well, use it as best_label.\n"
        "- You may include up to 2 other_labels that also somewhat fit.\n"
        "- If no existing labels fit, set best_label to null and create a new_label.\n"
        "- new_label MUST be a short topic-style category name (3–8 words).\n"
        "- new_label MUST NOT include 'If' or 'then'.\n"
        "- new_label should describe what the situation is about (theme/topic), not a full sentence.\n"
        "- Good examples: 'Possible rejection by others', 'Repairing a damaged relationship', 'Pressure to perform well'.\n"
        "- Bad examples: 'If someone criticizes me then I feel hurt', 'When X then Y'.\n\n"
        "Return ONLY a JSON object with this exact shape:\n"
        "{\n"
        '  "best_label": string or null,\n'
        '  "other_labels": [string, ...],\n'
        '  "new_label": string or null\n'
        "}\n"
    )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
        )
        raw = resp.choices[0].message.content
        # Try to extract JSON safely
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # If the model wrapped JSON in ```json ``` fences, strip them
            if "```" in raw:
                raw_stripped = raw.replace("```json", "").replace("```", "").strip()
                data = json.loads(raw_stripped)
            else:
                # If it's just a bare label, treat it as new_label
                data = {"best_label": None, "other_labels": [], "new_label": raw.strip()}

        best_label = data.get("best_label")
        other_labels = data.get("other_labels") or []
        new_label = data.get("new_label")
        if isinstance(other_labels, str):
            other_labels = [other_labels]
        elif not isinstance(other_labels, list):
            other_labels = []

    except Exception as e:
        print("[AI ERROR in ai_categorizer]:", e)
        # On any error, just fall back to a synthetic label
        best_label, other_labels, new_label = None, [], None

    # ---- Fallback: if model didn't give us a new label and no existing label fits ----
    if not best_label and not new_label:
        what = getattr(current_survey, "what_happened", "") or "General situation"
        what_short = str(what).strip().rstrip(".!?")
        new_label = what_short[:60] if what_short else "General situation"



    # Map labels back to Signature IDs
    best_signature_id = id_for_label.get(best_label) if best_label else None
    other_sig_ids = [id_for_label[lbl] for lbl in other_labels if lbl in id_for_label]

    # If best_signature_id is None, we will use new_label to create a new Signature later.
    return best_signature_id, other_sig_ids[:k], new_label, best_label
