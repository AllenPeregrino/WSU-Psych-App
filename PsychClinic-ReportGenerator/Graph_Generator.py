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
    # plot.set_xlim(1, 7)
    plot.set_xlim(0, 7)
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

    # Creating dataframe in pandas
    plotdata = pd.DataFrame(score, index=names)

    # Plotting the bar chart
    plot = plotdata.plot(kind="barh")
    plot.set_title(title)
    # plot.set_xlim(1, 5)
    plot.set_xlim(0, 5)
    plt.gcf().subplots_adjust(left=0.25)

    # Saving the plot as an image
    fig = plot.get_figure()
    plt.legend('', frameon=False)
    fig.savefig(path + "/images/rssmbarplot{}.png".format(key), transparent=True)

    # Rendering the bar plot in the PDF
    pdf.image(path + "/images/rssmbarplot{}.png".format(key), 90, height, 120)

def create_csip_bargraph(pdf, path, height, data, names, key, title):
    score = [float(numbers) for numbers in data]
    plt.clf()

    # Creating dataframe in pandas
    plotdata = pd.DataFrame(score, index=names)

    # Plotting the bar chart
    plot = plotdata.plot(kind="barh")
    plot.set_title(title)
    # plot.set_xlim(1, 5)
    plot.set_xlim(0, 3)
    plt.gcf().subplots_adjust(left=0.25)

    # Saving the plot as an image
    fig = plot.get_figure()
    plt.legend('', frameon=False)
    fig.savefig(path + "/images/csipbarplot{}.png".format(key), transparent=True)

    # Rendering the bar plot in the PDF
    pdf.image(path + "/images/csipbarplot{}.png".format(key), 90, height, 120)

def temperament_bargraph(path, pdf, data, names, title):
    positions = range(len(data))
    plt.clf()
    y = [float(number) for number in data]
    plt.figure(figsize=(10, 6))

    plt.ylim(0, 4)
    plt.bar(names, y)
    plt.title(title)
    plt.savefig(path + "/images/temperament.png")

    pdf.image(path + "/images/temperament.png", 10, 20, WIDTH)


def create_radar(pdf, path, data, names):
    xVector = 0.5
    yVector = 1

    Person1Name = names['RSSMName1']
    Person2Name = names['RSSMName2']
    Person3Name = names['RSSMName3']
    Person4Name = names['RSSMName4']

    Person1 = pd.DataFrame({
        'group': ['A'],
        'Self-Sacrificing': [data['RadarRSSMFriendIPS'][0]],
        'Intrusive': [data['RadarRSSMDominFriendIPS'][0]],
        'Domineering': [data['RadarRSSMDominantIPS'][0]],
        'Self-Centered': [data['RadarRSSMDominDistantIPS'][0]],
        'Distant/Cold': [data['RadarRSSMDistantIPS'][0]],
        'Socially Inhibited': [data['RadarRSSMYieldDistantIPS'][0]],
        'Nonassertive': [data['RadarRSSMYieldIPS'][0]],
        'Exploitable': [data['RadarRSSMYieldFriendIPS'][0]],
    })

   # print("person1", Person1)

    Person2 = pd.DataFrame({
        'group': ['A'],
        'Self-Sacrificing': [data['RadarRSSMFriendIPS'][1]],
        'Intrusive': [data['RadarRSSMDominFriendIPS'][1]],
        'Domineering': [data['RadarRSSMDominantIPS'][1]],
        'Self-Centered': [data['RadarRSSMDominDistantIPS'][1]],
        'Distant/Cold': [data['RadarRSSMDistantIPS'][1]],
        'Socially Inhibited': [data['RadarRSSMYieldDistantIPS'][1]],
        'Nonassertive': [data['RadarRSSMYieldIPS'][1]],
        'Exploitable': [data['RadarRSSMYieldFriendIPS'][1]],
    })

    #print("person 2", Person2)

    Person3 = pd.DataFrame({
        'group': ['A'],
        'Self-Sacrificing': [data['RadarRSSMFriendIPS'][2]],
        'Intrusive': [data['RadarRSSMDominFriendIPS'][2]],
        'Domineering': [data['RadarRSSMDominantIPS'][2]],
        'Self-Centered': [data['RadarRSSMDominDistantIPS'][2]],
        'Distant/Cold': [data['RadarRSSMDistantIPS'][2]],
        'Socially Inhibited': [data['RadarRSSMYieldDistantIPS'][2]],
        'Nonassertive': [data['RadarRSSMYieldIPS'][2]],
        'Exploitable': [data['RadarRSSMYieldFriendIPS'][2]],
    })

    #print("person 3", Person3)

    Person4 = pd.DataFrame({
        'group': ['A'],
        'Self-Sacrificing': [data['RadarRSSMFriendIPS'][3]],
        'Intrusive': [data['RadarRSSMDominFriendIPS'][3]],
        'Domineering': [data['RadarRSSMDominantIPS'][3]],
        'Self-Centered': [data['RadarRSSMDominDistantIPS'][3]],
        'Distant/Cold': [data['RadarRSSMDistantIPS'][3]],
        'Socially Inhibited': [data['RadarRSSMYieldDistantIPS'][3]],
        'Nonassertive': [data['RadarRSSMYieldIPS'][3]],
        'Exploitable': [data['RadarRSSMYieldFriendIPS'][3]],
    })

    #print("person 4", Person4)

    # number of variable
    categories=list(Person1)[1:]
    N = len(categories)

    # setting values
    values=Person1.loc[0].drop('group').values.flatten().tolist()
    values2=Person2.loc[0].drop('group').values.flatten().tolist()
    values3=Person3.loc[0].drop('group').values.flatten().tolist()
    values4=Person4.loc[0].drop('group').values.flatten().tolist()

    values += values[:1]
    values2 += values2[:1]
    values3 += values3[:1]
    values4 += values4[:1]

    # Combine all values to find maximum value
    all_values = values + values2 + values3 + values4
    max_value = max(map(float, all_values))  # Convert to float and find the maximum

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
                xytext=(0, -2.5), # -2.5 centers our vector
                arrowprops=(dict(facecolor='black',
                                 edgecolor='black',
                                 arrowstyle='->',
                                 linestyle='--',
                                 linewidth=2)))

    # ylabels
    ax.set_rlabel_position(0)
    plt.yticks(np.linspace(-max_value, max_value, 9),
           [str(round(val, 2)) for val in np.linspace(-max_value, max_value, 9)],
           color="black", size=6)
    plt.ylim(-max_value, max_value)

    # plotting the data
    ax.plot(angles, values, linewidth=1, linestyle='solid', color='blue', label=Person1Name)
    ax.fill(angles, values, 'b', alpha=0.0)

    ax.plot(angles, values2, linewidth=1, linestyle='solid', color='red', label=Person2Name)
    ax.fill(angles, values2, 'b', alpha=0.0)

    ax.plot(angles, values3, linewidth=1, linestyle='solid', color='green', label=Person3Name)
    ax.fill(angles, values3, 'b', alpha=0.0)

    ax.plot(angles, values4, linewidth=1, linestyle='solid', color='orange', label=Person4Name)
    ax.fill(angles, values4, 'b', alpha=0.0)

    # adding a legend
    ax.legend(bbox_to_anchor=(0.15, 0.05), fontsize=6)

    # save the graph as a picture
    #matplotlib: ver3.5.2
    fig = ax.get_figure()
    fig.savefig(path + "/images/radar.png", transparent=False)

    # rendering the radar plot
    pdf.image(path + "/images/radar.png", 5, 30, WIDTH-10)