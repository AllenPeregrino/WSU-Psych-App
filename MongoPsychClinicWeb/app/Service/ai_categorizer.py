# MongoPsychClinicWeb/app/Service/ai_categorizer.py

import os
import json
from openai import OpenAI

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
    parts.append(f"Meaning of event: {getattr(s, 'meaning_of_event', '')}")

    parts.append("Thoughts (pos): " + ", ".join(_flatten_list(getattr(s, "thoughts_pos", []))))
    parts.append("Thoughts (neg): " + ", ".join(_flatten_list(getattr(s, "thoughts_neg", []))))
    parts.append("Feelings (pos): " + ", ".join(_flatten_list(getattr(s, "feelings_pos", []))))
    parts.append("Feelings (neg): " + ", ".join(_flatten_list(getattr(s, "feelings_neg", []))))
    parts.append("Behaviors: " + ", ".join(_flatten_list(getattr(s, "behaviors_mc", []))))

    return "\n".join(parts)


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

    system_msg = (
        "You help categorize therapy diary entries into short situation categories. "
        "Existing categories are short 'If … then …' labels. "
        "Pick the best existing label if it clearly fits; otherwise propose a concise new label. "
        "Return ONLY JSON, no extra text."
    )

    user_msg = (
        "Here is a summary of the user's situation:\n\n"
        f"{_survey_summary(current_survey)}\n\n"
        "Existing category labels (may be '(none)'):\n"
        f"{labels_str}\n\n"
        "Decide on a category for this situation.\n\n"
        "Rules:\n"
        "- If one of the existing labels fits well, use it as best_label.\n"
        "- You may include up to 2 other_labels that also somewhat fit.\n"
        "- If no existing labels fit, set best_label to null and create a new_label.\n"
        "- new_label should be a short 'If … then …' style phrase, describing situation + reaction.\n\n"
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
    except Exception as e:
        print("[AI ERROR in ai_categorizer]:", e)
        # On any error, just fall back to a synthetic label
        best_label, other_labels, new_label = None, [], None

    # ---- Fallback: if model didn't give us a new label and no existing label fits ----
    if not best_label and not new_label:
        what = getattr(current_survey, "what_happened", "") or "this situation"
        valence = getattr(current_survey, "situation", "") or "this situation"
        # Keep it reasonably short
        what_short = (what[:80] + "…") if len(what) > 80 else what
        new_label = f"If {what_short}, then I feel {valence.lower()}."

    # Map labels back to Signature IDs
    best_signature_id = id_for_label.get(best_label) if best_label else None
    other_sig_ids = [id_for_label[lbl] for lbl in other_labels if lbl in id_for_label]

    # If best_signature_id is None, we will use new_label to create a new Signature later.
    return best_signature_id, other_sig_ids[:k], new_label
