#import openai
from flask_login import current_user

from app.Model.models import Survey

from openai import OpenAI
api_key = ''

client = OpenAI(api_key=api_key)

def analyze_entry(allSurveys, currentSurvey):
    # Default values for return
    similarSurvey = None
    allSimilarList = []

    try:
        current_options = [
            currentSurvey.thoughts_pos,
            currentSurvey.feelings_pos,
            currentSurvey.behaviors_mc,
            currentSurvey.thoughts_neg,
            currentSurvey.feelings_neg
        ]

        messages = [
            {"role": "system", "content": "Identify the survey that is most similar to the current one based on the options selected."}
        ]
        messages.append({"role": "user", "content": f"Current survey options: {current_options}"})

        for survey in allSurveys:
            if survey.id != currentSurvey.id:
                survey_options = [
                    survey.thoughts_pos,
                    survey.feelings_pos,
                    survey.behaviors_mc,
                    survey.thoughts_neg,
                    survey.feelings_neg
                ]
                messages.append({"role": "user", "content": f"Survey ID {survey.id} options: {survey_options}"})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
            temperature=0.5
        )

        if response.choices:
            generated_text = response.choices[0].text.strip()
            similarSurvey = "12345"  # Placeholder
            allSimilarList = "12345,67890"  # Placeholder
        if not similarSurvey or not allSimilarList:
            print("Failed to analyze surveys or no surveys found.")
        else:
            print(f"Most similar survey: {similarSurvey}")
            print(f"Similar surveys list: {allSimilarList}")
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {str(e)}")
        # Return default None values for both in case of exception
        return similarSurvey, allSimilarList

    return similarSurvey, allSimilarList







