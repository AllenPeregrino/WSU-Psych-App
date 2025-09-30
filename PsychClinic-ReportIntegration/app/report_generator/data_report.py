# Works Cited for Radar Plot: https://www.python-graph-gallery.com/radar-chart/

from fpdf import FPDF
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
import os

WIDTH = 210
HEIGHT = 297


def create_report():
    pdf = FPDF()
    # setting my path as everything leading up to current directory
    my_path = os.path.abspath("")

    pdf.add_page()
    pdf.image(my_path + "/images/wsu_banner.png", 0, 0, WIDTH)
    pdf.image(my_path + "/images/cover_page.png", 0, 50, WIDTH)

    pdf.add_page()
    #create_header(pdf, "Personal Goals")
    
    # sample graphs
    #create_bargraph(pdf, my_path)

    # dictionary with all graph information
    mydict = {"GoalStatus": ({"Score": [1,2,3,4]},["Goal 1", "Goal 2", "Goal 3", "Goal 4"]), 
              "GoalThinking": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalSatis": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalEfficacy": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalIntrinsic": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalApproach": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalGrowth": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"]),
              "GoalConflict": ({"Score": [10,1,2,3,4]},["Goal Total","Goal 1", "Goal 2", "Goal 3", "Goal 4"])}

    counter = 0
    # loop through all the items in the dictionary
    for key, value in mydict.items():
        # If counter == 2 we need to create a new page
        if counter == 2:
            create_bargraph(pdf, my_path, counter*92, value[0], value[1], key)
            print_textboxes(pdf, 1, 4)
            pdf.image(my_path + "/images/scaling.png", 100, 270, WIDTH/2)
            pdf.add_page()
            counter = 0
        else:
            create_bargraph(pdf, my_path, counter*92, value[0], value[1], key)
            counter += 1
    if counter == 2:
        pdf.image(my_path + "/images/scaling.png", 100, (counter*92)-5, WIDTH/2)
        print_textboxes(pdf, 1, 4)


    # Add text boxes
    #print_textboxes(pdf, "Hello Everybody", 4)

    pdf.add_page()
    create_radar(pdf, my_path)
    
    pdf.output('Personalized_report.pdf', 'F')

def print_textboxes(pdf, value, size):
    pdf.set_font("Arial", "", 10)
    pdf.ln(0)
    lineholder = 0
    d = "I wandered lonely as a cloud\nThat floats on high o'er vales and hills,\nWhen all at once I saw a crowd,\nA host, of golden daffodils\nBeside the lake, beneath the trees,\nFluttering and dancing in the breeze."
    for x in range(size):
        pdf.multi_cell(w=75,h=5,txt="Goal {}:\n{}".format(x+1, d), border = 1, align="L")
        lineholder += 72
        pdf.set_y(lineholder)

        

def create_title(pdf):
	pdf.set_font('Arial', '', 24)
	pdf.ln(5)
	pdf.write(5, f"Personality Assessment Feedback")

def create_header(pdf, header):
    pdf.set_font('Arial', '', 16)
    pdf.ln(5)
    pdf.write(5, f'{header}')
    
def create_bargraph(pdf, path, location, tupl1, tupl2, key):
    # creating dataframe in pandas
    plotdata = pd.DataFrame(
    #{"Score": ["GoalStatus1", "GoalStatus2", "GoalStatus3", "GoalStatus4"]}, 
    tupl1, 
    index=tupl2)
    
    
    # plotting the bar char a bar chart
    plot = plotdata.plot(kind="barh")
    plot.set_xlim(0, 7)

    # saving the plot as a picture in image folder
    fig = plot.get_figure()
    fig.savefig(path + "/images/barplot{}.png".format(key) , transparent=True)
    
    # rendering the barplot
    pdf.image(path + "/images/barplot{}.png".format(key), 90, location, 120)


