import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), 'app/report_generator'))
from datetime import time

from fpdf import FPDF

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from app.report_generator import Graph_Generator
from app.report_generator import PDF_Generator
from app.report_generator import Data_Pruner
from app.report_generator import automated_responses
from app.report_generator import Results_Sorted

import time
import requests
from app.report_generator.PDF_Generator import CustomPDF

# email stuff
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

current_directory = os.path.dirname(os.path.abspath(__file__))

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

mail_content = '''Hello,
Your Person in Context Assessment (PICA) results are attached below.
Thank You
'''
# end email stuff

WIDTH = 210
HEIGHT = 297

# need to start the python anywhere console
# username = 'WSUPsych'
# token = 'b19849a8c15e16119580e813c9a1bdc2b9985e5b'
# host = 'www.pythonanywhere.com'


# API endpoint for starting the console
# CONSOLE_START_URL = f'https://{host}/api/v0/user/{username}/consoles/33319540/start/'

def create_report(csv_file_path):
    # time.sleep(10)
    print('----------------------------------------')

    #number+1 to get total      currently at:tc
    for i in range (1, 2): # 1, 2 makes sure that the idxS ends up being -1 to get the last row
        #.get_survey(save_survey = "", survey_id = 'SV_3wvBtxhaQcsl06G')
        # pdf = FPDF()
        pdf = CustomPDF()
        # setting my path as everything leading up to current directory
        my_path = os.path.join(current_directory, 'static', 'images')

        # saving the most recent survey result from csv data into pandas df
        df = Graph_Generator.pd.read_csv(csv_file_path)
        idxS = 0 - i
        #print(f"Index for current survey (idxS): {idxS}")  # Debug idxS

        currentSurvey = df.iloc[idxS]
        #print(f"Row at idxS ({idxS}):\n{currentSurvey}")  # Debug the retrieved data

        #print("current survey: ", currentSurvey)
        print('----------------------------------------')
        print('Data Retrieved')
        data = Data_Pruner.get_data(csv_file_path, idxS)
        #print("Pruned data:", data)

        # Add title page
        print('----------------------------------------')
        print('Added Title Page')
        title_page(my_path, pdf, data['Personal'])

        #Temperament
        print('----------------------------------------')
        print('Added Temperament Graph')
        stuff = [list(data['Temperament'].values()), list(data['Temperament'].keys())]
        temperament_graph(my_path, pdf, stuff, "Temperament")

        #Self-Concept: Psychological Needs
        print('----------------------------------------')
        print('Added RSSM Graphs')
        rssmTitles = ["Relatedness Satisfaction", "Control Satisfaction", "Self-Esteem Frustration", "Autonomy Frustration"]
        barTitles = [f'Self-with-{v}' if v != 'Overall' else v for k,v in data['RSSMNames'].items()]
        rssm_bar_graphs(my_path, pdf, data['RSSM'], barTitles, rssmTitles)

        #Self-Concept: Rejection Sensitivity
        print('----------------------------------------')
        print('Added Rejection Sensitivity')
        rs_page(pdf, data['RejectionSensitivity'])

        #Self-Concept: Problematic Interpersonal Styles
        print('----------------------------------------')
        print('Added CSIP Graph')
        csipTitles = ["Domineering", "Self-Centered", "Distant/Cold", "Socially Inhibited", "Nonassertive", "Exploitable", "Self-Sacrificing", "Intrusive"]
        csip_bar_graphs(my_path, pdf, data['RadarRSSM'], barTitles, csipTitles)


        #Personal Goals and Standards
        goalTitles = ["Goal Thinking", "Goal Satisfaction", "Goal Self-Efficacy", "Goal Intrinsic Motivation", "Goal Approach Orientation", "Goal Growth Mindset", "Goal Level of Conflict"]

        standardTitles = ["Moral Standard Thinking", "Moral Standard Satisfaction", "Moral Standard Self-Efficacy", "Moral Standard Intrinsic Motivation", "Moral Standard Approach Orientation",
                        "Moral Standard Growth Mindset", "Moral Standard Level of Conflict"]
        #Personal Goals and Standards
        print('----------------------------------------')
        print('Added Goal Graphs')
        # begin adding goals section of the pdf
        goals_bar_graphs(my_path, pdf, data['Goals'], data['GoalDescription'], goalTitles)

        # Comparison figure----Personal Values
        print('----------------------------------------')
        print('Added Comparison Figure')
        PDF_Generator.comparison_figure(pdf, my_path, data['Comparison'], data['GoalDescription'])



        ''' #TODO: fix issues with fig.savefig(path + "/images/radar.png", transparent=False)
        print('----------------------------------------')
        print('Added Radar Plot')
        # add page and begin adding the radar plot
        pdf.add_page()
        PDF_Generator.section_headers(pdf, 'Relational Schema Interpersonal Behavior Scale')
        Graph_Generator.create_radar(pdf, my_path, data['RadarRSSM'], data['RadarRSSMName']) # TODO: last 2 parameters need to be the vector values from pandas df
        '''


        print('----------------------------------------')
        print('Added sorting of results')
        order = ""
        order = Results_Sorted.get_sort(data)
        # commented out line below to get rid of treatment recommendations
        # PDF_Generator.add_sort(pdf, order)

        print('----------------------------------------')
        print('PDF Saved')
        pdf.output('Personalized_report.pdf', 'F')


        print('----------------------------------------')
        user_email = data['Personal']['Email']
        print(f"Extracted email: {user_email}")
        send_mail(user_email)
        print('----------------------------------------')

        #send_mail('walter.scott@wsu.edu')
        #send_mail('chujiaming888@gmail.com')
        #send_mail('belinda.lin@wsu.edu')
        #send_mail('mananganchristian863@gmail.com')
        #send_mail('aquamarinefox.365@gmail.com')

        plt.close('all')

def title_page(my_path, pdf, info):
    pdf.add_page()
    ensure_directory_exists(os.path.join(current_directory, 'static', 'images'))

    pdf.skip_page_number = True  # 跳过标题页的页码
    pdf.image(os.path.join(current_directory, 'static', 'images', 'wsu_banner.png'), 0, 0, WIDTH)
    pdf.image(os.path.join(current_directory, 'static', 'images', 'buffer.png'), 0, HEIGHT / 2 + 1, WIDTH)
    PDF_Generator.add_name(pdf, 'For: {}'.format(info['First']))
    pdf.skip_page_number = False  # 恢复页码显示功能

def rs_page(pdf, rs):
    pdf.add_page()
    total = "Your Self-Concept: Rejection Sensitivity Score was: " + str(round(rs, 2))

    if rs <= 1.39:
        total += " (Very Low)"
    elif rs <= 5:
        total += " (Low)"
    elif rs <= 6.805:
        total += " (Moderately Low)"
    elif rs <= 10.415:
        total += " (Average)"
    elif rs <= 12.22:
        total += " (Moderately High)"
    elif rs <= 15.85:
        total += " (High)"
    else:
        total += " (Very High)"

    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 5, "Self-Concept: Rejection Sensitivity", border=0, align="C")

    intro_text =("     Rejection Sensitivity refers to a tendency to have intense emotional reactions to perceived rejection, whether it is actual or not.")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0,5, intro_text, border=0, align="L")
    pdf.ln(1)

    rejection_sen_text1 = ("     People with high rejection sensitivity have greater concerns about social rejection than most people. They tend to worry excessively about social interactions and what others might think of them. This often leads to misinterpretation of social cues and problems interacting with others due to misinterpretation. In addition, they tend to have extreme anxiety in social situations and a tendency to avoid many social situations due to discomfort or suffer through the situations with high anxiety.")
    pdf.multi_cell(0, 5, rejection_sen_text1, border=0, align="L")
    pdf.ln(1)

    rejection_sen_text2 = ("     High rejection sensitivity may be due to a history of being rejected, or perceiving that one is being rejected. And it can also be reflective or a negative self-concept or an anxious temperament (i.e., high behavioral inhibition).  ")
    pdf.multi_cell(0, 5, rejection_sen_text2, border=0, align="L")
    pdf.ln(1)

    rejection_sen_text3 = ("     People with low rejection sensitivity are not as concerned about social rejection or about how people may think of them or react to them. They do not worry about rejection and tend to believe that others will be receptive towards them and unlikely to reject their requests. They tend to have social confidence.")
    pdf.multi_cell(0, 5, rejection_sen_text3, border=0, align="L")
    pdf.ln(1)

    rejection_sen_text4 = ("     Low rejection sensitivity may be due to a history of being accepted by others, or perceiving that one is being accepted. And it can also be reflective of a positive self-concept or a low anxious temperament (i.e., low behavioral inhibition) and/or a high approach temperament (i.e., high behavioral activation).")
    pdf.multi_cell(0, 5, rejection_sen_text4, border=0, align="L")

    pdf.ln(3)
    pdf.set_font('Arial', 'B', 14)
    pdf.multi_cell(0, 5, total, border=0, align="L")

