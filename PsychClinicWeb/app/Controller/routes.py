from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from flask_login import  current_user, login_required
from app import db
from app.Model.models import User, Survey, SituationList, Signature
from app.Controller.forms import SituationForm, WhatHappened, Thoughts, Feelings, Behavior, SortingForm2, AdminQsortForm, SortingForm
from datetime import datetime
from sqlalchemy.sql import func

from sqlalchemy import desc

from flask import session


bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.admin !=0:
        return redirect(url_for('auth.login'))
    surveys = Survey.query.filter_by(user_id=current_user.id)
    ifs = Signature.query.filter_by(user_id=current_user.id)
    return render_template('index.html', title="PsychClinic Web", posts=surveys.all(), signature = ifs.all())

@bp_routes.route('/admin_view_surveys', methods=['GET'])
@login_required
def admin_view_survey():
    if current_user.admin !=1:
        return redirect(url_for('auth.login'))
    allUsers = User.query.filter_by(admin=0).all()
    return render_template('admin_view_surveys.html', title="PsychClinic Web", users = allUsers)



@bp_routes.route('/admin_index', methods=['GET'])
@login_required
def admin_index():
    if current_user.admin !=1:
        return redirect(url_for('auth.login'))
    allUsers = User.query.filter_by(admin=0).all()
    return render_template('admin_index.html', title="PsychClinic Web", users = allUsers)

@bp_routes.route('/information', methods=['GET'])
@login_required
def information():
    return render_template('information.html', title="PsychClinic Web")

@bp_routes.route('/pastSituations', methods=['GET'])
@login_required
def pastSituations():
    if current_user.admin !=0:
        return redirect(url_for('auth.login'))
    surveys = Survey.query.filter_by(user_id=current_user.id)
    ifs = Signature.query.filter_by(user_id=current_user.id)
    return render_template('pastSituations.html', title="PsychClinic Web", posts=surveys.all(), signature = ifs.all())

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
    if qsortForm.validate_on_submit():
        
        unique_user=User.query.filter_by(id=qsortForm.user_id.data).first()
        if unique_user is None:
            flash("No user found with that ID")
            return redirect(url_for('routes.qsort'))
        else:
            newSurvey = Survey(user_id = qsortForm.user_id.data,
                                what_happened = qsortForm.prototypicalSituation.data,thoughts_summary = qsortForm.protoThought.data ,
                                behaviors_description = qsortForm.protoBehavior.data, behaviors_outcome = qsortForm.protoGoal.data)
            for t in qsortForm.thought_pos.data:
                newSurvey.thoughts_pos.append(t)
            for t in qsortForm.thought_neg.data:
                newSurvey.thoughts_neg.append(t)
            for t in qsortForm.feelings_pos.data:
                newSurvey.feelings_pos.append(t)
            for t in qsortForm.feelings_neg.data:
                newSurvey.feelings_neg.append(t)
            for t in qsortForm.behavior_mc.data:
                newSurvey.behaviors_mc.append(t)
                
        
            if qsortForm.choice.data == 'True':
                newSurvey.situation =  "Mostly positive feelings"
            else:
                newSurvey.situation  = "Mostly negative feelings"

            newIfThen = Signature( ifThen = qsortForm.ifthenSignature.data, user_id = unique_user.id)
            db.session.add(newIfThen)
            db.session.add(newSurvey)
            db.session.commit()
            if qsortForm.situationList.data:
                temp = qsortForm.situationList.data.split(',')
                for t in temp:
                    sitList = SituationList(signature_id = newIfThen.id, situation = t)
                    db.session.add(sitList)
            # newIfThen = IfThenSignature( ifThen = qsortForm.ifthenSignature.data)
            # db.session.add(newIfThen)
            newSurvey.signature_id = newIfThen.id
            db.session.commit()
           
            return redirect(url_for('routes.admin_index'))
    return render_template('qsort.html', form = qsortForm)