# def create_bargraph2(pdf, path, location):
#     # creating dataframe in pandas
#     plotdata = pd.DataFrame(
#     #{"Score": ["GoalStatus1", "GoalStatus2", "GoalStatus3", "GoalStatus4"]}, 
#     {"Score": [10,1,2,3,4]}, 
#     index=["Overall Goal","Goal 1", "Goal 2", "Goal 3", "Goal 4"])
    
    
#     # plotting the bar char a bar chart
#     plot = plotdata.plot(kind="barh")
#     plot.set_xlim(0, 7)

#     # saving the plot as a picture in image folder
#     fig = plot.get_figure()
#     fig.savefig(path + "/images/barplot2.png", transparent=True)
    
#     # rendering the barplot
#     pdf.image(path + "/images/barplot2.png", 100, location, 100)




def create_radar(pdf, path):
    df = pd.DataFrame({
        'group': ['A','B','C','D'],
        'Friendly': [1.3, 1.0, -0.5, -1.4],
        'Dominant\nFriendly': [0.2, -2.2, 0.0, -0.3],
        'Dominant': [-0.4, -1.0, -1.2, -1.3],
        'Dominant\nDistant': [1.4, 1.5, 0.3, -2.1],
        'Distant': [1.5, -2.1, 0.6, 0.5],
        'Yield\nDistant': [1.2, 1.1, 0.4, -2.0],
        'Yield': [1.2, 1.5, 1.3, 0.6],
        'Yield\nFriendly': [-2.2, 1.5, 0.1, 1.4]
        })

    df2 = pd.DataFrame({
        'group': ['A','B','C','D'],
        'Friendly': [0.5, 1.0, 1.0, 0.4],
        'Dominant Friendly': [1.0, 1.0, 0.5, 0.7],
        'Dominant': [-0.8, 0.3, 0.6, 0.9],
        'Dominant Distant': [-1.0, 1.0, -1.0, 1.0],
        'Distant': [-0.8, -0.5, -0.5, 1.0],
        'Yield Distant': [0.8, 0.5, 0.5, 0.1],
        'Yield': [-0.8, 0.5, 0.5, 0.1],
        'Yield Friendly': [0.7, -2.1, -1.3, -0.2],
        })
    
    # number of variable
    categories=list(df)[1:]
    
    N = len(categories)
    
    # setting values
    values=df.loc[0].drop('group').values.flatten().tolist()
    values2=df2.loc[0].drop('group').values.flatten().tolist()

    values += values[:1]
    values2 += values2[:1]

    # calculating axis angles of plot items
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # create the radar plot
    ax = plt.subplot(111, polar=True)
    ax.tick_params(axis='x', which='major', pad=15)
    ax.tick_params(axis='y', which='major', pad=8)

    # creating axis for each variable and adding labels
    plt.xticks(angles[:-1], categories, color='black', size=8)
    
    # ylabels
    ax.set_rlabel_position(0)
    plt.yticks([-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5], 
        ["-2.5","-2.0","-1.5","-1.0","-0.5","0.0","0.5","1.0","1.5"], 
        color="black", size=7)
    plt.ylim(-2.5,1.5)
    
    # plotting the data
    ax.plot(angles, values, linewidth=1, linestyle='dashed')
    ax.fill(angles, values, 'b', alpha=0.1)

    ax.plot(angles, values2, linewidth=1, linestyle='solid')
    ax.fill(angles, values2, 'b', alpha=0.1)

    # save the graph as a picture
    fig = ax.get_figure()
    fig.savefig(path + "/images/radar.png", transparent=True)
    
    # rendering the radar plot
    pdf.image(path + "/images/radar.png", 5, 30, WIDTH-20)

def create_cell(pdf, text):
    pdf.cell(WIDTH/2-40, h = 58, txt = "{}".format(text), border = 1, ln = 1)
    pdf.cell(WIDTH/2-40, h = 4, border = 0, ln = 2, align = 'L')
    

# calling the create report function to actually generate pdf
main = create_report()