def generate_goal_feedback(scores, labels, current_title, is_overall=False):
    # Define explanation feedback for different titles
    feedback_templates = {
        "Goal Thinking": {
        "high": "     Your overall goal thinking score indicates that you are thinking about your goals often, that your goals are important to you and that you are committed to making them goal happen. Goals are more motivating, more likely to lead to effective action, when they are on our mind, when we are thinking about them frequently.",
        "average": "     Although you did not score low in thinking about your goals, you still might benefit from considering ways to increase your awareness of your goals if you believe they are worth pursuing. You might write your goals out and place them somewhere you will see them often (e.g., refrigerator, desk). You might also think of situations that you encounter in your life which present opportunities to act on your goals, associating those situations in your mind with your goal.",
        "low": "     Your score indicates that you don't think that much about your goals. Goals are more motivating, more likely to lead to effective action, when we are thinking about them often.  If you are not thinking of your goals, it is less likely that these goals will come to mind in situations where you might act on them, and you may feel less committed to your goals.\n     Consider ways to increase your awareness of your goals if you believe they are worth pursuing. You might write your goals out and place them somewhere you will see your goals often (e.g., refrigerator, desk). You might also think of situations that you encounter in your life which present opportunities to act on your goals, associating those situations in your mind with your goal."
        },
        "Goal Satisfaction": {
        "high": "     Your overall goal satisfaction score indicates that you are satisfied with your current level of progress in making your goals happen. Feeling good about your progress toward your goals builds your self efficacy, feels rewarding, and can fuel your motivation to continue goal pursuit and, in some cases, adopt even more challenging goals.",
        "average": "     Your overall goal satisfaction score indicates that you are neither particularly dissatisfied or satisfied with your current level of progress in making your goals happen. It might be helpful to think of specific actions that you can perform today or tomorrow, even if for only a few minutes, that will likely give you a sense of satisfaction in moving you closer to one of your most important goals.  Feeling good about your progress toward your goals builds your self efficacy, feels rewarding, and can fuel your motivation to continue goal pursuit and, in some cases, adopt even more challenging goals.",
        "low": "     Your overall goal satisfaction score indicates that you are generally dissatisfied with your current level of progress in making your goals happen. It might be helpful to think of specific actions that you can perform today or tomorrow, even if for only a few minutes, that will likely give you a sense of satisfaction in moving you closer to one of your most important goals.  Feeling good about your progress toward your goals builds your self efficacy, feels rewarding, and can fuel your motivation to continue goal pursuit and, in some cases, adopt even more challenging goals."
        },
        "Goal Self-Efficacy": {
        "high": "     Your overall goal self efficacy score indicates that you are confident in your ability to perform the activities/behaviors that lead to your goals. Humans don't just act; they reflect on their abilities to act. Self efficacy refers to how confident you are that you can perform a specific action.\n     If you have high goal self efficacy, and are confident in your ability to perform the actions that will lead to your goals, you are more likely to seek out situations and challenges that move you closer to your goals. You will be more motivated to persist in actions that lead to your goals, which is important because most goals worth pursuing involve setbacks and challenges that require persistence. All of these things can make attaining your goals more likely.",
        "average": "     Your overall goal self efficacy score indicates that you are not certain about your abilities to perform the activities/behaviors that lead to your goals. Self efficacy refers to how confident you are that you can perform a specific action.\n     As a result of not having strong confidence in your ability to perform goal related behaviors, your motivation for pursuing your goals may be low. Research suggests that when you lack strong confidence in your ability to perform the actions required to make your goal happen you may be less likely to seek out situations that might move you closer to your goals. You may be less motivated to persist in actions that lead to your goals, which is important because most goals worth pursuing involve setbacks and challenges that require persistence. Finally, you may be more prone to feeling anxious and/or depressed. All of these things can make attaining your goals less likely.\n     It might be helpful to get more specific about actions you do believe you can perform that might move you a little closer to your goal. You could create a goal ladder, with the first rungs describing specific behaviors you can do right now to move you closer to your goal, with later rungs describing specific behaviors for the more distant future. This may make your goal seem a little less challenging. By breaking your large goal down and focusing your thinking on the smaller, more specific goals, that lead to your larger goal, you are likely to feel more confident, have higher self efficacy, about making the big goal happen.\n     Sometimes the problem isn't with the goals themselves but rather that you think too lowly of your abilities. This can happen for a number of different reasons. For instance, if you also had a high BIS temperament, and are more prone to feeling anxious, this can lead to a sort of emotional reasoning.  In a sense, your anxious feelings are fooling you: \"I feel anxious, therefore I must not be capable of performing this behavior\" or \"I feel anxious so that means I won't be able to make my goal happen.\"\n     Other times a negative self concept, which may have been established at an early age but is no longer accurate, can lead to underestimating your true ability. In these cases, it might help to reflect on past situations in which you successfully performed behaviors similar to those required by your goals. By thinking of these past successes, you can feel more confident, more efficacious, and this should promote better motivation and goal success.",
        "low": "     Your overall goal self efficacy score indicates that you doubt your abilities to perform the activities/behaviors that lead to your goals. Self efficacy refers to how confident you are that you can perform a specific action. As a result of not having strong confidence in your ability to perform goal related behaviors, your motivation for pursuing your goals may be low. Research suggests that when you lack strong confidence in your ability to perform actions required for your goals you may be less likely to seek out situations that might move you closer to your goals. You may be less motivated to persist in actions that lead to your goals, which is important because most goals worth pursuing involve setbacks and challenges that require persistence. Finally, you may be more prone to feeling anxious and/or depressed. All of these things can make attaining your goals less likely.\n     It might be helpful to get more specific about actions you do believe you can perform that might move you a little closer to your goal. You could create a goal ladder, with the first rungs describing specific behaviors you can do right now to move you closer to your goal, with later rungs describing specific behaviors for the more distant future. This may make your goal seem a little less challenging. By breaking your large goal down and focusing your thinking on the smaller, more specific goals, that lead to your larger goal, you are likely to feel more confident, have higher self efficacy, about making the big goal happen.\n     Sometimes the problem isn't with the goals themselves but rather that you think too lowly of your abilities. This can happen for different reasons. For instance, if you also had a high BIS temperament, and are more prone to feeling anxious, this can lead to a sort of emotional reasoning.  In a sense, your anxious feelings are fooling you: \"I feel anxious, therefore I must not be capable of performing this behavior\" or \"I feel anxious so that means I won't be able to make my goal happen.\"\n     Other times a negative self concept, which may have been established at an early age but is no longer accurate, can lead to underestimating your true ability. In these cases, it might help to reflect on past situations in which you successfully performed behaviors similar to those required by your goals. By thinking of these past successes, you can feel more confident, more efficacious, and this should promote better motivation and goal success."
        },
        "Goal Intrinsic Motivation": {
        "high": "     Your overall goal intrinsic motivation score indicates that you think of your goals as intrinsically motivated. You see this goal as coming from you, as chosen because of your own values, interests, likes and dislikes.\n     This is good. Research has shown that, in general, intrinsically motivated goals are more adaptive, as they seem more likely to meet basic human needs for competence, relatedness, and autonomy, and are associated with higher levels of psychological well being.",
        "average": "     Your overall goal intrinsic motivation score indicates one of two things: 1) you think of your goals as both extrinsically and intrinsically motivated, or 2) you really don't think of your goals either as extrinsically or intrinsically motivated.\n     Extrinsically motivated goals are those you feel you are supposed do, perhaps in order to get something else you want. These are goals pursued for some external reason. In contrast, another way of thinking about goals is as intrinsically motivated goals, pursuing the goal for sake of the goal itself, because you find the goal related activities interesting, fun, and pleasant.\n     Research has shown that, although sometimes necessary, extrinsically motivated goals are, in general, less adaptive.  Typically, intrinsically motivated goals are more optimal, tend to more directly meet basic human needs for competence, relatedness, and autonomy, and are associated with higher levels of psychological well being. \n     It might be good to rethink your goals, and the activities related to your goals, so you see them as coming from you, as chosen by you because of your own values, interests, likes and dislikes.\n     It may be that your goals are not in and of themselves intrinsically motivated, but are instead related to larger goals you have that are intrinsically motivated. That's ok. In that case, it might be good to remind yourself of your larger goals (My goal to run is extrinsically motivated but it is part of a larger, intrinsically motivated, goal to become and feel healthier).",
        "low": "     Your overall goal intrinsic motivation score indicates that you tend to think about the activities related to your goals as extrinsically motivated, which means you think of them as things that you have to do, are supposed do, perhaps in order to get something else you want. You are pursuing your goals for some external reason.  In contrast, another way of thinking about your goals would be as intrinsically motivated goals, pursuing the goal for sake of the goal itself, because you find the goal related activities interesting, fun, and pleasant.\n     Research has shown that, although sometimes necessary, extrinsically motivated goals are, in general, less adaptive. It might be good to rethink your goals, and the activities related to your goals, so you see them as coming from you, as chosen by you because of your own values, interests, likes and dislikes. It is possible that your 'extrinsically motivated' goals are related to larger goals that are more intrinsically motivated.  In that case, it might be good when engaged in your 'extrinsically motivated' goals to remind yourself of the larger goals your extrinsically motivated goals are related to (My goal to run is extrinsically motivated but it is part of a larger, intrinsically motivated, goal to become and feel healthier)."
        },
        "Goal Approach Orientation": {
        "high": "     Your overall goal approach orientation score indicates that you tend to think of your goals as approach goals.  Research has shown that this is generally a good way to think about one's goals.\n     Approach goals are goals that we want to approach, obtain, get. In contrast, avoidance goals are those that we want to avoid, escape, prevent from happening. For instance, two people may have the same goal of wanting to lose weight. However, one of them thinks about this goal as something to avoid (avoid gaining weight) whereas the other person tends to frame it as something to approach (approach getting slimmer).\n     In short, you are thinking about your goals in way that appears most adaptive and most likely to make your goals happen.",
        "average": "     Your overall goal approach orientation score indicates one of two things: 1) you think of your goals with both an approach and an avoidance mindset, or 2) you don't think of your goals with either an approach or avoidance mindset. Avoidance goals are those that we want to avoid, escape, prevent from happening. Approach goals are goals that we want to approach, obtain, get. Research has shown that, in general, a better way to think about your goals is to think or frame them in your mind as approach goals.\n     You can change your thinking about your goals so that you think of them more as approach goals. For instance, two people may have the same goal of wanting to lose weight. However, one of them thinks about this goal as something to avoid (avoid gaining weight) whereas the other person tends to frame it as something to approach (approach getting slimmer).\n     Consider ways of rethinking your goals so that you can think of them as something positive you want to approach.",
        "low": "     Your overall goal approach orientation score indicates that you think of your goals as things you want to avoid, escape, prevent from happening. We call these avoidance goals. Research has shown that, in general, avoidance goals are not the best way to think about what you are trying to do. Instead, a better way to think about your goals is to rethink or reframe them as approach goals. Approach goals are goals that we want to approach, obtain, get.\n     You can change your thinking about your goals so that you think of them more as approach goals. For instance, two people may have the same goal of wanting to lose weight. However, one of them thinks about this goal as something to avoid (avoid gaining weight) whereas the other person tends to frame it as something to approach (approach getting slimmer).\n     Consider ways of rethinking your goals so that you can think of them as something positive you want to approach."
        },
        "Goal Growth Mindset": {
        "high": "     Your score indicates that you tend to think of your goals with a growth mindset, that is as opportunities to further develop your abilities and/or personal characteristics. This is good! In contrast, sometimes people focus on the goals they are pursuing as performance goals, as trying to prove some level of competence/ability or demonstrating some personal characteristic.\n     In general, research has shown that it is better to think of goals with a growth or learning mindset, as opportunities to improve, get better, as opposed to trying to demonstrate some already existing quality or ability level.\n     In short, it is good that you are thinking of your goals with a growth mindset, as opportunities to improve and further develop.",
        "average": "     Your overall goal growth mindset score indicates one of two things: 1) you think of your goals with both a growth and a performance mindset, or 2) you don't think of your goals with either a growth or a performance mindset. Performance goals are those in which we tend to think of our goal as proving some level of competence/ability or demonstrating some personal characteristic.  In contrast, another way of thinking about your goal would be to think of it with a growth mindset, as an opportunity to improve your level of competence/ability or further develop some characteristic.\n     In general, research has shown that it is better to think of your goals with a growth mindset, as opportunities to improve, get better, as opposed to trying to demonstrate some already existing quality or ability level.",
        "low": "     Your score indicates that you tend to think about your goals as performance goals, which means you think of your goals as trying to prove your level of competence/ability or trying to demonstrate some personal characteristic. In contrast, another way of thinking about your goals would be as a growth goals, thinking of your goals instead as opportunities to improve your level of competence/ability or further develop some personal characteristic.\n     In general, research has shown that it is better to think of your goals with a growth mindset, as opportunities to improve, get better, as opposed to trying to demonstrate some already existing quality or ability level."
        },
        "Goal Level of Conflict": {
        "high": "     Your overall goal level of conflict score indicates that your goals are conflicted. That is, you perceive that making progress on any one goal as interfering with making progress on your other important goals.\n     Research has shown that when our goals are conflicted in this way, it can interfere with making progress on any individual goal. Not only that but people who report high levels of goal conflict also tend to report increased psychological distress and even more physical illness symptoms.\n     We recommend reflecting on your personal values, what is most important to you in living a good life, at this stage of your life, and prioritize those goals you consider most important for where you are right now. If this goal is consistent with your values, and is important at this stage of your life, you might consider temporarily delaying the pursuit of other goals to minimize goal conflict. Alternatively, consider whether there is a way of thinking about this goal that minimizes its interference with your other goals.",
        "average": "     Your overall goal level of conflict score indicates that progress on any one goal neither interferes nor facilitates with making progress on your other goals.\n     It is good that you perceive that making progress on this goal does not conflict with making progress on your other goals.  Research has shown that when our goals are conflicted--when making progress on one goal is perceived as interfering with making progress on other important goals--it can interfere with making progress on any individual goal.  Not only that but people who report higher levels of goal conflict also tend to report increased psychological distress and even more physical illness symptoms.",
        "low": "     Your overall goal level of conflict score indicates that progress on any one of your goals generally helps with making progress on your other goals.\n     It is good that you perceive that making progress on any of your goals does not conflict with making progress on your other goals. Research has shown that when our goals are conflicted--when making progress on one goal is perceived as interfering with making progress on other important goals--it can interfere with making progress on any individual goal. Not only that but people who report higher levels of goal conflict also tend to report increased psychological distress and even more physical illness symptoms."
    }
    }

    # Define verbal descriptors based on score bounds
    def get_descriptor(score):
        score = float(score)
        if score >= 6.0:
            return "very high"
        elif score >= 5.0:
            return "high"
        elif score >= 3.0:
            return "average"
        elif score >= 2.0:
            return "low"
        else:
            return "very low"

    lowercase_title = current_title.lower()
    overview_paragraph = (
        f"Our {lowercase_title} can vary depending upon the specific goal involved. "
        f"Your scores below indicate how your {lowercase_title} varies for each of the four goals you identified on this measure."
    )

    # Choose the right feedback template
    feedback = f"{current_title}:\n"
    template = feedback_templates.get(current_title, None)

    if not template:
        return feedback  # If no suitable template is found, an empty response is returned.

    # If it is the Overall score, generate explanatory feedback
    if is_overall:
        score = float(scores[0])  # Assume the first one is the Overall score
        score = round(score, 2) # round to two places
        if score >= 6.0:
            feedback += f"Overall score is {score} (very high):\n{template['high']}\n"
        elif score >= 5.0:
            feedback += f"Overall score is {score} (high):\n{template['high']}\n"
        elif score >= 3.0:
            feedback += f"Overall score is {score} (average):\n{template['average']}\n"
        elif score >= 2.0:
            feedback += f"Overall score is {score} (low):\n{template['low']}\n"
        else:
            feedback += f"Overall score is {score} (very low):\n{template['low']}\n"

    # Add the overview paragraph
    feedback += f"\n{overview_paragraph}\n"

    # List Individual scores without explanation
    for i, score in enumerate(scores[1:], start=1):  # Skip the first one (Overall)
        label = labels[i]
        descriptor = get_descriptor(score)
        feedback += f"{label} score is {float(score)} ({descriptor})\n"

    return feedback