@bp_routes.route('/surveyPost/<survey_id>', methods=['GET'])
@login_required
def surveyPost(survey_id):
    print(survey_id)
    unique_survey=Survey.query.filter_by(id=int(survey_id)).first()
    print(unique_survey.signature_id)
    signature = Signature.query.filter_by(id = unique_survey.signature_id).first()
    print(signature)
    return render_template('surveyPost.html', title="PsychClinic Web", post=unique_survey, time =unique_survey.timestamp.strftime('%B %d %Y '), signature = signature.ifThen)

@bp_routes.route('/userSurveys/<user_id>', methods=['GET'])
@login_required
def userSurveys(user_id):
    unique_user=User.query.filter_by(id=user_id).first()
    # surveys = Survey.query.filter_by(user_id=unique_user.id).order_by(Survey.timestamp.desc())
    ifs = Signature.query.filter_by(user_id=unique_user.id)
    # t = unique_user.firstname + " "+  unique_user.lastname
    return render_template('userSignatures.html', user=unique_user,  signature = ifs.all())

@bp_routes.route('/ifThenSurveys/<user_id>/<signature_id>', methods=['GET'])
@login_required
def ifThenSurveys(user_id, signature_id):
    unique_user=User.query.filter_by(id=user_id).first()
    surveys = Survey.query.filter_by(user_id=unique_user.id, signature_id =int(signature_id) ).order_by(Survey.timestamp.desc())
    ifs = Signature.query.filter_by(user_id=unique_user.id, id =int(signature_id) ).first()
    return render_template('userSurveys.html', user=unique_user, surveys=surveys, title =ifs.ifThen )

@bp_routes.route('/situation_category', methods=['GET', 'POST'])
@login_required
def situation_category():
    feelingForm = SituationForm()

    # get pos neg value from URL
    pos_negChecker = request.args.get('pos_neg', session.get('pos_negChecker', 'False'))

    if feelingForm.validate_on_submit():
        newSurvey = Survey()
        if feelingForm.choice.data == 'True':
            newSurvey = Survey(user_id=current_user.id, situation = "Mostly positive feelings")
            pos_negChecker="True"
        else:
            newSurvey = Survey(user_id=current_user.id,  situation = "Mostly negative feelings")
            pos_negChecker="False"

        # Helps to store answer for back buttons
        session['pos_negChecker'] = pos_negChecker

        db.session.add(newSurvey)
        db.session.commit()
        return redirect(url_for('routes.what_happened', survey_id = newSurvey.id,pos_neg=pos_negChecker, back=0))

    # only get the previous value when form is resubmitted this helps so form isnt filled on first opening
    if request.method == 'POST':
        feelingForm.choice.data = pos_negChecker

    return render_template('feelings_page.html', form=feelingForm, pos_neg=pos_negChecker, back=0)

