import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi

WIDTH = 210
HEIGHT = 297

def create_bargraph(pdf, path, location, data, labels, key, title):
    score = [float(numbers) for numbers in data]
    # creating dataframe in pandas
    plotdata = pd.DataFrame(
    {"Score": score}, 
    index=labels)
    
    
    # plotting the bar char a bar chart
    plot = plotdata.plot(kind="barh")
    plot.set_title(title)
    plot.set_xlim(1, 7)
    plt.gcf().subplots_adjust(left=0.15)

    # saving the plot as a picture in image folder
    fig = plot.get_figure()
    plt.legend('', frameon=False)
    fig.savefig(path + "/images/barplot{}.png".format(key) , transparent=True)
    
    # rendering the barplot
    pdf.image(path + "/images/barplot{}.png".format(key), 90, location, 120)

def create_rssm_bargraph(pdf, path, height, data, names, key, title):
    score = [float(numbers) for numbers in data]
    plt.clf()
    # creating dataframe in pandas
    plotdata = pd.DataFrame(score, 
    index=names)
    
    # plotting the bar char a bar chart
    plot = plotdata.plot(kind="barh")
    plot.set_title(title)
    plot.set_xlim(1, 7)
    plt.gcf().subplots_adjust(left=0.25)

    # saving the plot as a picture in image folder
    fig = plot.get_figure()
    plt.legend('', frameon=False)
    fig.savefig(path + "/images/rssmbarplot{}.png".format(key) , transparent=True)
    
    # rendering the barplot
    pdf.image(path + "/images/rssmbarplot{}.png".format(key), 10, height, 120)

def temperament_bargraph(path, pdf, data, names, title):
    positions = range(len(data))
    plt.clf()
    y = [float(number) for number in data]
    plt.figure(figsize=(10, 6))

    plt.ylim(0, 4)
    plt.bar(names, y)
    plt.title(title)
    plt.savefig(path + "/images/temperament.png")

    pdf.image(path + "/images/temperament.png", 0, 20, WIDTH)


def create_radar(pdf, path, xVector, yVector):
    RSSMDominantIPS1 = pd.DataFrame({
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

    RSSMDominantIPS2 = pd.DataFrame({
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
    
    RSSMDominantIPS3 = pd.DataFrame({
        'group': ['A','B','C','D'],
        'Friendly': [0.3, -1.0, 1.3, 1.4],
        'Dominant Friendly': [1.0, -1.0, 0.5, 0.7],
        'Dominant': [-0.8, -0.3, 0.6, 0.9],
        'Dominant Distant': [1.0, 1.0, 0.5, 1.0],
        'Distant': [-0.8, -0.5, -2.3, 1.0],
        'Yield Distant': [1.5, 0.5, 0.5, 0.1],
        'Yield': [-2.0, 0.5, -0.5, 0.1],
        'Yield Friendly': [0.7, -2.1, -1.3, -0.2],
        })
    
    RSSMDominantIPS4 = pd.DataFrame({
        'group': ['A','B','C','D'],
        'Friendly': [0.2, 1.0, -1.0, 0.4],
        'Dominant Friendly': [-1.6, 1.0, 0.5, 0.7],
        'Dominant': [-0.8, 0.3, 1.6, 0.9],
        'Dominant Distant': [-2.0, 1.0, -1.0, 1.0],
        'Distant': [-0.8, -0.5, -1.8, 1.0],
        'Yield Distant': [-0.8, 0.5, 0.5, 0.1],
        'Yield': [-0.8, 0.5, 0.5, 0.1],
        'Yield Friendly': [1.7, -2.1, -1.3, -0.2],
        })
    
    # number of variable
    categories=list(RSSMDominantIPS1)[1:]
    
    N = len(categories)
    
    # setting values
    values=RSSMDominantIPS1.loc[0].drop('group').values.flatten().tolist()
    values2=RSSMDominantIPS2.loc[0].drop('group').values.flatten().tolist()
    values3=RSSMDominantIPS3.loc[0].drop('group').values.flatten().tolist()
    values4=RSSMDominantIPS4.loc[0].drop('group').values.flatten().tolist()
    
    values += values[:1]
    values2 += values2[:1]
    values3 += values3[:1]
    values4 += values4[:1]

    # calculating axis angles of plot items
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    # create the radar plot
    ax = plt.subplot(111, polar=True)
    ax.tick_params(axis='x', which='major', pad=15)
    ax.tick_params(axis='y', which='major', pad=8)

    # creating axis for each variable and adding labels
    plt.xticks(angles[:-1], categories, color='black', size=8)
    
    # creating the vector
    ax.annotate('', xy=(xVector,yVector), 
                xytext=(0,-2.5), # -2.5 centers our vector
                arrowprops=(dict(facecolor='black', 
                                 edgecolor='black', 
                                 arrowstyle='->', 
                                 linestyle='--', 
                                 linewidth=2)))
    
    # ylabels
    ax.set_rlabel_position(0)
    plt.yticks([-2.5,-2.0,-1.5,-1.0,-0.5,0.0,0.5,1.0,1.5], 
        ["-2.5","-2.0","-1.5","-1.0","-0.5","0.0","0.5","1.0","1.5"], 
        color="black", size=6)
    plt.ylim(-2.5,1.5)
    
    # plotting the data
    ax.plot(angles, values, linewidth=1, linestyle='solid', color='blue', label='RSSMDominantIPS1')
    ax.fill(angles, values, 'b', alpha=0.0)

    ax.plot(angles, values2, linewidth=1, linestyle='solid', color='red', label='RSSMDominantIPS2')
    ax.fill(angles, values2, 'b', alpha=0.0)
    
    ax.plot(angles, values3, linewidth=1, linestyle='solid', color='green', label='RSSMDominantIPS3')
    ax.fill(angles, values3, 'b', alpha=0.0)
    
    ax.plot(angles, values4, linewidth=1, linestyle='solid', color='orange', label='RSSMDominantIPS4')
    ax.fill(angles, values4, 'b', alpha=0.0)

    # adding a legend
    ax.legend(bbox_to_anchor=(0.15, 0.05), fontsize=6)


    # save the graph as a picture
    fig = ax.get_figure()
    fig.savefig(path + "/images/radar.png", transparent=True)
    
    # rendering the radar plot
    pdf.image(path + "/images/radar.png", 5, 30, WIDTH-20)