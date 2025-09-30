import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import pi
import os

WIDTH = 210
HEIGHT = 297

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_bargraph(pdf, path, location, data, labels, key, title, descriptions):
    # Adjusting scores and labels for missing data
    adjusted_scores = []
    bar_labels = []

    # Skip "Overall" for alignment with descriptions
    for score, desc, label in zip(data[1:], descriptions, labels[1:]):  # Skip first element
        if str(desc) == 'nan':  # Check if the description is missing
            adjusted_scores.append(None)  # No bar for missing data
            bar_labels.append(label)  # Keep the original label
        else:
            adjusted_scores.append(float(score))
            bar_labels.append(label)

    # Add "Overall" back as the first element if needed
    adjusted_scores.insert(0, data[0])
    bar_labels.insert(0, labels[0])

    # Creating the DataFrame for plotting
    plotdata = pd.DataFrame({"Score": adjusted_scores}, index=bar_labels)

    # Creating the bar chart
    ax = plotdata.plot(kind="barh", color="tab:blue", legend=False)
    ax.set_title(title)
    ax.set_xlim(1, 7)  # Aligning with your specified x-axis limits
    plt.gcf().subplots_adjust(left=0.15)

    # Adding red text for missing bars
    for i, (score, label) in enumerate(zip(adjusted_scores, bar_labels)):
        if score is None:
            plt.text(0.2, i, "(Missing)", color="red", va='center', ha='left', fontsize=10)

    # Saving the plot as a PNG file
    # Rendering the bar plot in the PDF
    fig = ax.get_figure()
    images_dir = os.path.join(path, 'images')
    ensure_directory_exists(images_dir)
    image_path = os.path.join(images_dir, f"barplot{key}.png")
    fig.savefig(image_path, transparent=True)
    pdf.image(image_path, 90, location, 120)
    plt.close(fig)

def create_rssm_bargraph(pdf, path, height, data, names, key, title):
    #print(f"Processing key: {key}")
    #print(f"Data received: {data}")

    # Adjust scores for missing data
    adjusted_scores = []
    bar_labels = []

    # Check for missing data and adjust scores and labels
    for score, label in zip(data, names):
        if str(score) == 'nan':  # Check if the score is missing
            adjusted_scores.append(-1)  # Use a placeholder value (e.g., 0) for missing data
            bar_labels.append(label)  # Keep the original label
        else:
            adjusted_scores.append(float(score))
            bar_labels.append(label)

    # Creating dataframe in pandas
    plotdata = pd.DataFrame({"Score": adjusted_scores}, index=bar_labels)
    plotdata = plotdata.iloc[::-1]  # Reverse to match the description box order

    # Plotting the bar chart
    ax = plotdata.plot(kind="barh", color="tab:blue", legend=False)
    ax.set_title(title)
    ax.set_xlim(1, 5)  # Adjust the x-axis range
    ax.set_xticks([1, 2, 3, 4, 5])  # Set the scale position
    ax.set_xticklabels(['1\nvery low', '2', '3\naverage', '4', '5\nvery high'])  # 设置刻度标签
    plt.gcf().subplots_adjust(left=0.25)

    # Adding red text for missing bars
    for i, (score, label) in enumerate(zip(adjusted_scores[::-1], bar_labels[::-1])):  # Reverse to align with plot
        if score == -1:  # Identify placeholder values as missing data
            plt.text(1.2, i, "(Missing)", color="red", va='center', ha='left', fontsize=10)

    # Saving the plot as an image
    # Rendering the bar plot in the PDF
    fig = ax.get_figure()
    images_dir = os.path.join(path, 'images')
    ensure_directory_exists(images_dir)
    image_path = os.path.join(images_dir, f"rssmbarplot{key}.png")
    fig.savefig(image_path, transparent=True)
    pdf.image(image_path, 10, height, 100)

    ################
    # score = [float(numbers) for numbers in data]
    # plt.clf()

    # # Creating dataframe in pandas
    # plotdata = pd.DataFrame(score, index=names)
    # plotdata = plotdata.iloc[::-1] # reverse it so it matches the description box

    # # Plotting the bar chart
    # plot = plotdata.plot(kind="barh")
    # plot.set_title(title)
    # # plot.set_xlim(1, 5)
    # plot.set_xlim(0, 3)
    # plt.gcf().subplots_adjust(left=0.25)

    # # Saving the plot as an image
    # fig = plot.get_figure()
    # plt.legend('', frameon=False)
    # fig.savefig(path + "/images/rssmbarplot{}.png".format(key), transparent=True)

    # # Rendering the bar plot in the PDF
    # pdf.image(path + "/images/rssmbarplot{}.png".format(key), 10, height, 100)

    # plt.close(fig)

    plt.close(fig)

