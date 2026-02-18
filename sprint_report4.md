# Sprint 4 Report (1/12-2/17)
## YouTube link of Sprint * Video 
https://youtu.be/ITnCv1wzrZY
## What's New (User Facing)
* PDF generation with new goal measures
* AI Suggestion Feedback
## Work Summary (Developer Facing)
PDF generation will now include new goal data measures with additional graphs using data from our redcap survey
The application will now ask the user if the categorization suggestion was useful so that the AI can learn from the feedback to improve it. 

## Unfinished Work
The PDF is still incomplete as there is some text generation that has yet to be completed. But all data from the survey is accurately portrayed in the PDF, just need to add descriptive text
Adding personality components to user’s profiles. Clients and clinicians work together to add personality components to the clients' profiles. During diary text entries, users will be asked if the entry relates to their specific personality components. 

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:
•	https://github.com/AllenPeregrino/WSU-Psych-App/issues/3
•	https://github.com/AllenPeregrino/WSU-Psych-App/issues/11

## Incomplete Issues/User Stories
Here are links to issues we worked on but did not complete in this sprint:
* https://github.com/AllenPeregrino/WSU-Psych-App/issues/14 << New feature requested from the client, still working on implementing the feature>>
* URL of issue 2 <<One sentence explanation of why issue was not completed>>

## Code Files for Review
Please review the following code files, which were actively developed during this
sprint, for quality:
* [report_generator]https://github.com/AllenPeregrino/WSU-Psych-App/tree/main/PsychClinic-ReportIntegration-Redcap/app/report_generator
* [routes.py]( https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/Controller/routes.py)
* [models.py]( https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/Model/models.py)
*[sorting.html] https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/View/templates/sorting.html
*[ai_categorizer.py] https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/Service/ai_categorizer.py

## Retrospective Summary
Here's what went well:
* Client meetings
* PDF generation
* Improvement on AI in the Mindful Application
Here's what we'd like to improve:
* Documentation
* Organizing the repository
Here are changes we plan to implement in the next sprint:
* Redcap publishing and final tests
* Personality components to users
