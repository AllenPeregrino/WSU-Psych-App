# vim: set ft=rst:

# Project Name
WSU Psych App
## Project summary
Software Design Project for WSU Psychology Clinic. Redcap web-based survey and Mindful application
### One-sentence description of the project
There are two applications for this project. The Redcap web-based survey inquires the clients about their main goals and how they affect them emotionally, as well as the people around them and their importance to the client. The Mindful application is for user to record any situations that happened to them recently and if it affected them positively or negatively, as well as how it affected them. Currently the app itself is just for the clients sake but we are looking to possibly implement an admin user that can access the users recorded situations

### Additional information about the project
For the Redcap web-based survey, the user can either choose to do a full assessment survey, which would take around an hour to complete, or a temperament, self-concept and interpersonal style, or personal goals/standards survey. The full assessment would cover all of the sub surveys. The survey consists of short answer questions and multiple choice questions that are straightforward for the user to complete. The Mindful application requires the user to register for an account, and can make new situations/view past situations on the home page of the application. The new situation after completing, will be categorized for the user to easily locate when using the application, and can find by going to the Past Situation Categories page. User can edit basic information about their situations but not the answers to the situations themselves. 

## Installation

### Prerequisites
Before running the installation instructions you must have installed:

•	Git
•	Python
•	Flask<2.3
o	Flask-mongoengine
o	Flask-json
o	Flask-login
o	Flask-moment
•	Openai
•	WTForms<3.0
o	Wtforms-sqlalchemy == 0.3
•	FPDF
•	Matplotlib

### Add-ons
•	Flask<2.3: Core web framework that powers the ap
o	Flask-mongoengine: Bridge between Flask and MongoDB
o	Flask-json: simplifies and formatting JSON responses
o	Flask-login: handles user authentication
o	Flask-moment: handles and displays dates and times
•	Openai: Official OpenAI API client
•	WTForms<3.0: form-handling library
o	Wtforms-sqlalchemy == 0.3: automatically generate form fields based on database models
•	FPDF: PDF generation library
•	Matplotlib: Plotting and visualization library
•	Pandas: Data analysis library

### Installation Steps
•	Git:
In terminal:
sudo apt install git

•	Python:
https://www.python.org/downloads/

In terminal:
git clone https://github.com/AllenPeregrino/WSU-Psych-App.git
cd WSU-Psych-App
python -m venv venv
venv\Scripts\activate

•	Flask<2.3:
o	Flask-mongoengine
o	Flask-json
o	Flask-login
o	Flask-moment
In terminal:
pip install "flask<2.3"
pip install flask-mongoengine flask-json flask-login flask-moment flask-cors
•	Openai:
In terminal: 
pip install openai
•	WTForms<3.0
o	Wtforms-sqlalchemy == 0.3
In terminal:
pip install "WTForms<3.0" "wtforms-sqlalchemy==0.3"
pip install fpdf matplotlib pandas
•	FPDF
In terminal:
pip install fpdf 

•	Matplotlib:
In terminal:
pip install matplotlib

•	Pandas:
In terminal:
pip install pandas

## Functionality
To run application:
In terminal:
python .\PsychClinic-ReportIntegration-Final\psychclinic.py
You should see something like:
* Running on http://127.0.0.1:5000
Open link to get to running application
To Navigate Website:
Register account or login
There you can make new situations, look at past situations, and find more information about the Mindful application

## Known Problems
As of right now there are two main functions that aren’t implemented yet. The Enter PICA Results, which will integrate the Redcap web-based survey with the Mindful application for the user. And the search feature which will make it easier for the user to find past situations based off keywords they enter
## Contributing

TODO: Leave the steps below if you want others to contribute to your project.

1.	Fork it!
2.	Clone your fork locally
a.	```bash
b.	   git clone https://github.com/<your-username>/WSU-Psych-App.git
c.	   cd WSU-Psych-App
3.	Create a new branch
a.	git checkout -b feature/my-new-feature
4.	Make your changes
5.	Commit your changes
a.	git commit -am "Add some feature"
6.	Push your branch to GitHub
a.	git push origin feature/my-new-feature
7.	Submit a Pull Request
a.	Go to your fork on GitHub and click “Compare & pull request” to propose your changes.

## Additional Documentation
https://github.com/AllenPeregrino/WSU-Psych-App/blob/9e35c6f9793fbc92cafb6ef15801df735dd52065/sprint_report.md

## License
https://github.com/AllenPeregrino/WSU-Psych-App/blob/3015764a4fef486b5399306f72196b70664a1313/LICENSE.txt