def create_csip_bargraph(pdf, path, height, data, names, key, title):
    #print(f"Processing key: {key}")
    #print(f"Data received: {data}")

    # Adjust scores for missing data
    adjusted_scores = []
    bar_labels = []

    # Check for missing data and adjust scores and labels
    for score, label in zip(data, names):
        if str(score) == 'nan':  # Check if the score is missing
            adjusted_scores.append(-1)  # Use a placeholder value (e.g., 0) for missing data
            bar_labels.append(label)  # Keep the original label
        else:
            adjusted_scores.append(float(score))
            bar_labels.append(label)

    # Creating dataframe in pandas
    plotdata = pd.DataFrame({"Score": adjusted_scores}, index=bar_labels)
    plotdata = plotdata.iloc[::-1]  # Reverse to match the description box order

    # Plotting the bar chart
    ax = plotdata.plot(kind="barh", color="tab:blue", legend=False)
    ax.set_title(title)
    ax.set_xlim(0, 5)  # Adjust the x-axis range
    plt.gcf().subplots_adjust(left=0.25)

    # Adding red text for missing bars
    for i, (score, label) in enumerate(zip(adjusted_scores[::-1], bar_labels[::-1])):  # Reverse to align with plot
        if score == -1:  # Identify placeholder values as missing data
            plt.text(0.2, i, "(Missing)", color="red", va='center', ha='left', fontsize=10)

    # Saving the plot as an image
    # Rendering the bar plot in the PDF
    fig = ax.get_figure()
    images_dir = os.path.join(path, 'images')
    ensure_directory_exists(images_dir)
    image_path = os.path.join(images_dir, f"csipbarplot{key}.png")
    fig.savefig(image_path, transparent=True)
    pdf.image(image_path, 10, height, 100)
    plt.close(fig)

    ################
    # score = [float(numbers) for numbers in data]
    # plt.clf()

    # # Creating dataframe in pandas
    # plotdata = pd.DataFrame(score, index=names)
    # plotdata = plotdata.iloc[::-1] # reverse it so it matches the description box

    # # Plotting the bar chart
    # plot = plotdata.plot(kind="barh")
    # plot.set_title(title)
    # # plot.set_xlim(1, 5)
    # plot.set_xlim(0, 3)
    # plt.gcf().subplots_adjust(left=0.25)

    # # Saving the plot as an image
    # fig = plot.get_figure()
    # plt.legend('', frameon=False)
    # fig.savefig(path + "/images/csipbarplot{}.png".format(key), transparent=True)

    # # Rendering the bar plot in the PDF
    # pdf.image(path + "/images/csipbarplot{}.png".format(key), 10, height, 100)

    # plt.close(fig)

def temperament_bargraph(path, pdf, data, names, title, y_position):
    # Reorder data and names to place 'BAS' as the second item
    reordered_data = [data[0], data[4], data[1], data[2], data[3]]
    reordered_names = [names[0], names[4], names[1], names[2], names[3]]

    # Plotting the reordered bar chart
    positions = range(len(reordered_data))
    plt.clf()
    y = [float(number) for number in reordered_data]
    plt.figure(figsize=(10, 6))

    plt.ylim(0, 4)
    plt.bar(reordered_names, y)
    plt.title(title)

    # Ensuring the directory exists
    images_dir = os.path.join(path, 'images')
    ensure_directory_exists(images_dir)
    image_path = os.path.join(images_dir, "temperament.png")

    # Saving the plot as a PNG file
    plt.savefig(image_path, transparent=True)

    # Rendering the bar plot in the PDF
    pdf.image(image_path, x=10, y=y_position, w=WIDTH - 20)

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
    # rendering the radar plot
    images_dir = os.path.join(path, 'images')
    ensure_directory_exists(images_dir)
    image_path = os.path.join(images_dir, "radar.png")
    fig = ax.get_figure()
    fig.savefig(image_path, transparent=True)

    # Embed the radar plot in the PDF
    pdf.image(image_path, 5, 30, WIDTH - 10)

    plt.close(fig)