def add_personal_goals_intro(pdf):
    # Add a new page for the introductory text
    pdf.set_font("Arial", "", 10)

    # First paragraph
    intro_text1 = (
        "     Personal goals are those things we are trying to make happen. Wanting to become a doctor, "
        "finding a partner, losing weight--these all represent future or possible selves, things that we are striving "
        "to make happen for ourselves. Goals can also be undesired future states, such as avoiding being poor, dropping out "
        "of college, or being divorced. Goals also imply personal standards, which are what we consider acceptable, good behaviors in the present. "
        "For instance, the goal of becoming a doctor implies that getting good grades now is an important personal standard. Other "
        "personal standards include our morals, beliefs we have about what is inherently good and bad behavior. Being honest, disciplined, "
        "and polite to others--each of these are examples of moral standards that may guide our behavior."
    )
    pdf.multi_cell(0, 5, intro_text1, border=0, align="L")
    pdf.ln(1)

    # Second paragraph
    intro_text2 = (
        "     Personal goals and standards strongly influence your personality functioning, including the situations you seek out, how you "
        "interpret what happens to you, how motivated you are, and how you feel and act. We compare our current behavior to our goals and "
        "standards, feeling bad if we come up short and feeling good if we have performed successfully. To assess your personal goals and "
        "standards, you completed a modified version of the Personal Concerns Inventory (M-PCI; Cox & Klinger, 2011). Although the M-PCI is "
        "considered a \"goal\" measure, when people complete the M-PCI they tend to list both goals (e.g., graduate college) and standards "
        "(e.g., maintain my good GPA)."
    )
    pdf.multi_cell(0, 5, intro_text2, border=0, align="L")
    pdf.ln(1)

    # Third paragraph
    intro_text3 = (
        "     Research has shown that it is not just what goals and standards you have but how you think about them that matters. For instance, "
        "two people can have the same goal of getting a college degree. But one person is very satisfied with their progress, confident in "
        "being able to get a degree, and thinks about it as something positive to approach (e.g., \"get a college degree\"). Another person "
        "with the same goal may think about it very differently: they are not satisfied with their progress, doubt their ability to get a degree, "
        "and think about it as something negative to avoid (e.g., \"don't get kicked out of college\"). A large body of research shows that how "
        "you think about your goals matters, and influences your psychological well-being as well as the likelihood of goal/standard success."
    )
    pdf.multi_cell(0, 5, intro_text3, border=0, align="L")
    pdf.ln(1)

    # Fourth paragraph
    intro_text4 = (
        "     For your goal/standard scores, we provide interpretations for both your overall goal scores and for your individual goal scores. For any scale, if there "
        "is not much difference in your scores across the four goals-standards you listed, you should just use your overall score. However, if for "
        "any goal/standard score, you see differences across the four goals/standards, then use the individual goal scores to interpret your feedback."
    )
    pdf.multi_cell(0, 5, intro_text4, border=0, align="L")
    pdf.ln(1)

