from __future__ import print_function
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), 'app/report_generator'))

from bson import ObjectId
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, jsonify

from app.Controller.OpenAi import analyze_entry
from config import Config
from flask_login import  current_user, login_required
from app import db
from app.Model.models import User, Survey, SituationList, Signature, Thoughtspositive, Thoughtsnegative, \
    Feelingspositive, Feelingsnegative, Behaviormc
from app.Controller.forms import SituationForm, WhatHappened, Thoughts, Feelings, Behavior, SortingForm2, AdminQsortForm, SortingForm
from datetime import datetime
from sqlalchemy.sql import func
from flask import Flask
from sqlalchemy import desc
from flask import session
from app.report_generator.Report_Generator_Sorting import create_report
from app.report_generator.automated_responses import get_survey
import traceback
import pandas as pd

PROCESSED_RESPONSES_FILE = "/home/WSUPsych/PsychClinic-ReportIntegration-Final/app/report_generator/processed_responses.txt"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_fallback_key')

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.admin != 0:
        return redirect(url_for('auth.login'))

    surveys = Survey.objects(user=current_user)
    ifs = Signature.objects(user=current_user)

    return render_template('index.html', title="PsychClinic Web", posts=surveys, signature=ifs)

@bp_routes.route('/admin_view_surveys', methods=['GET'])
@login_required
def admin_view_survey():
    if current_user.admin != 1:
        return redirect(url_for('auth.login'))
    allUsers = User.objects(admin=0).all()
    return render_template('admin_view_surveys.html', title="PsychClinic Web", users = allUsers)

@bp_routes.route('/admin_index', methods=['GET'])
@login_required
def admin_index():
    if current_user.admin != 1:
        return redirect(url_for('auth.login'))

    all_users = User.objects(admin=0)
    return render_template('admin_index.html', title="PsychClinic Web", users=all_users)

@bp_routes.route('/information', methods=['GET'])
@login_required
def information():
    return render_template('information.html', title="PsychClinic Web")

@bp_routes.route('/pastSituations', methods=['GET'])
@login_required
def pastSituations():
    if current_user.admin != 0:
        return redirect(url_for('auth.login'))

    surveys = Survey.objects(user=current_user)
    ifs = Signature.objects(user=current_user)

    return render_template('pastSituations.html', title="PsychClinic Web", posts=surveys, signature=ifs)

@bp_routes.route('/search', methods=['GET'])
@login_required
def search():
    return render_template('search.html', title="PsychClinic Web")

@bp_routes.route('/pica', methods=['GET'])
@login_required
def pica():
    return render_template('PICA.html', title="PsychClinic Web")

@bp_routes.route('/qsort', methods=['GET', 'POST'])
@login_required
def qsort():
    qsortForm = AdminQsortForm()
    qsortForm.thought_pos.choices = [(str(t.id), t.name) for t in Thoughtspositive.objects]
    qsortForm.thought_neg.choices = [(str(t.id), t.name) for t in Thoughtsnegative.objects]
    qsortForm.feelings_pos.choices = [(str(t.id), t.name) for t in Feelingspositive.objects]
    qsortForm.feelings_neg.choices = [(str(t.id), t.name) for t in Feelingsnegative.objects]
    qsortForm.behavior_mc.choices = [(str(t.id), t.name) for t in Behaviormc.objects]

    if qsortForm.validate_on_submit():

        unique_user = User.objects(id=qsortForm.user_id.data).first()
        if unique_user is None:
            flash("No user found with that ID")
            return redirect(url_for('routes.qsort'))
        else:
            if qsortForm.choice.data == 'True':
                situation_category_value = "Mostly positive feelings"
            else:
                situation_category_value = "Mostly negative feelings"

            newSurvey = Survey(user = qsortForm.user_id.data,
                               what_happened = qsortForm.prototypicalSituation.data,
                               situation = situation_category_value)

            newSurvey.save_thoughts(
                thoughts_pos=qsortForm.thought_pos.data,
                thoughts_neg=qsortForm.thought_neg.data,
                thoughts_meaning_of_event = qsortForm.protoThought.data
            )
            newSurvey.save_feelings(
                feelings_pos=qsortForm.feelings_pos.data,
                feelings_neg=qsortForm.feelings_neg.data
            )
            newSurvey.save_behaviors(
                behaviors_mc = qsortForm.behavior_mc.data,
                behaviors_description = qsortForm.protoBehavior.data,
                behaviors_outcome = qsortForm.protoGoal.data
            )

            newIfThen = Signature( ifThen = qsortForm.ifthenSignature.data, user = unique_user)
            newIfThen.save()
            newSurvey.save()
            if qsortForm.situationList.data:
                temp = qsortForm.situationList.data.split(',')
                for t in temp:
                    sitList = SituationList(signature = newIfThen, situation = t)
                    sitList.save()
            newSurvey.signature = newIfThen
            newSurvey.save()

            return redirect(url_for('routes.admin_index'))
    return render_template('qsort.html', form = qsortForm)
