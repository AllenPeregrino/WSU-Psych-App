# PICA (Person In Context Assessment)

## Project summary

### One-sentence description of the project

2 Applications, Self-Monitoring Application for clients to input daily situations to be used for both the client and their clinician. Survey/Survey Report using REDCap for the survey for clients to fill out and gain their personality assessments from their survey report.

### Additional information about the project

For the Redcap web-based survey, the user can either choose to do a full assessment survey, which would take around an hour to complete, or a temperament, self-concept and interpersonal style, or personal goals/standards survey. The full assessment would cover all of the sub surveys. The survey consists of short answer questions and multiple choice questions that are straightforward for the user to complete. The Mindful application requires the user to register for an account, and can make new situations/view past situations on the home page of the application. The new situation after completing, will be categorized for the user to easily locate when using the application, and can find by going to the Past Situation Categories page. User can edit basic information about their situations but not the answers to the situations themselves.

## Installation

### Prerequisites

Git
Python

### Installation Steps

To run the Self-Monitoring app locally, download the codebase locally on your device. Once installed, open Command Prompt on your device and open the folder that you have installed the codebase on. In the terminal, run the following “pip install -r requirements.txt”. You will also need to create a virtual environment. To create one, run the following command “python -m venv venv”. To open the virtual environment run “venv\scripts\activate”. Once you have opened the virtual environment, you can now run the program by inputting “python MongoPsychClinicWeb\psychclinic.py”. This should provide a link locally that you can open by holding your Control key and left clicking.
To run the live Self-Monitoring App, you may follow the link below located in the Additional Documentation section.

## Functionality

For the Self-Monitoring App: When you first open the page, you will be directed to a Login page. Once you create an account and login, you will be redirected to the Homepage (after being logged in once, you will always be directed to the Homepage unless you logout). To find more information about the features within the App, you can press the Information page, to find out all of the features within the app. 

## Known Problems

•	The AI used in the Self-Monitoring App may, in rare cases, not work properly and won’t suggest any categories/new category name. Main file the AI is used in is located in "WSU-Psych-App\MongoPsychClinicWeb\app\Service\ai_categorizer.py".

## Additional Documentation

•	Link to Self-Monitoring App: https://pica-wsupsych.pythonanywhere.com/
•	Link to REDCap Survey: 
•	Link to PythonAnywhere: https://www.pythonanywhere.com/user/WSUPsych/
### Tips
•	If AI does not work at all: Check if the quota for the credits have been reached. You can check by having the main client follow this link, https://platform.openai.com/settings/organization/billing/overview. If the credits are at $0, recharge the balance (recommend setting up auto-recharge so you don’t have to worry about this).
•	

## License

Located within the PythonAnywhere under “LICENSE.txt”
