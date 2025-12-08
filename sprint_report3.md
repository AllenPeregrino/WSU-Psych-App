# Sprint 3 Report 11/5-12/5

## What's New (User Facing)
 * AI name recommendation for new categories in Mindful App
 * AI recognizing and recommending similar categories for new situations
 * New goal questions added
 * Data pruner refactor complete

## Work Summary (Developer Facing)
During this sprint, for the Mindful Application we removed and rewrote the code for the behavior and sorting functions of the program to implement OpenAI into the program to read new situations to find the right category for it or recommend a name for a new one. 

During this spring for our personality assessment, we added new goal questions that clients gave us. As well as finishing the data pruner for the new data format. 

## Unfinished Work
For the Mindful Application, the AI may not be able to fully recognize similar categories from reading situations as it may not understand the concepts of what it means to be similar. The goal is to work with the client to better explain to the AI to recognize categories more efficiently. This will be done next semester. If this is completed faster than expected we can begin to integrate the Mindful Application with the REDCap survey results. 

The personality assessment needs to adjust our graph generator for our new goal questions. Once that is complete we can begin testing our PDF generator and look to publish our survey

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/9
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/10
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/7 
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/13 
 
 ## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
 
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/11 <<Not enough time to complete issue>>
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/12 <<REDCap Survey not 100% completed yet and may be subjected to changes>>
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/3 <<new goal question got added late>>

 

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * routes.py https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/Controller/routes.py 
 * ai_categorizer.py https://github.com/AllenPeregrino/WSU-Psych-App/blob/openai/MongoPsychClinicWeb/app/Service/ai_categorizer.py 
 * [Data_Pruner_redcaps .py]( https://github.com/AllenPeregrino/WSU-Psych-App/blob/main/PsychClinic-ReportIntegration-Redcap/Data_Pruner_redcaps.py )
 
## Retrospective Summary
Here's what went well:
  * Client communication
  * OpenAI API integration
  * adding goal questions
  * calculations for survey answers
 
Here's what we'd like to improve:
   * Documentation
   * Time Management
  
Here are changes we plan to implement in the next semester:
   * Improve AI in the Mindful Application
   * Integrate REDCap Survey results into the Mindful Application (possibly)
   * new PDF’s for goal questions
   * PDF generator testing
•	Survey publishing 