@bp_routes.route('/what_happened/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def what_happened(survey_id,pos_neg, back):
    #create a back that deletes the survey if the user goes back
    whatHappenedForm = WhatHappened()
    unique_survey=Survey.query.filter_by(id=survey_id).first()

    if back == '1': #if back is 1, then we want to clear the what happened field
        print("testing")
        unique_survey.what_happened = ""
        db.session.commit()

    pos_negChecker = session.get('pos_negChecker', 'False')

       # return redirect(url_for('routes.situation_category', survey_id = unique_survey.id, pos_neg=pos_neg, back=back))
    if whatHappenedForm.validate_on_submit():
        if unique_survey:
            unique_survey.what_happened = whatHappenedForm.answer.data
            db.session.commit()       
        return redirect(url_for('routes.thoughts', survey_id = unique_survey.id, pos_neg=pos_negChecker, back='0'))
       
    return render_template('whatHappened.html', form=whatHappenedForm, pos_neg=pos_negChecker, back='0')

@bp_routes.route('/thoughts/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def thoughts(survey_id, pos_neg,back):
    thoughtsForm = Thoughts()
    unique_survey=Survey.query.filter_by(id=survey_id).first()
   
    if back == '1': #if back is 1, then we want to clear the thoughts field
        print("testing")
        unique_survey.thoughts_pos = []
        unique_survey.thoughts_neg = []
        unique_survey.thoughts_meaning_of_event = ""
        unique_survey.thoughts_summary = ""
        db.session.commit()
        # return redirect(url_for('routes.what_happened', survey_id = unique_survey.id, pos_neg=pos_neg, back=0))
    if thoughtsForm.validate_on_submit(): 
        if unique_survey:
            for t in thoughtsForm.thought_pos.data:
                unique_survey.thoughts_pos.append(t)
            for t in thoughtsForm.thought_neg.data:
                unique_survey.thoughts_neg.append(t)
            unique_survey.thoughts_meaning_of_event=thoughtsForm.meaning_of_event.data

            db.session.commit()
        return redirect(url_for('routes.feelings', survey_id = unique_survey.id, pos_neg=pos_neg, back='0'))
       
    return render_template('thoughts.html', form=thoughtsForm, pos_neg=pos_neg, back='0', survey_id=survey_id)

@bp_routes.route('/feelings/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def feelings(survey_id, pos_neg, back=0):
    feelingsForm = Feelings()
    unique_survey=Survey.query.filter_by(id=survey_id).first()
    if back == '1':
        print("testing")
        unique_survey.feelings_pos = []
        unique_survey.feelings_neg = []
        db.session.commit()
        # return redirect(url_for('routes.thoughts', survey_id = unique_survey.id, pos_neg=pos_neg, back='0'))
    if feelingsForm.validate_on_submit():
        if unique_survey:
            for t in feelingsForm.feelings_pos.data:
                unique_survey.feelings_pos.append(t)
            for t in feelingsForm.feelings_neg.data:
                unique_survey.feelings_neg.append(t)
            db.session.commit()
        return redirect(url_for('routes.behavior', survey_id = unique_survey.id, pos_neg=pos_neg, back='0'))
       
    return render_template('feelings.html', form=feelingsForm, pos_neg=pos_neg, back='0', survey_id=survey_id)


@bp_routes.route('/behavior/<survey_id>/<pos_neg>/<back>', methods=['GET', 'POST'])
@login_required
def behavior(survey_id, pos_neg,back=0):
    print("pos_neg", pos_neg)
    behaviorForm = Behavior()
    # unique survey is the current user survey the future new one
    unique_survey=Survey.query.filter_by(id=survey_id).first()
    if back == '1':
        print("testing")
        unique_survey.behaviors_mc = []
        unique_survey.behaviors_description = ""
        unique_survey.behaviors_outcome = ""
        db.session.commit()
        # return redirect(url_for('routes.feelings', survey_id = unique_survey.id, pos_neg=pos_neg, back=back))
    if behaviorForm.validate_on_submit():
        if unique_survey:
            unique_survey.behaviors_description=behaviorForm.description.data
            unique_survey.behaviors_outcome=behaviorForm.outcome.data
            for t in behaviorForm.behavior_mc.data:
                unique_survey.behaviors_mc.append(t)
            db.session.commit()
            
           
            allSurveys = Survey.query.filter_by(user_id=current_user.id)
            print("all surveys", allSurveys)
            allSimilarSurveyID = []
            similarSurvey = ""
            
            compareTP = []
            compareFP = []
            compareB = []
            compareTN = []
            compareFN = []
            # print(type(unique_survey.thoughts_pos))
            currentListTP = []
            currentListFP = []
            currentListB = []
            currentListTN = []
            currentListFN = []

            #gather all information of choose all that apply questions for current survey
            for t in  unique_survey.thoughts_pos.all():
                currentListTP.append(t.id )
            for f in unique_survey.feelings_pos.all():
                currentListFP.append(f.id)
            for b in unique_survey.behaviors_mc.all():
                currentListB.append(b.id)
            for tn in unique_survey.thoughts_neg.all():
                currentListTN.append(tn.id)
            for fn in unique_survey.feelings_neg.all():
                currentListFN.append(fn.id)
            # print(currentList)
            intersectionCountTP = 0
            intersectionCountFP = 0
            intersectionCountB = 0
            intersectionCountTN = 0
            intersectionCountFN = 0
           # loop through all surveys to find similar surveys
            # only want similar surveys with signature ids
            print("new change")
            for survey in allSurveys:
                print("survey signature id", survey.signature_id)
                if survey.signature_id is not None:
                    if str(survey.id) != survey_id:
                        # collects data on survey in all of the surveys if positive situation collect data here
                        if unique_survey.situation == 'Mostly positive feelings' :
                            if survey.situation == 'Mostly positive feelings':
                                if pos_neg == 'True':
                                    print("IN TRUE")
                                    for t in survey.thoughts_pos.all():
                                        compareTP.append(t.id)
                                    for f in survey.feelings_pos.all():
                                        compareFP.append(f.id)
                                    for b in survey.behaviors_mc.all():
                                        compareB.append(b.id)

                                    intersectionCountTP = intersection(compareTP, currentListTP)
                                    intersectionCountFP = intersection(compareFP, currentListFP)
                                    intersectionCountB = intersection(compareB, currentListB)
                                    # print(intersectionCount/len(compareTP))

                                    # check for similarity based on metrics of everything being atleast 50% in common
                                    if (len(compareTP) !=0) and (len(compareFP) != 0) and (len(compareB) != 0):
                                        if (intersectionCountTP/len(compareTP) >=0.50) and (intersectionCountFP/len(compareFP) >=0.50) and (intersectionCountB/len(compareB) >=0.50):
                                            allSimilarSurveyID.append(survey.id)
                                            similarSurvey = str(survey.id)
                                    elif ((len(compareTP) == 0 and len(currentListTP) == 0 )  or (len(compareFP) == 0 and len(currentListFP) == 0 )  or (len(compareB) == 0 and len(currentListB) == 0)):
                                        allSimilarSurveyID.append(survey.id)
                                        similarSurvey = str(survey.id)
                                    compareTP = []
                                    compareFP = []
                                    compareB = []
                        if unique_survey.situation == 'Mostly negative feelings':
                            if survey.situation == 'Mostly negative feelings':
                       #if surbey that were searching through all surveys is negative collect data here
                                if pos_neg == 'False':
                                    print("IN FALSE")
                                    for t in survey.thoughts_neg.all():
                                        compareTN.append(t.id)
                                    for f in survey.feelings_neg.all():
                                        compareFN.append(f.id)
                                    for b in survey.behaviors_mc.all():
                                        compareB.append(b.id)

                                    intersectionCountTN = intersection(compareTN, currentListTN)
                                    intersectionCountFN = intersection(compareFN, currentListFN)
                                    intersectionCountB = intersection(compareB, currentListB)

                                    # check for similarity based on metrics of everything being atleast 50% in common
                                    if (len(compareTN) !=0) and (len(compareFN) != 0) and (len(compareB) != 0):
                                        if (intersectionCountTN/len(compareTN) >=0.50) and (intersectionCountFN/len(compareFN) >=0.50) and (intersectionCountB/len(compareB) >=0.50):
                                            allSimilarSurveyID.append(survey.id)
                                            similarSurvey = str(survey.id)
                                    elif ((len(compareTN) == 0 and len(currentListTN) == 0 )  or (len(compareFN) == 0 and len(currentListFN) == 0 )  or (len(compareB) == 0 and len(currentListB) == 0)):
                                        allSimilarSurveyID.append(survey.id)
                                        similarSurvey = str(survey.id)
                                    compareTN = []
                                    compareFN = []
                                    compareB = []
            # if there are no similar surveys initialize similar survey string to -1
            if similarSurvey == "":
                similarSurvey = "-1"

            # convert the similar survey list to a string to pass it into sorting route
            convertSTR = convertList(allSimilarSurveyID)
            print("similar survey", similarSurvey)
           
            
        return redirect(url_for('routes.sorting', survey_id = unique_survey.id, pos_neg=pos_neg, back='0', similarSurvey = similarSurvey, allSimilarList = convertSTR))
       
    return render_template('behavior.html', form=behaviorForm, pos_neg=pos_neg, back='0', survey_id=survey_id)

@bp_routes.route('/sorting/<survey_id>/<pos_neg>/<back>/<similarSurvey>/<allSimilarList>', methods=['GET', 'POST'])
@login_required
def sorting(survey_id, pos_neg,back, similarSurvey, allSimilarList ):
    test = Survey()
    unique_survey=Survey.query.filter_by(id=survey_id).first()
    allUserSignatures = Signature.query.filter_by(user_id = current_user.id).all()
    sign = []
    for s in allUserSignatures:
        surveyTemp = Survey.query.filter_by(signature_id = s.id).all()
        for t in surveyTemp:
        # print(surveyTemp)
            if t.situation == "Mostly positive feelings" and pos_neg == "True":
                if s.ifThen not in sign:
                    sign.append(s.ifThen)
            if t.situation == "Mostly negative feelings" and pos_neg == "False":
                if s.ifThen not in sign:
                    sign.append(s.ifThen)
    print("sign::")
    print(sign)
    
    sortform2 = SortingForm2()
    sortingForm = SortingForm()
    anotherthing = Signature()
    total = []
    result = []
    print("similar survey num", similarSurvey)
    if int(similarSurvey) > 0:
        # test is a survey it gets the first similar survey to the current survey from the database returns Survey x
        # some surveys do not have a signature id
        test = Survey.query.filter_by(id=int(similarSurvey)).first()
        print("test", test)
        print("test signature id", test.signature_id)
        # another thing is a signature
        # it is getting the signature of test - which is the similar survey
        anotherthing = Signature.query.filter_by(id = test.signature_id).first()
        print("anotherthing", anotherthing)

        if(anotherthing):
            totalSit = SituationList.query.filter_by(signature_id = anotherthing.id).all()
        
            total = []
            
            print("total sit", totalSit)
            for t in totalSit:
                total.append(t)
      
        allID = convertString(allSimilarList)

        allSimilarSurvey = []
        result = []
        # add all the similar survey's signature id's into allSimilarSurvey list
        for id in allID:
            temp = Survey.query.filter_by(id=int(id)).first()
            if temp.signature_id not in allSimilarSurvey:
                allSimilarSurvey.append( temp.signature_id)
        print("all simialar survey ", allSimilarSurvey)
        # remove the current similar id from the list
        if(anotherthing):
            if anotherthing.id in allSimilarSurvey:
                allSimilarSurvey.remove(anotherthing.id)
            print("all similar survey", allSimilarSurvey)

        # get all the actuall if then signature fromthe common surveys
        # for t in allSimilarSurvey:
        #     temp = Signature.query.filter_by(id = t).first()
        #     result.append(temp.ifThen)
        #     if temp.ifThen in sign:
        #         sign.remove(temp.ifThen)
        for t in allSimilarSurvey:
            temp = Signature.query.filter_by(id=t).first()
            if temp is not None:
                result.append(temp.ifThen)
                if temp.ifThen in sign:
                    sign.remove(temp.ifThen)
      
        
        if sortingForm.validate_on_submit():
        
            if sortingForm.choice.data == 'True':
                if  int(similarSurvey) > 0:
                    # get the similar survey
                    test = Survey.query.filter_by(id=int(similarSurvey)).first()
                    # get the if then signature for that survey
                    anotherthing = Signature.query.filter_by(id = test.signature_id).first()
                    # print("check Pont")
                    print(anotherthing)
                    # set the signature to the current survey and add the situation to the situation list table
                    unique_survey.signature_id = anotherthing.id
                    newSituation = SituationList(signature_id = anotherthing.id, situation = unique_survey.what_happened)
                    db.session.add(newSituation)
                    db.session.commit()
                    
            else:
                option = request.form.getlist('options')
                option2 = request.form.getlist('options2')
                if(len(option) > 0 and len(option2)> 0):
                    flash("Please choose from one either the similar signatures OR all signatures section")
                    return redirect(url_for('routes.sorting', survey_id = survey_id, pos_neg=pos_neg, back='0', similarSurvey = similarSurvey, allSimilarList = allSimilarList))
                elif(len(option2) > 1):
                    flash("please only choose one option")
                    return redirect(url_for('routes.sorting', survey_id = survey_id, pos_neg=pos_neg, back='0', similarSurvey = similarSurvey, allSimilarList = allSimilarList))
                elif len(option2) == 1:
                    getIfThen = Signature.query.filter_by(ifThen = option2[0]).first()
                    print(getIfThen)
                    unique_survey.signature_id = getIfThen.id
                    newSituation = SituationList(signature_id = getIfThen.id, situation = unique_survey.what_happened)
                    db.session.add(newSituation)
                    db.session.commit()
                # flash message if user chose more than one similar survey
                elif len(option) > 1:
                    flash("please only choose one option")
                    return redirect(url_for('routes.sorting', survey_id = survey_id, pos_neg=pos_neg, back='0', similarSurvey = similarSurvey, allSimilarList = allSimilarList))
                # user choice one of the other similar surveys provided to them
                elif len(option) == 1:
                    getIfThen = Signature.query.filter_by(ifThen = option[0]).first()
                    unique_survey.signature_id = getIfThen.id
                    newSituation = SituationList(signature_id = getIfThen.id, situation = unique_survey.what_happened)
                    db.session.add(newSituation)
                    db.session.commit()
                # user entered in a new category
                else:
                    input = sortingForm.newCategory.data
            
                    newIfthen = Signature(ifThen = input, user_id = current_user.id)
                    db.session.add(newIfthen)
                    db.session.commit()
                    unique_survey.signature_id = newIfthen.id
                    newSituation = SituationList(signature_id = newIfthen.id, situation = unique_survey.what_happened)
                    db.session.add(newSituation)
                    db.session.commit()
                    
                    
            return redirect(url_for('routes.index'))
    elif int(similarSurvey) == -1:
        # sortform2 = SortingForm2()
        if sortform2.validate_on_submit():
            option2 = request.form.getlist('options2')
            if(len(option2) > 1):
                flash("please only choose one option")
                return redirect(url_for('routes.sorting', survey_id = survey_id, pos_neg=pos_neg, back='0', similarSurvey = similarSurvey, allSimilarList = allSimilarList))
            elif len(option2) == 1:
                getIfThen = Signature.query.filter_by(ifThen = option2[0]).first()
                unique_survey.signature_id = getIfThen.id
                newSituation = SituationList(signature_id = getIfThen.id, situation = unique_survey.what_happened)
                db.session.add(newSituation)
                db.session.commit()
            elif len(option2) == 0:
                input = sortform2.newCategory.data

                newIfthen = Signature(ifThen = input, user_id = current_user.id)
                db.session.add(newIfthen)
                db.session.commit()

                unique_survey.signature_id = newIfthen.id
                newSituation = SituationList(signature_id = newIfthen.id, situation = unique_survey.what_happened)
                db.session.add(newSituation)
                db.session.commit()

            return redirect(url_for('routes.index'))
    return render_template('sorting.html', similarSurvey = similarSurvey, form=sortingForm, pos_neg=pos_neg, back='0', survey_id=survey_id, id =anotherthing.ifThen, situationlist = total, 
                           allSimilar = result, form2 =sortform2, allUserSignatures = sign)


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