@bp_routes.route('/surveyPost/<survey_id>', methods=['GET'])
@login_required
def surveyPost(survey_id):
    unique_survey = Survey.objects(id=survey_id).first()
    signature = Signature.objects(id=unique_survey.signature.id).first()
    return render_template('surveyPost.html', title="PsychClinic Web", post=unique_survey, time =unique_survey.timestamp.strftime('%B %d %Y '), signature = signature.ifThen)

@bp_routes.route('/userSurveys/<user_id>', methods=['GET'])
@login_required
def userSurveys(user_id):
    unique_user=User.objects(id=user_id).first()
    ifs = Signature.objects(user=unique_user)
    return render_template('userSignatures.html', user=unique_user,  signature = ifs.all())

@bp_routes.route('/ifThenSurveys/<user_id>/<signature_id>', methods=['GET'])
@login_required
def ifThenSurveys(user_id, signature_id):
    unique_user = User.objects.get(id=ObjectId(user_id))
    surveys = Survey.objects(user=unique_user, signature=ObjectId(signature_id)).order_by('-timestamp')
    ifs = Signature.objects(user=unique_user, id=ObjectId(signature_id)).first()

    return render_template('userSurveys.html', user=unique_user, surveys=surveys, title=ifs.ifThen)

@bp_routes.route('/situation_category', methods=['GET', 'POST'])
@login_required
def situation_category():
    feelingForm = SituationForm()
    # get pos neg value from URL
    pos_neg_checker = request.args.get('pos_neg', session.get('pos_neg_checker', 'False'))

    if feelingForm.validate_on_submit():
        if feelingForm.choice.data == 'True':
            situation_category_value = "Mostly positive feelings"
            pos_neg_checker = "True"
        else:
            situation_category_value = "Mostly negative feelings"
            pos_neg_checker= "False"

        new_survey = Survey(user=current_user, situation=situation_category_value)
        new_survey.save()

        # Helps to store answer for back buttons
        session['pos_neg_checker'] = pos_neg_checker

        return redirect(url_for('routes.what_happened', survey_id=new_survey.id, pos_neg=pos_neg_checker, back=0))

    # only get the previous value when form is resubmitted; this helps so the form isn't filled on the first opening
    if request.method == 'POST':
        feelingForm.choice.data = pos_neg_checker

    return render_template('feelings_page.html', form=feelingForm, pos_neg=pos_neg_checker, back=0)