# function to complete the goals section of bar graphs and text boxes
def goals_bar_graphs(my_path, pdf, data, descriptions, titles):
    pdf.add_page()
    PDF_Generator.section_headers(pdf, 'Personal Goals and Standards')
    pdf.ln(4)
    add_personal_goals_intro(pdf)
    #pdf.add_page()
    #PDF_Generator.print_textboxes(pdf, "Goal", descriptions, 4)

    #counter = 0
    # Create a dictionary mapping keys to titles
    title_map = {
        "GoalThink": "Goal Thinking",
        "GoalSatis": "Goal Satisfaction",
        "GoalEfficacy": "Goal Self-Efficacy",
        "GoalIntrinsic": "Goal Intrinsic Motivation",
        "GoalApproach": "Goal Approach Orientation",
        "GoalGrowth": "Goal Growth Mindset",
        "GoalConflict": "Goal Level of Conflict"
    }

    # loop through all the items in the dictionary
    for key, value in data.items():

        if len(value) == 4:
            labels = ["Goal 1", "Goal 2", "Goal 3", "Goal 4"]
        else:
            labels = ["Overall", "Goal 1", "Goal 2", "Goal 3", "Goal 4"]

        # Setting the is_overall variable
        is_overall = labels[0] == "Overall"

        if key[4:] == 'Conflict' or key[4:] == 'Growth':
            holder = 'Goal_{}'.format(key[4:])
        else:
            holder = key[4:]

        # Get the current title according to key
        current_title = title_map.get(key, "Goal")  # If no match is found, the default title is used.
       ############
        # 每个图表和反馈框都在新的一页
        pdf.add_page()
        PDF_Generator.section_headers(pdf, 'Personal Goals and Standards')

        # 显示描述框
        PDF_Generator.print_textboxes(pdf, "Goal", descriptions, 4)

        # 创建图表
        Graph_Generator.create_bargraph(pdf, my_path, 8, value, labels, key, titles.pop(0), descriptions)
        pdf.ln(5)  # Adjust this value as needed

        # 生成反馈并在反馈框中显示
        feedback = generate_goal_feedback(value, labels, current_title, is_overall)
        PDF_Generator.print_feedback_box_horizontal(pdf, feedback, x=10, y=None, w=180,offset_y=30)

        # 添加图表图像
        image_path = os.path.join(my_path, f"{holder}_Scaling.png")
        pdf.image(image_path, 95, 94, (WIDTH / 2) + 10)

# Create and add the text boxes and graphs for the standard graphs
def standard_bar_graphs(my_path, pdf, data, descriptions, titles):
    pdf.add_page()
    PDF_Generator.section_headers(pdf, 'Personal Moral Standards')
    counter = 0
    # loop through all the items in the dictionary
    for key, value in data.items():
        if len(value) == 4:
            labels = ["Moral\nStandard 1", "Moral\nStandard 2", "Moral\nStandard 3", "Moral\nStandard 4"]
        else:
            labels = ["Overall","Moral\nStandard 1", "Moral\nStandard 2", "Moral\nStandard 3", "Moral\nStandard 4"]

        if key[8:] == 'Conflict' or key[8:] == 'Growth':
            holder = 'Moral_{}'.format(key[8:])
        else:
            holder = key[8:]

        # If counter == 2 we need to create a new page
        if counter == 2:
            Graph_Generator.create_bargraph(pdf, my_path, counter*96, value, labels, key, titles.pop(0))
            PDF_Generator.print_textboxes(pdf, "Moral Standard", descriptions, 4)
            image_path = os.path.join(my_path, "static", "images", f"{holder}_Scaling.png")
            pdf.image(image_path, 100, counter * 96 + 86, WIDTH / 2)
            pdf.add_page()
            PDF_Generator.section_headers(pdf, 'Personal Moral Standards')
            counter = 0
        else:
            if counter != 0:
                Graph_Generator.create_bargraph(pdf, my_path, counter*96, value, labels, key, titles.pop(0))
                image_path = os.path.join(my_path, "static", "images", f"{holder}_Scaling.png")
                pdf.image(image_path, 100, counter * 96 + 86, WIDTH / 2)
                counter += 1
            else:
                Graph_Generator.create_bargraph(pdf, my_path, 8, value, labels, key, titles.pop(0))
                image_path = os.path.join(my_path, "static", "images", f"{holder}_Scaling.png")
                pdf.image(image_path, 100, 94, WIDTH / 2)
                counter += 1

    # if counter != 0 then we add new text boxes
    if counter != 0:
        PDF_Generator.print_textboxes(pdf, "Moral Standard", descriptions, 4)

