# Sprint 2  Report 10/5 – 11/5

## YouTube link of Sprint 2 Video (Make this video unlisted) (feature presenation is shown towards end of the video)
https://youtu.be/KijPbiWZDmk


## What's New (User Facing)
 * REDCap survey migration
 * API integration
*  Category Recommendation for situations


## Work Summary (Developer Facing)
This sprint we were able to migrate all questions from the original Qualtrics survey into REDCap. Just above 400 questions it took some time as REDCap is less user friendly than Qualtrics. After the survey was finished we were able to complete the API integration to get data records from REDCap to a CSV file in our project folder. As for the mindful application, we were able to get the app up and running locally and had to sift through all the code to fully understand where things are and how the logic flows as there was no prior documentation provided for the existing codebase. With that we were able to fix and fully implement the matching categories for new situations. 
## Unfinished Work
We were hoping to finish refactoring the data pruner but due to the survey migration taking more time than expected we were unable to start. We have started to implement using artificial intelligence within the app, specifically for helping categorize situations. This involves learning how to code with the OpenAI API, which is why we were unable to complete it within sprint 2. This will all be moved to sprint 3. 

## Completed Issues/User Stories
Here are links to the issues that we completed in this sprint:

 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/4
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/5 
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/8

 ## Incomplete Issues/User Stories
 Here are links to issues we worked on but did not complete in this sprint:
 
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/7  due to the survey migration taking longer than expected we were unable to refactor data pruner. 
 * https://github.com/AllenPeregrino/WSU-Psych-App/issues/9 needed to spend time learning how to make code that uses AI

## Code Files for Review
Please review the following code files, which were actively developed during this sprint, for quality:
 * automated_responses_redcaps.py  https://github.com/AllenPeregrino/WSU-Psych-App/blob/API-integration/PsychClinic-ReportIntegration-Redcap/automated_responses_redcaps.py
* routes.py https://github.com/AllenPeregrino/WSU-Psych-App/blob/main/MongoPsychClinicWeb/app/Controller/routes.py
 
## Retrospective Summary
Here's what went well:
  * Survey migration
  * API integration
  * Client communication
 
Here's what we'd like to improve:
   * documentation
  
Here are changes we plan to implement in the next sprint:
   * refactor data pruner
   * publish REDCap survey
   * Implementing AI

