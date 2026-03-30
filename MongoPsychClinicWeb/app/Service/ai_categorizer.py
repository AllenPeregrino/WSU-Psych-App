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
    parts.append("Behavior choices: " + ", ".join(_flatten_list(getattr(s, "behaviors_mc", []))))
    parts.append(f"Behavior description: {getattr(s, 'behaviors_description', '')}")
    parts.append(f"Behavior goals/outcome: {getattr(s, 'behaviors_outcome', '')}")

    # Add selected personality components if present
    try:
        comps = getattr(s, "personality_components", []) or []
        comp_names = []
        for comp in comps:
            if hasattr(comp, "name") and comp.name:
                comp_names.append(comp.name)
        if comp_names:
            parts.append("Relevant personality components: " + ", ".join(comp_names))
    except Exception:
        pass

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


    system_msg = """
    You help categorize therapy diary entries into short situation category names.

    Categories should reflect recurring psychological/interpersonal patterns based on:
    - core appraisal or meaning of the event
    - dominant feelings
    - behavioral tendencies or goals

    Create category names that are:
    - concise topic-style phrases
    - psychologically meaningful
    - similar in style to examples like:
        - Fear of disappointing others
        - Feeling excluded by others
        - Pressure to perform well
        - Repairing a damaged relationship
        - Relief after uncertainty
        - Feeling valued and connected
        - Curiosity and exploration

    Do not force entries into a rigid predefined taxonomy.
    Instead, infer the best-fitting recurring pattern and name it at a similar level of abstraction.

    Example:

    Situation summary:
    A friend canceled plans and I felt like they didn’t want to spend time with me.
    Feelings: sad, worried
    Behavior: withdrew from texting

    Good category label:
    Feeling excluded by others

    Situation summary:
    My supervisor pointed out mistakes in my work.
    Feelings: embarrassed, anxious
    Behavior: apologized repeatedly

    Good category label:
    Fear of looking incompetent

    Avoid:
    - full sentences
    - "If ... then ..." phrasing
    - labels that are too vague like "bad situation"
    - labels that are too specific to only one event
    - overly clinical jargon
    Return ONLY JSON, no extra text.
    """

    example_block = """
    Here are examples of good categorization decisions.

    Each Line is formatted as: 
    Valence,WhatHappened,ThoughtsText,ThoughtsChecked,FeelingsChecked,BehaviorText,GoalsChecked,Category

    Negative,"A friend canceled dinner plans at the last minute.","They probably didn’t really want to spend time with me.","They don't like me. I am not wanted. I have been rejected.|I have been disappointed. I’ve done something wrong.","Unhappy, sad, depressed|Disappointed by others, let down","I stopped texting and decided not to reschedule.","To get away from something that I didn’t like","Rejection"

    Negative,"I was excluded from a social event.","I must not matter very much to them.","They don't like me. I am not wanted. I have been rejected.|I’ve lost something important to me.","Unhappy, sad, depressed|Disappointed by others, let down","I stayed home and avoided reaching out to anyone.","To get away from something that I didn’t like","Rejection"

    Negative,"My supervisor pointed out several errors in a report I submitted.","I should have caught those mistakes and I probably looked incompetent.","They are right to be judgmental/critical of my minor actions/behaviors. They see that I have done something really wrong.|I look inadequate. I am being awkward. I look foolish to others.","Shame, humiliated|Disappointed in myself, regretful|Nervous, anxious, tense","I apologized repeatedly and avoided eye contact during the meeting.","To meet someone else's expectations, not make them angry or disappoint them|To make up for harm I've caused","Shame"

    Negative,"My partner criticized how I handled a family issue.","Maybe I really do mess things up more than I realize.","They are right to be judgmental/critical of my minor actions/behaviors. They see that I have done something really wrong.|I look inadequate. I am being awkward. I look foolish to others.","Shame, humiliated|Disappointed in myself, regretful","I withdrew and stopped talking for the rest of the evening.","To get away from something that I didn’t like","Shame"

    Negative,"A coworker interrupted me repeatedly during a meeting.","They don’t respect me and what I have to say.","This was unfair. Someone else is to blame for this bad situation.|They don't like me. I am not wanted.","Mad, angry, pissed off|Annoyed, resentful, irritated","I became curt and stopped contributing to the discussion.","To correct something that someone else did that was unfair, not right","Anger"

    Negative,"I argued with my sibling over a family issue.","We will never see eye to eye on anything.","This will never get any better.|This was unfair. Someone else is to blame for this bad situation.","Mad, angry, pissed off|Frustrated, exasperated","I stopped responding to messages and disengaged.","To correct something that someone else did that was unfair, not right","Anger"

    Negative,"I received a lower grade than I expected on an exam.","I was hoping for better and this shows I’m not doing well enough.","I was hoping for better. That was not what I wanted.|I don’t see how this bad situation will ever improve.","Unhappy, sad, depressed|Resigned, defeated","I avoided reviewing the feedback and procrastinated studying.","To get away from something that I didn’t like","Hopelessness"

    Negative,"I skipped my planned workout.","I have no discipline and this will never improve.","This will never get any better.|I don’t see how this bad situation will ever improve.","Disappointed in myself, regretful|Resigned, defeated","I stayed on the couch scrolling on my phone.","To get away from something that I didn’t like","Hopelessness"

    Negative,"I got stuck in traffic and arrived late to a meeting.","This always happens to me and I can’t get anything right.","This will never get any better.|I don’t see how to handle what is happening or about to happen. I might not be able to deal with it. Something bad might happen.","Frustrated, exasperated|Nervous, anxious, tense","I rushed in flustered and barely spoke during the meeting.","To meet someone else's expectations, not make them angry or disappoint them","Anxiety"

    Negative,"My internet went down during an online presentation.","This is a disaster and I won’t recover from it.","I don’t see how to handle what is happening or about to happen. I might not be able to deal with it. Something bad might happen.","Nervous, anxious, tense|Frustrated, exasperated","I apologized repeatedly and ended the presentation early.","To get support, help/assistance from others","Anxiety"

    Negative,"A colleague received recognition that I wanted.","I should have been acknowledged instead.","I was hoping for better. That was not what I wanted.|This was unfair. Someone else is to blame for this bad situation.","Annoyed, resentful, irritated|Disappointed by others, let down","I congratulated them briefly but avoided further conversation.","To correct something that someone else did that was unfair, not right","Performance"

    Negative,"A coworker received recognition I hoped for.","I should have been acknowledged instead.","I was hoping for better. That was not what I wanted.|This was unfair. Someone else is to blame for this bad situation.","Annoyed, resentful, irritated|Disappointed by others, let down","I congratulated them but avoided further interaction.","To correct something that someone else did that was unfair, not right","Performance"

    Positive,"I completed a challenging task successfully.","I handled that well and deserve credit.","I had a role in things turning out well.|I got what I wanted. This is good. This is great.","Pleased, proud, triumphant|Relieved","I shared the success with colleagues.","To accomplish something|To connect, feel closer to someone","Mastery"

    Positive,"I solved a complex problem.","I figured it out through effort.","With some effort, I can make things better in this situation.|I deserve some credit for what I’ve done.","Eager, determined|Pleased, proud, triumphant","I documented what I learned.","To understand, learn, figure something out|To accomplish something","Mastery"

    Positive,"A friend expressed appreciation for my help.","My support really mattered.","My support is needed. I can be helpful here.|I am accepted. They appreciate me for who I am.","Appreciative, thankful, grateful|Affection, close, love","I thanked them warmly.","To connect, feel closer to someone","Connection"

    Positive,"I reconnected with an old friend.","This connection still matters.","This situation is meaningful to me.|I am accepted. They appreciate me for who I am.","Affection, close, love|Lighthearted, happy, joyful","I scheduled another meeting.","To connect, feel closer to someone","Connection"

    Positive,"My child achieved something important.","They are growing and doing well.","Things are going to be fine.|I had a role in things turning out well.","Pleased, proud, triumphant|Hopeful, optimistic","I celebrated with them.","To connect, feel closer to someone","Relief"

    Positive,"I had a relaxing evening.","This is exactly what I needed.","I got what I wanted. This is good.|I was enjoying it.","Calm, tranquil, serene|Pleasurable, enjoyment, fun","I avoided checking work email.","To be in the moment, be appreciative","Relief"

    Positive,"I enjoyed a peaceful walk outdoors.","This moment feels meaningful and calming.","This situation is meaningful to me.|I was enjoying it. I am having a good time. This is fun.","Calm, tranquil, serene|Pleasurable, enjoyment, fun","I slowed down and stayed present.","To be in the moment, be appreciative","Curiosity"

    Positive,"I had an engaging discussion.","This is interesting and meaningful.","This is interesting, engaging.|This situation is meaningful to me.","Interested, involved, intrigued|Excited, stimulated, passionate","I stayed in the conversation longer.","To further explore, make sense of, or try to understand something better","Curiosity"
    
"""

    user_msg = (
        "Here is a summary of the user's situation:\n\n"
        f"{_survey_summary(current_survey)}\n\n"
        "Existing category labels (may be '(none)'):\n"
        f"{labels_str}\n\n"
        "Feedback memory (use this to bias your choice toward labels the user accepts):\n"
        f"{feedback_str}\n\n"
        "Decide on a category for this situation.\n\n"
        "Here are labeled examples of good category assignments:\n"
        f"{example_block}\n\n"
        "Rules:\n"
        "- If one of the existing labels fits well, use it as best_label.\n"
        "- You may include up to 2 other_labels that also somewhat fit.\n"
        "- If no existing labels fit, set best_label to null and create a new_label.\n"
        "- new_label MUST be a short topic-style category name (3–8 words).\n"
        "- new_label MUST NOT include 'If' or 'then'.\n"
        "- new_label should describe what the situation is about (theme/topic), not a full sentence.\n"
        "- Good examples: 'Possible rejection by others', 'Repairing a damaged relationship', 'Pressure to perform well'.\n"
        "- Bad examples: 'If someone criticizes me then I feel hurt', 'When X then Y'.\n\n"
        "- Treat listed personality components as important context for identifying recurring themes.\n"
        "- Prefer category names that resemble recurring themes or patterns, not exact event descriptions.\n"
        "- Focus on the underlying recurring pattern, not the specific event details.\n"
        "- The label should be similar in style to examples like 'Fear of disappointing others' or 'Feeling excluded by others'.\n"
        "- Do not force the output to exactly match any predefined example if a better natural label fits.\n"
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