def generate_rssm_feedback(scores, labels, current_title, is_overall=False):
    #Defining an explanatory feedback template
    feedback_templates = {
        "Relatedness Satisfaction": {
            "high": "     Your overall score suggests that in general you experience some features of a positive self-concept. More specifically, this suggests that in general you experience high levels of being connected to, close to, and accepted by the people you most interact with or think about. Some research suggests that feeling connected to others is a basic psychological need and contributes to higher self-esteem and psychological well-being.",
            "average": "     Your overall score suggests that although you do not necessarily experience disconnection or rejection from the people you most interact with or think about, you also do not experience an optimal level of connectedness, relatedness, or acceptance.\n     Some research suggests that feeling connected to others is a basic psychological need. Your score indicates that this need is not being fully met. To increase your levels of relatedness satisfaction, you might reflect on whether you are relating to others in a way that allows for deeper connection and relatedness. Alternatively, you might also reflect on who you choose to spend time and interact with, and deliberately spending time with those people who accept you and with whom you feel close.",
            "low": "     Your overall score suggests that in general you experience some features of a negative self-concept. Specifically, you experience a self that is disconnected from, not close to, and/or rejected by the people you most interact with and/or think about.\n     Some research suggests that feeling connected to others is a basic psychological need. Your score indicates that this need is not being fully met. To increase your levels of relatedness satisfaction, you might reflect on whether you are relating to others in a way that allows for deeper connection and relatedness. Alternatively, you might also reflect on who you choose to spend time and interact with, and deliberately spending time with those people who accept you and with whom you feel close."
        },
        "Control Satisfaction": {
            "high": "     Your overall score suggests that in general you experience some features of a positive self-concept. More specifically, this suggests that in general you experience a self that is in control, engaged, and capable and skilled.  Some research suggests that feeling in control, engaged, and capable is a basic psychological need. Your score indicates that this need is being met. The self tends to experience \"flow,\" an optimal state of control, when it is engaged in challenging activities for which there are learned and developed skills and abilities. It appears you have developed skills and abilities that empower your sense of self.",
            "average": "     Your overall score suggests that although you do not necessarily experience low control, engagement, or capability with others, you also do not experience an optimal level of control and engagement.\n     Some research suggests that feeling in control, engaged, and capable is a basic psychological need. Your score indicates that this need is not being fully met. The self tends to experience \"flow,\" an optimal state of control, when it is engaged in challenging activities for which you have developed some degree of skill and ability. To increase your level of control, you might consider exercising more influence in your relationships with others, being more assertive, and engaging in mutual activities that interest you and for which you feel competent.",
            "low": "     Your overall score suggests that in general you experience some features of a negative self-concept when interacting or thinking about this person. More specifically, this suggests that in general you do not experience a self that is in control, engaged, and capable and skilled.\n     Some research suggests that feeling in control, engaged, and capable is a basic psychological need. Your score indicates that this need is not being fully met. The self tends to experience \"flow,\" an optimal state of control, when it is engaged in challenging activities for which you have developed some degree of skill and ability.\n     To increase your experience of control, you might consider exercising more influence in your relationships with others, being more assertive, and engaging in activities that interest you and enabling you to develop greater competence."
        },
        "Self-Esteem Frustration": {
            "high": "     Your overall score suggests that you possess some features of a negative self-concept. More specifically, this suggests that in general you experience a self that is low in self-esteem. Our self-esteem reflects both our levels of feeling accepted by others and feeling competent. The two go hand-in-hand in contributing to our self-esteem. This is likely because the experience of acceptance leads us to validate our own personal competence, qualities, and abilities.\n     Some research suggests that feeling a high sense of self-esteem is a basic psychological need. Your score indicates that this need is not being met.\n     To increase your level of self-esteem, you might consider whether you are misinterpreting being rejected by others, which might then lead you to question your competence, qualities, or abilities.\n     Further, if in fact you are being rejected by others, does this necessarily mean you do not possess certain abilities and good qualities as a person?",
            "average": "     Your overall score suggests that in general you experience average levels of self-esteem. Our self-esteem reflects both our levels of feeling accepted by others and feeling competent. The two go hand-in-hand in contributing to our self-esteem. This is likely because the experience of acceptance leads us to validate our own personal competence, qualities, and abilities.\n     Your score suggests that although you do not necessarily experience low self-esteem, you also do not experience high self-esteem. Some research suggests that feeling a high sense of self-esteem is a basic psychological need. Your score indicates that this need is not being fully met.\n     To increase your level of self-esteem, you might consider whether you are misinterpreting being rejected by others, which might then lead you to question your competence, qualities, or abilities. Further, if in fact you are being rejected by others, does this necessarily mean that you do not possess certain abilities and good qualities as a person?",
            "low": "     Your overall score suggests that in general your needs for self-esteem are being adequately met and you do not experience self-esteem frustration.\n     Some research suggests that feeling a high sense of self-esteem is a basic psychological need. Research has shown that our self-esteem reflects both our levels of feeling accepted and competent. This is likely because the experience of acceptance by others leads us to validate our own personal competence, abilities, or self-qualities. The two go hand-in-hand in contributing to our self-esteem.\n     Your score suggests that you do experience acceptance and also feel competent in your own abilities with the people you most interact withor think about--therefore your need for self-esteem is being adequately met."
        },
        "Autonomy Frustration": {
            "high": "     Your overall score suggests that you possess some features of a negative self-concept.  More specifically, your score suggests that you often feel as if your actions are externally controlled, coerced or pressured by others, and that you are doing things out of a sense of obligation.\n     Some research suggests that feeling a high sense of autonomy is a basic psychological need. Your score indicates that this need is not being fully met.\n     To decrease levels of autonomy frustration, you might benefit from focusing on what you consider most important, of most value, of most interest, and choose to pursue and engage in those actions, activities, and relationships.",
            "average": "     Your overall score suggests that although you do not experience a high level of autonomy frustration, you also do not experience an optimal level of autonomy.  More specifically, your score suggests that you sometimes feel as if your actions are externally controlled, coerced or pressured by others, and that you are doing things out of a sense of obligation.\n     Some research suggests that feeling a high sense of autonomy-high levels of internal control, freedom, and choice-is a basic psychological need. Your score indicates that this need is not being fully met.\n     To decrease levels of autonomy frustration, you might benefit from focusing on what you consider most important, of most value, of most interest, and choose to pursue and engage in those actions, activities, and relationships.",
            "low": "     Your overall score suggests that in general you do not experience high autonomy frustration, or that your actions are being controlled, coerced or pressured by others, that you are doing things out of a sense of obligation.\n     Some research suggests that feeling a high sense of autonomy-- an optimal level of internal control, freedom, and choice--is a basic psychological need. Your score indicates that this need is being met."
        }
    }

    # Choose the right feedback template
    feedback = f"{current_title}\n"
    template = feedback_templates.get(current_title, None)

    if not template:
        return feedback  # If no suitable template is found, an empty response is returned.

    # If it is the Overall score, generate explanatory feedback
    if is_overall:
        score = float(scores[0])  # Assume the first one is the Overall score
        score = round(score, 2) # round the score to two decimal places
        if score >= 4.5:
            feedback += f"Overall score is {score} (very high):\n{template['high']}\n"
        elif score >= 3.5:
            feedback += f"Overall score is {score} (high):\n{template['high']}\n"
        elif score >= 2.5:
            feedback += f"Overall score is {score} (average):\n{template['average']}\n"
        elif score >= 1.5:
            feedback += f"Overall score is {score} (low):\n{template['low']}\n"
        else:
            feedback += f"Overall score is {score} (very low):\n{template['low']}\n"


    # 添加概述段落
    lowercase_title = current_title.lower()
    feedback += (
        f"     Our experience of {lowercase_title} can vary depending upon the specific other person involved."
        f"Your scores below indicate how your {lowercase_title} varies for each of the four persons you identified on this measure.\n"
    )

    # 横向排列单独分数，并添加括号
    feedback += ""
    #individual_scores = []
    for i, score in enumerate(scores[1:], start=1):  # 跳过第一个总分
        label = labels[i]
        score = round(float(score), 2)
        if score >= 4.5:
            category = "very high"
        elif score >= 3.5:
            category = "high"
        elif score >= 2.5:
            category = "average"
        elif score >= 1.5:
            category = "low"
        else:
            category = "very low"
        #individual_scores.append(f"{label} score is {score} ({category})")
        feedback += f"{label} score is {score} ({category})\n"

    # feedback += "  ".join(individual_scores)
     # Arrange the scores in pairs
    #paired_scores = []
    #for i in range(0, len(individual_scores), 2):
        #if i + 1 < len(individual_scores):
            #paired_scores.append(f"{individual_scores[i]}  {individual_scores[i + 1]}")
        #else:
            #paired_scores.append(individual_scores[i])  # Handle last remaining single score

    #feedback += "\n".join(paired_scores)
    return feedback

# Create and add rssm bar graphs
def rssm_bar_graphs(my_path, pdf, data, names, titles):
    #initial_y_position = 30  # Sets the initial Y position of the box
    pdf.add_page()
    PDF_Generator.section_headers(pdf, 'Self-Concept: Psychological Needs When with Significant Others')
    pdf.ln(4)

    # Introductory text for this section
    pdf.set_font("Arial", "", 10)
    intro_text = (
        "     The second personality structure we assessed was your self-concept--these are beliefs you "
        "possess about who you are, your qualities, needs, and experiences. Our self-concept influences how we perceive "
        "ourselves, interpret the actions of others, feel and behave, and are a major part of your personality."
    )
    pdf.multi_cell(0, 5, intro_text, border=0, align="L")
    pdf.ln(1)

    rssm_text_contin = (
        "     Rather than a single self-concept, research has shown that we have multiple self-concepts. These different \"selves\" "
        "emerge from, and are tied to, our interactions with significant others. That is, many people experience the self differently "
        "when with different others (e.g., self-with-mom, self-with-friend)."
    )
    pdf.multi_cell(0, 5, rssm_text_contin, border=0, align="L")
    pdf.ln(1)

    rssm_text_contin2 = (
        "     To assess your self-concepts, you completed the Relational Self-Schema Questionnaire (RSSM; Scott et al., 2021), which "
        "had you rate how you experience the self and act when with the four people you interact with and/or think about the most. "
        "Some research suggests that our self-experience is organized around the satisfaction of basic psychological needs, such as "
        "the need to feel connected to others, to feel competent/in control, and to have a sense of self-esteem. The RSSM assesses "
        "the experience of these needs when the self is with different significant others."
    )
    pdf.multi_cell(0, 5, rssm_text_contin2, border=0, align="L")
    pdf.ln(5)

    title_map = {
        "RssmRelateSatis": "Relatedness Satisfaction",
        "RssmControlSatis": "Control Satisfaction",
        "RssmEsteemFrus": "Self-Esteem Frustration",
        "RssmAutoFrus": "Autonomy Frustration"
    }

    initial_y_position = pdf.get_y()  # Get the initial Y coordinate
    graph_x_position = 10  # X coordinate of the chart
    total_height = 130  # Total height of each chart and text explanation (chart + text)
    feedback_box_width = pdf.w - 20

    counter = 0  # Used to record chart counts
    data_copy = data.copy()  # Preventing original data from being modified
    is_first_page = True  # Used to mark whether the first page has been processed

    for key, value in data_copy.items():
        #print(f"Processing key: {key}")  # 添加打印语句
        current_title = title_map.get(key, "RSSM Scale")  # Get the current title from the title list
        labels = names

        ####################
        if is_first_page:
            # Special treatment for the first page: only one chart is displayed
            graph_y_position = initial_y_position
            feedback_y_position = graph_y_position + 80

            # Create RSSM chart
            Graph_Generator.create_rssm_bargraph(pdf, my_path, graph_y_position, value, names, key, current_title)
            image_path = os.path.join(my_path, "RSSM_Scaling.png")
            pdf.image(image_path, graph_x_position + 20, graph_y_position + 71, WIDTH / 2 - 30, 5)

            # Display explanation text
            feedback = generate_rssm_feedback(value, labels, current_title, is_overall=True)
            PDF_Generator.print_feedback_box(pdf, feedback, x=10, y=feedback_y_position, w=feedback_box_width, font_size=9)

            # Mark the first page processing completed
            is_first_page = False

            # Add a new page and prepare to process subsequent content
            pdf.add_page()
            PDF_Generator.section_headers(pdf, 'Self-Concept: Psychological Needs When with Significant Others')
            initial_y_position = pdf.get_y()  # Update initial Y coordinate
            counter = 0  # Reset Counter

            # Skip the subsequent logic and enter the next loop
            continue


        # From the second page onwards: a maximum of two charts can be placed per page
        graph_y_position = initial_y_position + (counter * total_height)
        feedback_y_position = graph_y_position + 75

        # RSSM
        Graph_Generator.create_rssm_bargraph(pdf, my_path, graph_y_position, value, names, key, current_title)
        image_path = os.path.join(my_path, "RSSM_Scaling.png")
        pdf.image(image_path, graph_x_position + 20, graph_y_position + 71, WIDTH / 2 - 30, 5)

        feedback = generate_rssm_feedback(value, labels, current_title, is_overall=True)
        PDF_Generator.print_feedback_box(pdf, feedback, x=10, y=feedback_y_position, w=feedback_box_width, font_size=9)

        counter += 1

        # Display at most 2 charts per page, add a new page when the number exceeds
        if counter == 2:
            pdf.add_page()
            PDF_Generator.section_headers(pdf, 'Self-Concept: Psychological Needs When with Significant Others')
            initial_y_position = pdf.get_y()
            counter = 0

