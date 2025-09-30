import os
from fpdf import FPDF
import Graph_Generator
import PDF_Generator
import Data_Pruner
import automated_responses

# email stuff
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
mail_content = '''Hello,
This is a test mail.
In this mail we are sending some attachments.
The mail is sent using Python SMTP library.
Thank You
'''
# end email stuff

WIDTH = 210
HEIGHT = 297

def create_report():
    automated_responses.get_survey(save_survey = "", survey_id = 'SV_3wvBtxhaQcsl06G')
    pdf = FPDF()
    # setting my path as everything leading up to current directory
    my_path = os.path.abspath("")
    
    # saving the most recent survey result from csv data into pandas df
    df = Graph_Generator.pd.read_csv('Capstone Working Survey.csv')
    currentSurvey = df.tail(1)
    data = Data_Pruner.get_data('Capstone Working Survey.csv')


    # Code for accessing column value by name: value = currentSurvey.loc[:, 'IPAddress'].values[0]
    # IPAddress is the column name in the example above

    # Add title page
    title_page(my_path, pdf, data['Personal'])

    goalTitles = ["Goal Thinking", "Goal Satisfaction", "Goal Self-Efficacy", "Goal Intrinsic Motivation", "Goal Approach Orientation", "Goal Growth Mindset", "Goal Level of Conflict"]

    standardTitles = ["Moral Standard Thinking", "Moral Standard Satisfaction", "Moral Standard Self-Efficacy", "Moral Standard Intrinsic Motivation", "Moral Standard Approach Orientation",
                    "Moral Standard Growth Mindset", "Moral Standard Level of Conflict"]
    
    # begin adding goals section of the pdf
    goals_bar_graphs(my_path, pdf, data['Goals'], data['GoalDescription'], goalTitles)

    # Comparison figure
    PDF_Generator.comparison_figure(pdf, my_path, data['Comparison'], data['GoalDescription'])

    # Add extra bar graphs
    standard_bar_graphs(my_path, pdf, data['Morals'], data['StandardDescription'], standardTitles)

    rssmTitles = ["Relatedness Satisfaction", "Control Satisfaction", "Self-Esteem Frustration", "Autonomy Frustration"]
    rssm_bar_graphs(my_path, pdf, data['RSSM'], [v for k,v in data['RSSMNames'].items()], rssmTitles)
    
    stuff = [list(data['Temperament'].values()), list(data['Temperament'].keys())]
    temperament_graph(my_path, pdf, stuff, "Temperament")

    # add page and begin adding the radar plot
    pdf.add_page()
    PDF_Generator.create_title(pdf, 'Radar Plot')
    Graph_Generator.create_radar(pdf, my_path, 0.5, 1) # TODO: last 2 parameters need to be the vector values from pandas df
    
    pdf.output('Personalized_report.pdf', 'F')

    send_mail()

def title_page(my_path, pdf, info):
    pdf.add_page()
    pdf.image(my_path + "/images/wsu_banner.png", 0, 0, WIDTH)
    pdf.image(my_path + "/images/Washington-State-University-logo.png", 0, HEIGHT/2 - 100, WIDTH)
    pdf.image(my_path + "/images/buffer.png", 0, HEIGHT/2 + 1, WIDTH)
    PDF_Generator.create_title(pdf, 'For: {} {}'.format(info['First'], info['Last']))
    # pdf.image(my_path + "/images/cover_page.png", 0, 50, WIDTH)

# function to complete the goals section of bar graphs and text boxes
def goals_bar_graphs(my_path, pdf, data, descriptions, titles):
    pdf.add_page()
    counter = 0
    # loop through all the items in the dictionary
    for key, value in data.items():
        if len(value) == 4:
            labels = ["Goal 1", "Goal 2", "Goal 3", "Goal 4"]
        else:
            labels = ["Overall","Goal 1", "Goal 2", "Goal 3", "Goal 4"]

        if key[4:] == 'Conflict' or key[4:] == 'Growth':
            holder = 'Goal_{}'.format(key[4:])
        else:
            holder = key[4:]

        # If counter == 2 we need to create a new page
        if counter == 2:
            Graph_Generator.create_bargraph(pdf, my_path, counter*92, value, labels, key, titles.pop(0))
            PDF_Generator.print_textboxes(pdf, "Goal", descriptions, 4)
            pdf.image(my_path + "/images/{}_Scaling.png".format(holder), 100, 270, WIDTH/2)
            pdf.add_page()
            counter = 0
        else:
            Graph_Generator.create_bargraph(pdf, my_path, counter*92, value, labels, key, titles.pop(0))
            pdf.image(my_path + "/images/{}_Scaling.png".format(holder), 100, counter*92+86, WIDTH/2)
            counter += 1

    # if counter is not 0 then we add new text boxes
    if counter != 0:
        PDF_Generator.print_textboxes(pdf, "Goal", descriptions, 4)

# Create and add the text boxes and graphs for the standard graphs
def standard_bar_graphs(my_path, pdf, data, descriptions, titles):
    pdf.add_page()
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
            Graph_Generator.create_bargraph(pdf, my_path, counter*92, value, labels, key, titles.pop(0))
            PDF_Generator.print_textboxes(pdf, "Moral Standard", descriptions, 4)
            pdf.image(my_path + "/images/{}_Scaling.png".format(holder), 100, 270, WIDTH/2)
            pdf.add_page()
            counter = 0
        else:
            Graph_Generator.create_bargraph(pdf, my_path, counter*92, value, labels, key, titles.pop(0))
            pdf.image(my_path + "/images/{}_Scaling.png".format(holder), 100, counter*92+86, WIDTH/2)
            counter += 1
    # if counter is 2 then we add new text boxes
    if counter != 0:
        PDF_Generator.print_textboxes(pdf, "Moral Standard", descriptions, 4)

# Create and add rssm bar graphs
def rssm_bar_graphs(my_path, pdf, data, names, titles):
    pdf.add_page()
    counter = 0
    # loop through all the items in the dictionary
    for key, value in data.items():
        # If counter == 2 we need to create a new page
        if counter == 2:
            Graph_Generator.create_rssm_bargraph(pdf, my_path, (counter*88+14), value, names, key, titles.pop(0))
            pdf.image(my_path + "/images/Scaling.png", 30, 275, WIDTH/2)
            pdf.add_page()
            counter = 0
        else:
            Graph_Generator.create_rssm_bargraph(pdf, my_path, (counter*88+14), value, names, key, titles.pop(0))
            counter += 1
    if counter != 0:
        pdf.image(my_path + "/images/Scaling.png", 30, (counter*88+14), WIDTH/2)

# Create and add temperament bar graph
def temperament_graph(my_path, pdf, data, title):
    body = {'FFFS': 'FFFS stands for ',
            'BIS': 'BIS stands for',
            'BAS-Total': 'BAS-Total stands for',
            'BAS-RI': 'BAS-RI stands for',
            'BAS-GDP': 'BAS-GDP stands for',
            'BAS-RR': 'BAS-RR stands for',
            'BAS-I': 'BAS-I stands for'}
    pdf.add_page()
    Graph_Generator.temperament_bargraph(my_path, pdf, data[0], data[1], title)
    PDF_Generator.write_body(pdf, body)

def send_mail():
    sender_address = 'teambluebirds2023@gmail.com'
    sender_pass = 'zgfuoltymavvcskq'
    receiver_address = 'jillianplahn@gmail.com'
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
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

main = create_report()