@bp_routes.route('/what_happened/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def what_happened(survey_id,pos_neg, back):
    #create a back that deletes the survey if the user goes back
    whatHappenedForm = WhatHappened()
    unique_survey = Survey.objects(id=survey_id, user=current_user).first()

    if back == '1':  # if back is 1, then we want to clear the what happened field
        print("testing")
        if unique_survey:
            unique_survey.what_happened = ""
            unique_survey.save()

    pos_neg_checker = session.get('pos_neg_checker', 'False')

    if whatHappenedForm.validate_on_submit():
        if unique_survey:
            unique_survey.what_happened = whatHappenedForm.answer.data
            unique_survey.save()

        return redirect(url_for('routes.thoughts', survey_id=unique_survey.id, pos_neg=pos_neg_checker, back='0'))

    return render_template('whatHappened.html', form=whatHappenedForm, pos_neg=pos_neg_checker, back='0')

@bp_routes.route('/thoughts/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def thoughts(survey_id, pos_neg,back):
    thoughtsForm = Thoughts()
    unique_survey = Survey.objects(id=survey_id, user=current_user).first()

    thoughtsForm.thought_pos.choices = [(str(t.id), t.name) for t in Thoughtspositive.objects]
    thoughtsForm.thought_neg.choices = [(str(t.id), t.name) for t in Thoughtsnegative.objects]

    if back == '1':  # if back is 1, then we want to clear the thoughts field
        print("testing")
        if unique_survey:
            unique_survey.thoughts_pos = []
            unique_survey.thoughts_neg = []
            unique_survey.thoughts_meaning_of_event = ""
            unique_survey.thoughts_summary = ""
            unique_survey.save()


    if thoughtsForm.validate_on_submit():
        if unique_survey:
            unique_survey.save_thoughts(
                thoughts_pos=thoughtsForm.thought_pos.data,
                thoughts_neg=thoughtsForm.thought_neg.data,
                thoughts_meaning_of_event=thoughtsForm.meaning_of_event.data
            )
        return redirect(url_for('routes.feelings', survey_id=unique_survey.id, pos_neg=pos_neg, back='0'))

    return render_template('thoughts.html', form=thoughtsForm, pos_neg=pos_neg, back='0', survey_id=survey_id)

@bp_routes.route('/feelings/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def feelings(survey_id, pos_neg, back=0):
    feelingsForm = Feelings()
    unique_survey = Survey.objects(id=survey_id).first()

    feelingsForm.feelings_pos.choices = [(str(t.id), t.name) for t in Feelingspositive.objects]
    feelingsForm.feelings_neg.choices = [(str(t.id), t.name) for t in Feelingsnegative.objects]

    if back == '1':
        print("testing")
        unique_survey.feelings_pos = []
        unique_survey.feelings_neg = []
        unique_survey.save()
        # return redirect(url_for('routes.thoughts', survey_id = unique_survey.id, pos_neg=pos_neg, back='0'))
    if feelingsForm.validate_on_submit():
        if unique_survey:
            unique_survey.save_feelings(
                feelings_pos=feelingsForm.feelings_pos.data,
                feelings_neg=feelingsForm.feelings_neg.data
            )
        return redirect(url_for('routes.behavior', survey_id = unique_survey.id, pos_neg=pos_neg, back='0'))

    return render_template('feelings.html', form=feelingsForm, pos_neg=pos_neg, back='0', survey_id=survey_id)


@bp_routes.route('/behavior/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def behavior(survey_id, pos_neg, back='0'):
    behaviorForm = Behavior()
    unique_survey = Survey.objects(id=survey_id).first()

    if not unique_survey:
        flash("Survey not found.")
        return redirect(url_for('routes.index'))

    behaviorForm.behaviors_mc.choices = [(str(t.id), t.name) for t in Behaviormc.objects]

    if behaviorForm.validate_on_submit():
        # Save the behaviors based on the type of feelings, positive or negative
        if pos_neg == "False":
            unique_survey.save_behaviors_negative(
                behaviors_mc=behaviorForm.behaviors_mc.data,
                behaviors_description=behaviorForm.description.data,
                behaviors_outcome=behaviorForm.outcome.data
            )
        else:
            unique_survey.save_behaviors_positive(
                behaviors_mc=behaviorForm.behaviors_mc.data,
                behaviors_description=behaviorForm.description.data
            )

        allSurveys = Survey.objects(user=current_user, signature__exists=True)
        similarSurvey, allSimilarList = analyze_entry(allSurveys, unique_survey)

        # Handling potential None values
        if not similarSurvey or not allSimilarList:
            similarSurvey = 'defaultSimilarSurvey'
            allSimilarList = 'defaultAllSimilarList'

        # Logging for debugging
        print(f"Redirecting to sorting with similarSurvey: {similarSurvey} and allSimilarList: {allSimilarList}")

        return redirect(url_for('routes.sorting', survey_id=unique_survey.id, pos_neg=pos_neg, back='0', similarSurvey=similarSurvey, allSimilarList=allSimilarList))

    return render_template('behavior.html', form=behaviorForm, pos_neg=pos_neg, back=back, survey_id=survey_id)

@bp_routes.route('/sorting/<survey_id>/<pos_neg>/<back>/<similarSurvey>/<allSimilarList>', methods=['GET', 'POST'])
@login_required
def sorting(survey_id, pos_neg, back, similarSurvey, allSimilarList):
    unique_survey = Survey.objects(id=survey_id).first()
    allUserSignatures = Signature.objects(user=current_user.id).all()
    sortForm = SortingForm()
    categories = []
    if pos_neg == 'positive':
         categories = Feelingspositive.objects(user=current_user)
    elif pos_neg == 'negative':
         categories = Feelingsnegative.objects(user=current_user)
    else:
        categories = []

    if sortForm.validate_on_submit():
         flash("Form processed.")
         return redirect(url_for('routes.index'))

    return render_template('sorting.html', form=sortForm, survey_id=survey_id, categories=categories, pos_neg=pos_neg, similarSurvey=similarSurvey, allUserSignatures=allUserSignatures, allSimilarList=allSimilarList)

def intersection(survey, currentSurvey):
    result = []
    for s in survey:
        if s in currentSurvey:
            result.append(s)
    print(result)
    return len(result)

def convertList(list):
    string = ""
    for l in list:
        string = string + str(l) + ','
    if string == "":
        string = "-1"
    else:
        string = string[:-1]
    return string

def convertString(list):
    return list.split(',')

@app.route('/analyze/<int:survey_id>')
@login_required
def analyze_survey(survey_id):
    currentSurvey = Survey.query.get(survey_id)
    allSurveys = Survey.query.filter(Survey.user_id == current_user.id).all()

    similarSurvey, allSimilarList = analyze_entry(allSurveys, currentSurvey)

    if not similarSurvey:
        return "No similar survey found or error in analysis.", 400

    # Redirect or render a template with the results
    return redirect(url_for('show_results', similarSurvey=similarSurvey, allSimilarList=allSimilarList))

@app.route('/results')
@login_required
def show_results():
    similarSurvey = request.args.get('similarSurvey')
    allSimilarList = request.args.get('allSimilarList')
    return render_template('results.html', similarSurvey=similarSurvey, allSimilarList=allSimilarList)

@bp_routes.route('/generate_report', methods=['GET'])
@login_required
def generate_report():
    try:
        survey_id = 'SV_3wvBtxhaQcsl06G'
        save_survey_path = "/home/WSUPsych/PsychClinic-ReportIntegration-Final/app/report_generator"
        print(f"Saving survey CSV to: {save_survey_path}")

        # Call the get_survey function and log the output
        csv_file_path = get_survey(save_survey=save_survey_path, survey_id=survey_id)
        print(f"CSV file path generated: {csv_file_path}")

        # Check if the file exists before proceeding
        if not csv_file_path or not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found at {csv_file_path}")

        # Proceed with report generation
        create_report(csv_file_path)
        return "Report generated and email sent!", 200

    except FileNotFoundError as fnf_error:
        # Catch file-related errors
        print(f"File not found error: {fnf_error}")
        return f"Error generating report: {str(fnf_error)}", 500

    except Exception as e:
        # Catch all other exceptions
        traceback.print_exc()
        return f"Error generating report: {str(e)}", 500

def load_processed_responses():
    """Load processed response IDs from file, creating the file if it doesn't exist."""
    if not os.path.exists(PROCESSED_RESPONSES_FILE):
        # Create an empty file to avoid errors
        with open(PROCESSED_RESPONSES_FILE, "w") as f:
            pass  # Just creates the file, doesn't write anything
        return set()

    # Read the file if it exists
    with open(PROCESSED_RESPONSES_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed_response(response_id):
    """Save a successfully processed ResponseID to file."""
    with open(PROCESSED_RESPONSES_FILE, "a") as f:
        f.write(response_id + "\n")

@bp_routes.route('/qualtrics_webhook', methods=['POST'])
def qualtrics_webhook():
    try:
        # Log incoming request data
        print("Incoming request data: ", request.get_data())
        print("Request headers: ", request.headers)

        # Check for the token in the request headers
        token = request.headers.get('Authorization')
        if token != 'Token mysecrettoken123':
            return jsonify({"status": "Unauthorized"}), 401

        # Process the webhook data
        data = request.get_json()
        survey_id = data.get('SurveyID')
        response_id = data.get('ResponseID')

        # Log the survey ID and response ID
        print(f"SurveyID: {survey_id}, ResponseID: {response_id}")

        if not survey_id or not response_id:
            return jsonify({"status": "Bad Request", "error": "Missing SurveyID or ResponseID"}), 400

        # Load previously processed responses
        processed_responses = load_processed_responses()

        print(f"Already Processed Response IDs: {processed_responses}")

        print(f"ResponseID {response_id} will be checked")
        # Check if this response has already been processed
        if response_id in processed_responses:
            print(f"ResponseID {response_id} has already been processed. Skipping.")
            return jsonify({"status": "Already Processed", "ResponseID": response_id}), 200

        # Define the path where you want to save the survey CSV file
        save_survey_path = "/home/WSUPsych/PsychClinic-ReportIntegration-Final/app/report_generator"

        try:
            # Call the get_survey() function from automated_responses.py
            csv_survey_path = get_survey(save_survey=save_survey_path, survey_id=survey_id)

            # Debugging: Print the returned path
            print(f"DEBUG: csv_survey_path returned from get_survey(): {csv_survey_path}")

            # Proceed with report generation using the downloaded CSV
            create_report(csv_survey_path)

            # Save the response ID **only if everything above is successful**
            save_processed_response(response_id)

            return jsonify({"status": "Webhook processed successfully"}), 200

        except Exception as e:
            print(f"Error processing ResponseID {response_id}: {str(e)}")
            traceback.print_exc()
            return jsonify({"status": "Error processing webhook", "error": str(e)}), 500

    except Exception as e:
        # Print the full traceback for debugging
        print(f"Critical error occurred: {str(e)}")
        traceback.print_exc()
        return jsonify({"status": "Critical error processing webhook", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)