def generate_csip_feedback(scores, labels, current_title, is_overall=False):
    # Define explanatory feedback templates with different titles
    feedback_templates = {
        "Domineering": {
            "description": "This refers to a interpersonal style in which one is too controlling, manipulating, bossy, argumentative, and/or is acting too superior/condescending when relating to others.\n     Your score indicates that this is {}. Our interpersonal styles sometimes varies depending on who we are with. Your scores below indicate how domineering you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Self-Centered": {
            "description": "This refers to a interpersonal style in which one is too insensitive to others needs, thoughts, feelings, has difficulty providing emotional support, liking others and getting along.\n     Your score indicates that this is {}. Your scores below indicate how self-centered you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Distant/Cold": {
            "description": "This refers to a problematic interpersonal style in which one is uncomfortable with being close or intimate, has difficulty fully connecting and enjoying others company.\n     Your score indicates that this is {}. Your scores below indicate how distant/cold you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Socially Inhibited": {
            "description": "This refers to a problematic interpersonal style in which one is anxious and shy around others, unable to be themselves and has difficulty fitting in.\n     Your score indicates that this is {}. Your scores below indicate how socially inhibited you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Nonassertive": {
            "description": "This refers to a problematic interpersonal style in which one tends to be too compromising, and is too easily taken advantage of, acting overly submissive, letting others boss them around too much.\n     Your score indicates that this is {}. Your scores below indicate how nonassertive you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Exploitable": {
            "description": "This refers to a problematic interpersonal style in which one has trouble being assertive and taking the lead, tends to feel weak and insecure and easily embarrassed around others.\n     Your score indicates that this is {}. Your scores below indicate how exploitable you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Self-Sacrificing": {
            "description": "This refers to a problematic interpersonal style in which one is too giving, tending to put others needs before one's own needs, being easily affected by others pain and suffering and being too trusting.\n     Your score indicates that this is {}. Your scores below indicate how self-sacrificing you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        },
        "Intrusive": {
            "description": "This refers to a problematic interpersonal style in which one has trouble respecting others privacy, talking too much, being overly affectionate and/or needing to be the center of attention.\n     Your score indicates that this is {}. Your scores below indicate how intrusive you are with each of the four persons you identified on this measure.\n",
            "problem_levels": [
                (0.49, "not a problem for you"),
                (1.49, "a minor problem for you"),
                (2.49, "a moderate problem for you"),
                (3.00, "a serious problem for you")
            ]
        }
    }

    feedback = f"{current_title} - "
    template = feedback_templates.get(current_title, None)

    if not template:
        return feedback  # If no suitable template is found, return empty feedback

    # If it is the Overall score, generate explanatory feedback
    if is_overall:
        score = float(scores[0])  # Assume the first one is the Overall score
        score = round(score, 2) # round the decimal to two places
        problem_level_text = "not a problem"
        for threshold, text in template['problem_levels']:
            if score <= threshold:
                problem_level_text = text
                break
        feedback += f"Overall score is {score} ({problem_level_text}):\n     {template['description'].format(problem_level_text)}"

    # add an indent before the individual scores
    feedback += "     "

    # List Individual scores without explanation
    for i, score in enumerate(scores[1:], start=1):
        label = labels[i]
        score = round(float(score), 2) # round to two decimal places
        problem_level_text = "not a problem"
        for threshold, text in template['problem_levels']:
            if score <= threshold:
                problem_level_text = text
                break
        feedback += f"{label} score is {score} ({problem_level_text})     "

    return feedback

def add_problematic_styles_intro(pdf):
    pdf.set_font("Arial", "", 10)
    intro_text = (
        "     For each of the four persons you identified in the Relational Self-Schema Measure, you also "
        "completed a shortened version of the Circumplex Scales of Interpersonal Problems (Boudreaux et al., 2018). "
        "As we did for your scores on the Relational Self-Schema Measure, we provide interpretations for both your "
        "overall scores and for each of your individual self-with-other scores. If there is not much difference in your "
        "scores across the four people you listed, you should just use your overall score. However, if for any scale, "
        "you see differences in your scores across the four people, use the individual scores to interpret your feedback."
    )
    pdf.multi_cell(0, 5, intro_text, border=0, align="L")

# Create and add rssm bar graphs
def csip_bar_graphs(my_path, pdf, data, names, titles):
    pdf.add_page()
    PDF_Generator.section_headers(pdf, 'Self Concept: Problematic Interpersonal Styles')
    pdf.ln(4)
    add_problematic_styles_intro(pdf)  # Add the introductory text here

    initial_y_position = pdf.get_y() #+ 10  # Sets the initial Y position after the intro text
    feedback_box_width = 75  # Width of the feedback box
    graph_x_position = 10  # X position for the graph to be placed next to the feedback box
    graph_y_offset = -10     # Additional Y offset for the graph image to improve label alignment
    image_height = 35 # estimation of the graph heights

    counter = 0  # Counter to keep track of graphs on each page

    # Delete irrelevant data
    dataCopy = data.copy()
    dataCopy.pop('RadarRSSMName', None)
    dataCopy.pop('RSSM_YVector', None)
    dataCopy.pop('RSSM_XVector', None)

    # Iterate over each item in the data dictionary
    for key, value in dataCopy.items():
        current_title = titles.pop(0)  # Get the current title

        labels = names

        # Generate and print feedback for the first two graphs with adjusted positioning
        if counter < 2:
            # Position the graph next to the feedback box
            graph_y_position = initial_y_position + (counter * 115)
            Graph_Generator.create_csip_bargraph(pdf, my_path, graph_y_position, value, names, key, current_title)
            image_path = os.path.join(my_path, "RSSM_Scaling.png")
            pdf.image(image_path, graph_x_position + 20, graph_y_position + 73, WIDTH / 2 - 30)

            # position the feedback under the graph
            feedback_y_position = graph_y_position + initial_y_position + image_height  # Adjust y-position for each graph
            feedback = generate_csip_feedback(value, labels, current_title, is_overall=True)
            PDF_Generator.print_feedback_box(pdf, feedback, x=10, y=feedback_y_position, w=(pdf.w - pdf.l_margin - pdf.r_margin), font_size=10)

            counter += 1

        # After the first two graphs, return to the original layout for subsequent pages
        else:
            image_height = 70 # set image height for new pages
            # Reset the counter when adding a new page
            if counter == 2:
                counter = 0
                pdf.add_page()
                PDF_Generator.section_headers(pdf, 'Self Concept: Problematic Interpersonal Styles')
                initial_y_position = pdf.get_y()  # Reset initial Y position for the new page

            # Position the graph next to the feedback box
            graph_y_position = initial_y_position + (counter * 115)
            Graph_Generator.create_csip_bargraph(pdf, my_path, graph_y_position, value, names, key, current_title)
            image_path = os.path.join(my_path, "RSSM_Scaling.png")
            pdf.image(image_path, graph_x_position + 20, graph_y_position + 73, WIDTH / 2 - 30)

            # position the feedback under the graph
            feedback_y_position = graph_y_position + initial_y_position + image_height  # Adjust y-position for each graph
            feedback = generate_csip_feedback(value, labels, current_title, is_overall=True)
            PDF_Generator.print_feedback_box(pdf, feedback, x=10, y=feedback_y_position, w=(pdf.w - pdf.l_margin - pdf.r_margin), font_size=10)
            counter += 1

# Function to generate temperament feedback
def generate_temperament_feedback(scores, labels):
    feedback_templates = {
        "BIS": {
        "very_high": "     Your score suggests that you may be someone who is more sensitive to situations that are unfamiliar, threatening, or challenging. In these situations, you may have more reactivity in emotional parts of the brain, particularly the amygdala, and may experience greater physiological reactivity. Research has found that infants with high behavioral inhibition temperaments are more likely to develop into 'shy' children. Not all infants with high behavioral inhibition stay 'shy' as your experiences and environment can influence how temperament develops. Importantly, people with high behavioral inhibition temperaments do not experience anxiety unless they experience unfamiliar, challenging or threatening situations. In situations that are familiar, non-challenging, or non-threatening, people with high behavioral inhibition are no more anxious than other people.\n     All temperaments have strengths and weaknesses. As a result of being quicker to notice threat and to more readily feel anxious, people with high behaviorally inhibited temperaments can be very motivated to anticipate and prepare for such threats. As a result, they can be very conscientious.  Other research has shown that people with behaviorally inhibited temperaments are more careful, use more thoughtful, strategic approaches to problem-solving.  People with this temperament can be also very empathic, more attuned to the emotional experiences of others. On the downside, research has shown that people with high behaviorally inhibited temperaments can be more vulnerable to problems with anxiety and depression.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths--it's part of who you are.  But to also learn to minimize your temperament's weaknesses by developing compensatory strategies and skills. For example, it's important to learn how to tolerate initial feelings of anxiety so you don't avoid situations that may seem scary at first but actually provide opportunities for connecting with others and developing skills and competencies. Research shows that as you continue to expose yourself to these initially anxiety-provoking situations, your feelings of anxiety will gradually reduce, and you are likely to feel more confident, and not see these situations as threatening.  As a result of seeing these situations as less threatening or novel, you will be less likely in the future to activate your behavioral inhibition system in these situations, which are now more familiar to you.",
        "high": "     Your score suggests that you may be someone who is more sensitive to situations that are unfamiliar, threatening, or challenging. In these situations, you may have more reactivity in emotional parts of the brain, particularly the amygdala, and may experience greater physiological reactivity. Research has found that infants with high behavioral inhibition temperaments are more likely to develop into 'shy' children. Not all infants with high behavioral inhibition stay 'shy' as your experiences and environment can influence how temperament develops. Importantly, people with high behavioral inhibition temperaments do not experience anxiety unless they experience unfamiliar, challenging or threatening situations. In situations that are familiar, non-challenging, or non-threatening, people with high behavioral inhibition are no more anxious than other people.\n     All temperaments have strengths and weaknesses. As a result of being quicker to notice threat and to more readily feel anxious, people with high behaviorally inhibited temperaments can be very motivated to anticipate and prepare for such threats. As a result, they can be very conscientious.  Other research has shown that people with behaviorally inhibited temperaments are more careful, use more thoughtful strategic approaches to problem-solving.  People with this temperament can be also very empathic, more attuned to the emotional experiences of others. On the downside, research has shown that people with high behaviorally inhibited temperaments can be more vulnerable to problems with anxiety and depression.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths it's part of who you are.  But to also learn to minimize your temperament's weaknesses by developing compensatory strategies and skills. For example, it's important to learn how to tolerate initial feelings of anxiety so you don't avoid situations that may seem scary at first but actually provide opportunities for connecting with others and developing skills and competencies. Research shows that as you continue to expose yourself to these initially anxiety-provoking situations, your feelings of anxiety will gradually reduce, and you are likely to feel more confident, and not see these situations as threatening.  As a result of seeing these situations as less threatening or novel, you will be less likely in the future to activate your behavioral inhibition system in these situations, which are now more familiar to you.",
        "average": "     Your score suggests that when exposed to situations that are novel, unfamiliar, or threatening, you are generally no more and no less sensitive to these types of situations as is the typical person. If you also scored approximately in the average range on behavioral activation system temperament, this would suggest that you possess an even-keeled, emotionally stable temperament.",
        "low": "     Your score suggests that you may be less sensitive to situations that are unfamiliar, threatening, or challenging. In these situations, you may have less reactivity in emotional parts of the brain, particularly the amygdala, and may experience less anxiety and less physiological reactivity. Research has found that infants with high behavioral inhibition temperaments are more likely to develop into 'shy' children. Your score suggests that it is unlikely that you were shy as a child, although factors other than temperament can influence shyness.\n     All temperaments have strengths and weaknesses.  For instance, your score suggests that you may be someone who does not readily feel anxious when you face new, challenging, or threatening situations.  You can be calm and even bold.  However, your lower level of sensitivity to threat, unfamiliarity, and challenge can also have a downside.  You may be prone to being impulsive, to approaching situations too quickly without pausing to consider what might go wrong, which can get you into trouble. This is especially true if you also scored higher on the Behavioral Activation System.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths-it's part of who you are.  But to also learn to minimize your temperament's weaknesses by developing compensatory skills.  For example, if impulsivity is a problem, you can learn to hesitate, pause, consider possible negative consequences before approaching a situation that is potentially dangerous.",
        "very_low": '''     Your score suggests that you may be less sensitive to situations that are unfamiliar, threatening, or challenging. In these situations, you may have less reactivity in emotional parts of the brain, particularly the amygdala, and may experience less anxiety and less physiological reactivity. Research has found that infants with high behavioral inhibition temperaments are more likely to develop into "shy" children. Your score suggests that it is unlikely that you were shy as a child, although factors other than temperament can influence shyness.\n     All temperaments have strengths and weaknesses.  For instance, your score suggests that you may be someone who does not readily feel anxious when you face new, challenging, or threatening situations.  You can be calm and even bold.  However, your lower level of sensitivity to threat, unfamiliarity, and challenge can also have a downside.  You may be prone to being impulsive, to approaching situations too quickly without pausing to consider what might go wrong, which can get you into trouble. This is especially true if you also scored higher on the Behavioral Activation System.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths-it's part of who you are.  But to also learn to minimize your temperament's weaknesses by developing compensatory skills.  For example, if impulsivity is a problem, you can learn to hesitate, pause, consider possible negative consequences before approaching a situation that is potentially dangerous.'''
    },
        "BAS": {
            "very_high": "     Your score suggests that you may be more sensitive to situations where there are rewards, things that are attractive, things you want. In these situations, you may have more reactivity in reward systems of the brain that involve the orbitofrontal cortex, the nucleus accumbens, and amygdala, leading you to experience more excitement, more enthusiasm, to approach and get these things that you want. Research has found that people with high behavioral approach temperaments experience positive affect more easily and also learn faster in learning conditioning studies where there are rewards.\n     All temperaments have strengths and weaknesses.  On the plus side, you are capable of experiencing high levels of enthusiasm, positive affect, and motivation to pursue what it is that you are attracted to, what you want.  On the down side, especially if you also scored low in behavioral inhibition, you may have problems with being too impulsive.  People with high behavioral approach temperaments are quick to hit the gas pedal but, especially if they also have low behavioral inhibition temperaments, can be slow to hit the brake pedal.  In short, you can be prone to acting without thinking about potential risks.  You can engage in attractive but risky activities. \n     As with behavioral inhibition, the important thing is to appreciate your temperament and its strengths-it's part of who you are.  But to learn to minimize your temperament's weaknesses by developing coping strategies and skills.  For example, if impulsivity is a problem and sometimes gets you into trouble, you can learn to hesitate, pause, and consider possible negative consequences, prepare for them, before approaching.",
            "high": "     Your score suggests that you may be more sensitive to situations where there are rewards, things that are attractive, things you want. In these situations, you may have more reactivity in reward systems of the brain that involve the orbitofrontal cortex, the nucleus accumbens, and amygdala, leading you to experience more excitement, more enthusiasm, to approach and get these things that you want. Research has found that people with high behavioral approach temperaments experience positive affect more easily and also learn faster in learning conditioning studies where there are rewards.\n     All temperaments have strengths and weaknesses.  On the plus side, you are capable of experiencing high levels of enthusiasm, positive affect, and motivation to pursue what it is that you are attracted to, what you want.  On the down side, especially if you also scored low in behavioral inhibition, you may have problems with being too impulsive.  People with high behavioral approach temperaments are quick to hit the gas pedal but, especially if they also have low behavioral inhibition temperaments, can be slow to hit the brake pedal.  In short, you can be prone to acting without thinking about potential risks.  You can engage in attractive but risky activities. \n     As with behavioral inhibition, the important thing is to appreciate your temperament and its strengths-it's part of who you are.  But to learn to minimize your temperament's weaknesses by developing coping strategies and skills.  For example, if impulsivity is a problem and sometimes gets you into trouble, you can learn to hesitate, pause, and consider possible negative consequences, prepare for them, before approaching.",
            "average": "     Your score suggests that you are fairly typical in your sensitivity to situations where there are rewards, things that are attractive, things you want. In these situations, your reactivity in reward systems of the brain that involve the orbitofrontal cortex, the nucleus accumbens, and amygdala is no more, and no less, reactive than the average person. Similarly, you are likely to experience the amount of excitement and enthusiasm to approach and get these things that you want as the typical person. On the plus side, you are likely to be someone who is even-keeled, emotionally stable, and unlikely to be too impulsive.",
            "low": "     Your score suggests that you may be less sensitive to situations where there are rewards, things that are attractive, things you want. In these situations, you may have less reactivity in reward systems of the brain that involve the orbitofrontal cortex, the nucleus accumbens, and amygdala, and you may experience less excitement, less enthusiasm, to approach and get these things that you want.\n     You might be described as more calm, more even-keeled, emotionally stable, not too excitable or too impulsive.  However, your low behavioral activation temperament can have a down side, in that you may experience less enthusiasm, less excitement and positive affect when you see things you want.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths-its part of who you are.  But to also learn to minimize your temperaments weaknesses by developing compensatory strategies and skills.  For example, if you have difficulty experiencing positive emotions, it may be especially important that you consciously plan for activities that give you pleasure, positive reinforcement, a sense of connection with others or a sense of mastery as you may be less likely to do this spontaneously.  In pursuing goals that are important to you, it might be particularly important for you to reward yourself for small accomplishments to sustain your motivation. ",
            "very_low": "     Your score suggests that you may be less sensitive to situations where there are rewards, things that are attractive, things you want. In these situations, you may have less reactivity in reward systems of the brain that involve the orbitofrontal cortex, the nucleus accumbens, and amygdala, and you may experience less excitement, less enthusiasm, to approach and get these things that you want.\n     You might be described as more calm, more even-keeled, emotionally stable, not too excitable or too impulsive.  However, your low behavioral activation temperament can have a down side, in that you may experience less enthusiasm, less excitement and positive affect when you see things you want.\n     The important thing, and this is true for all temperaments, is to appreciate your temperament and its strengths-its part of who you are.  But to also learn to minimize your temperaments weaknesses by developing compensatory strategies and skills.  For example, if you have difficulty experiencing positive emotions, it may be especially important that you consciously plan for activities that give you pleasure, positive reinforcement, a sense of connection with others or a sense of mastery as you may be less likely to do this spontaneously.  In pursuing goals that are important to you, it might be particularly important for you to reward yourself for small accomplishments to sustain your motivation. "
        },
        "BAS-Drive": {
            "very_high": "     Your score suggests that you tend to be very motivated to pursue the goals you have, and are quick to act on and move towards your goals, as well as being persistent in achieving them.",
            "high": "     Your score suggests that you tend to be very motivated to pursue the goals you have, and are quick to act on and move towards your goals, as well as being persistent in achieving them.",
            "average": "     Your score suggests that you are fairly typical in your tendency to be motivated to pursue goals you have, neither quick or slow to act on and move towards your goals, or persistent or non-persistent in achieving them.",
            "low": "     Your score suggests that you may not be very motivated to pursue goals you have, nor quick to act on and move towards your goals, or persistent in achieving them.",
            "very_low": "     Your score suggests that you may not be very motivated to pursue goals you have, nor quick to act on and move towards your goals, or persistent in achieving them."
        },
        "BAS-Fun Seeking": {
            "very_high": "     Your score suggests that you tend to crave excitement, and are very motivated and quick to pursue new rewards or things you think might be fun or exciting on the spur of the moment.",
            "high": "     Your score This suggests that you tend to crave excitement, and are very motivated and quick to pursue new rewards or things you think might be fun or exciting on the spur of the moment.",
            "average": "     Your score suggests that you are fairly typical in your tendency to be motivated to pursue excitement, fun, new rewards on the spur of the moment.",
            "low": "     Your score suggests that you are not very motivated to pursue excitement, fun, new rewards on the spur of the moment.",
            "very_low": "     Your score suggests that you are not very motivated to pursue excitement, fun, new rewards on the spur of the moment."
        },
        "BAS-Reward": {
            "very_high": "     Your score suggests that you experience a high degree of enthusiasm, excitement, and positive emotions when a positive outcome/reward has occurred or when you anticipate a positive outcome/reward to occur.",
            "high": "     Your score suggests that you experience a high degree of enthusiasm, excitement, and positive emotions when a positive outcome/reward has occurred or when you anticipate a positive outcome/reward to occur.",
            "average": "     Your score suggests that you experience a typical amount of enthusiasm, excitement, and positive emotions when a positive outcome/reward has occurred or when you anticipate a positive outcome/reward to occur.",
            "low": "     Your score suggests that you not experience a typical level of enthusiasm, excitement, and positive emotions when a positive outcome/reward has occurred or when you anticipate a positive outcome/reward to occur.",
            "very_low": "     Your score suggests that you not experience a typical level of enthusiasm, excitement, and positive emotions when a positive outcome/reward has occurred or when you anticipate a positive outcome/reward to occur."
        }
    }

    feedback = ""
    for i, score in enumerate(scores):
        label = labels[i]
        template = feedback_templates.get(label)

        if not template:
            continue

        if score >= 3.5:
            level = "very_high"
        elif score >= 2.75:
            level = "high"
        elif score >= 2.25:
            level = "average"
        elif score >= 1.5:
            level = "low"
        else:
            level = "very_low"

        feedback += f"{label}: {round(score, 2)} ({level.replace('_', ' ')})\n{template[level]}\n\n"

    return feedback

def print_bis_section(pdf):
    # Bold text for the title part
    pdf.set_font("Arial", "B", 10)
    pdf.multi_cell(0, 5, "Behavioral Inhibition System (BIS)", border=0, align="L")

    # Revert to regular text and continue in the same textbox
    pdf.set_font("Arial", "", 10)
    bis_text = ("     The first temperament type is the behavioral inhibition system. It involves a set of brain structures that lead people to hesitate or withdraw "
                "when they encounter situations that seem unfamiliar, challenging, or threatening. In these situations, people who score high in behavioral inhibition more "
                "easily experience anxiety and impulses to hesitate or withdraw. You can think of this as a psychic brake pedal, a stop system, that moves us away from things "
                "that might be dangerous. We all have behavioral inhibition systems. But people inherit behavioral inhibition systems with different sensitivities. "
                "Your score can be used to indicate the sensitivity level of your behavioral inhibition system.")

    # Continue printing the rest of the text
    pdf.multi_cell(0, 5, bis_text, border=0, align="L")

def print_bas_section(pdf):
    # Bold text for the title part
    pdf.set_font("Arial", "B", 10)
    pdf.multi_cell(0, 5, "Behavioral Approach System (BAS)", border=0, align="L")

    # Revert to regular text and continue in the same textbox
    pdf.set_font("Arial", "", 10)
    bas_text = ("     The second temperament type is the behavioral approach system. The behavioral approach system involves a set of brain structures that causes people to "
                "experience excitement, enthusiasm, and be more motivated to approach situations where there are rewards/incentives--that is, things you want, such as food, sex, "
                "or a desired goal. You can think of this as a psychic gas pedal, a go system that moves us to approach things we want. We all have behavioral approach systems. "
                "But people inherit behavioral approach systems that differ in their sensitivity or reactivity.")

    # Continue printing the rest of the text
    pdf.multi_cell(0, 5, bas_text, border=0, align="L")
    pdf.ln(1)
    bas_text_contin = ("     In addition to an overall BAS score, there are three different subscales that measure different types of behavioral activation.  If you do not see much differences in your three BAS subscales, your overall BAS score is probably the best score to interpret.  However, if you score high on subscales but average or low on others, then it is better to just interpret your specific BAS subscale scores.")
    pdf.multi_cell(0, 5, bas_text_contin, border=0, align="L")

# Create and add temperament bar graph
def temperament_graph(my_path, pdf, data, title):
    pdf.add_page()

    # Add title: "Person in Context Assessment"
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Person in Context Assessment", ln=True, align="C")
    pdf.ln(5)

    # Add introductory text
    introductory_text = ("     The surveys you completed are part of a new approach to assessing personality "
                         "based on recent research in personality science. We refer to it as the Person in "
                         "Context Assessment, or PICA, for short. In this personality assessment, you completed "
                         "questionnaires measuring different parts of what makes up your personality, including "
                         "your temperament, self-concept, interpersonal styles, sensitivity to rejection, and your "
                         "personal goals and standards.")
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 5, introductory_text)
    pdf.ln(3)

    # Set the font for the bold title
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 10, "Temperament: Behavioral Inhibition and Approach Systems", border=0, align="C")

    # Define the introductory text with specific words in bold
    intro_text = ("     Temperament refers to inherited biological systems that influence how you react "
                "emotionally and behaviorally to events. To assess temperament, you completed the "
                "Behavioral Inhibition and Behavioral Activation System scale (BIS/BAS; Carver & White, 1994), which is "
                "the most frequently used measure to assess these two temperament systems.")

    # Split the text into parts for formatting
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0,5, intro_text, border=0, align="L")
    pdf.ln(2)

    print_bis_section(pdf)
    pdf.ln(2)

    print_bas_section(pdf)
    pdf.ln(2)

    # Get the current Y position after the introductory text
    current_y = pdf.get_y()
    pdf.ln(5)  # Optional: add a little more space

    # Pass the current Y position to the temperament_bargraph function
    Graph_Generator.temperament_bargraph(my_path, pdf, data[0], data[1], title, y_position=current_y)

    # Get the new Y position after the graph to position the scaling labels
    new_y = current_y + 60  # Adjust based on the height of your graph
    PDF_Generator.temperament_scaling(pdf, y_position=new_y)

    # Generate and print feedback
    labels = ["BIS", "BAS", "BAS-Drive", "BAS-Fun Seeking", "BAS-Reward"]

    # Correct the order of scores to align with the labels
    original_order = [0, 4, 1, 3, 2]  # Indices to reorder the data
    scores = [float(data[0][i]) for i in original_order]  # Reorder scores based on indices
    #labels = ["BIS", "BAS", "BAS-D", "BAS-FS", "BAS-R"]

    feedback = generate_temperament_feedback(scores, labels)

    # Set Y position for the feedback box
    feedback_y_position = new_y + 55  # Adjust based on the content above
    pdf.set_y(feedback_y_position)

    # Print feedback to PDF
    # 移除 font_size 参数
    PDF_Generator.print_feedback_box_horizontal(pdf, feedback, x=10, y=None, w=180)


def send_mail(receiver_address):
    sender_address = 'teambluebirds2023@gmail.com'
    sender_pass = 'zgfuoltymavvcskq'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Your personal assessment feedback report'
    #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'Personalized_report.pdf'
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream', Name=attach_file_name)
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment
    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    print(f"Sending email to: {receiver_address}")  # Debugging print
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

# main = create_report()