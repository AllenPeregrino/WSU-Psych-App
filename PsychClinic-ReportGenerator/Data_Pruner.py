import numpy as np
import pandas as pd
import math
graphs = {}

def get_data(current, i):
    df = pd.read_csv(current)
    recent = df.iloc[[i]]
    #recent = df.tail(1)
    values = ['GoalThink', 'GoalSatis', 'GoalEfficacy', 'GoalIntrinsic', 'GoalApproach', 'GoalGrowth', 'GoalConflict', # Goal graphs
              'StandardThink', 'StandardSatis', 'StandardEfficacy', 'Standardintrinsic', 'StandardApproach', 'StandardGrowth', 'StandardConflict',# Moral Standard Graphs
              'RssmRelateSatis', 'RssmControlSatis', 'RssmEsteemFrus', 'RssmAutoFrus' , 'RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4'# RSSM graphs
              ]
    add_goals(recent, values[:7])
    # add_morals(recent, values[7:])
    add_rssm(recent, values[14:])
    add_temperament(recent)
    add_descriptions(recent)
    add_comparison(recent)
    add_personal_data(recent)
    add_radar(recent)
    add_sensitivity(recent)

    return graphs

def add_sensitivity(data):
    temp = {}
    idx1 = ['Q1365', 'Q473', 'Q476', 'Q479', 'Q482', 'Q485', 'Q488', 'Q491', 'Q494']
    idx2 = ['Q471', 'Q474',	'Q477',	'Q480', 'Q483', 'Q486',	'Q489',	'Q492',	'Q495']

    idx1 = list(map(lambda x:float(data.iloc[0][x]), idx1))
    idx1 = list(map(lambda x:1 if math.isnan(x) else x, idx1))
    idx2 = list(map(lambda x:float(data.iloc[0][x]), idx2))
    idx2 = list(map(lambda x:1 if math.isnan(x) else x, idx2))

    total = [x*y for x,y in zip(idx1,idx2)]
    graphs['RejectionSensitivity'] = sum(total)/9

def add_goals(data, values):
    temp = {}
    checker = 0

    # Goal Think
   # for x in range(4):
    temp = {'GoalThink': [], 'GoalSatis': [], 'GoalEfficacy': [], 'GoalIntrinsic': [], 'GoalApproach': [], 'GoalGrowth': [], 'GoalConflict': []}
    column_indices = [38, 49, 60, 71]
    for column_index in column_indices:
        column_name = f'Q{column_index}'

        if checker == 1:
        #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalThink'].append(data.iloc[0][column_name])
        else:
            temp['GoalThink'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['43_1', '54_1', '66_1', '76_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalSatis'].append(data.iloc[0][column_name])
        else:
            temp['GoalSatis'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['42_1', '53_1', '64_1', '75_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalEfficacy'].append(data.iloc[0][column_name])
        else:
            temp['GoalEfficacy'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['41_1', '52_1', '63_1', '74_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalIntrinsic'].append(data.iloc[0][column_name])
        else:
            temp['GoalIntrinsic'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['39_1', '50_1', '61_1', '72_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalApproach'].append(data.iloc[0][column_name])
        else:
            temp['GoalApproach'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['40_1', '51_1', '62_1', '73_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalGrowth'].append(data.iloc[0][column_name])
        else:
            temp['GoalGrowth'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['40_1', '51_1', '62_1', '73_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['GoalConflict'].append(data.iloc[0][column_name])
        else:
            temp['GoalConflict'] = [data.iloc[0][column_name]]
            checker = 1


    # handle if any values are nan
    temp['GoalThink'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalThink']]
    temp['GoalSatis'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalSatis']]
    temp['GoalEfficacy'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalEfficacy']]
    temp['GoalIntrinsic'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalIntrinsic']]
    temp['GoalApproach'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalApproach']]
    temp['GoalGrowth'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalGrowth']]
    temp['GoalConflict'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['GoalConflict']]


    # # Convert values to integers for calculation
    values = [int(val) for val in temp['GoalThink']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalThink'].insert(0, average)

    values = [int(val) for val in temp['GoalSatis']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalSatis'].insert(0, average)

    values = [int(val) for val in temp['GoalEfficacy']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalEfficacy'].insert(0, average)

    values = [int(val) for val in temp['GoalIntrinsic']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalIntrinsic'].insert(0, average)

    values = [int(val) for val in temp['GoalApproach']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalApproach'].insert(0, average)

    values = [int(val) for val in temp['GoalGrowth']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalGrowth'].insert(0, average)

    values = [int(val) for val in temp['GoalConflict']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['GoalConflict'].insert(0, average)

    graphs['Goals'] = temp
    #print("goals graph: ", graphs['Goals'])

# Note: Moral standards have been deleted
def add_morals(data, values):
    temp = {}
    temp = {'StandardThink': [], 'StandardSatis': [], 'StandardEfficacy': [], 'Standardintrinsic': [], 'StandardApproach': [], 'StandardGrowth': [], 'StandardConflict': []}
    checker = 0

    column_indices = [481, 829, 836, 843]
    #print(f"data.columns: {data.columns}")
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardThink'].append(data.iloc[0][column_name])
        else:
            temp['StandardThink'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['486_1', '834_1', '841_1', '848_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardSatis'].append(data.iloc[0][column_name])
        else:
            temp['StandardSatis'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['485_1', '833_1', '840_1', '847_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardEfficacy'].append(data.iloc[0][column_name])
        else:
            temp['StandardEfficacy'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['484_1', '832_1', '839_1', '846_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['Standardintrinsic'].append(data.iloc[0][column_name])
        else:
            temp['Standardintrinsic'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['482_1', '830_1', '837_1', '844_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardApproach'].append(data.iloc[0][column_name])
        else:
            temp['StandardApproach'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['483_1', '831_1', '838_1', '845_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardGrowth'].append(data.iloc[0][column_name])
        else:
            temp['StandardGrowth'] = [data.iloc[0][column_name]]
            checker = 1

    column_indices = ['483_1', '831_1', '838_1', '845_1']
    for column_index in column_indices:
        column_name = f'Q{column_index}'
        if checker == 1:
            #temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            temp['StandardConflict'].append(data.iloc[0][column_name])
        else:
            temp['StandardConflict'] = [data.iloc[0][column_name]]
            checker = 1


    # Handle if nan values
    temp['StandardThink'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardThink']]
    temp['StandardSatis'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardSatis']]
    temp['StandardEfficacy'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardEfficacy']]
    temp['Standardintrinsic'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['Standardintrinsic']]
    temp['StandardApproach'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardApproach']]
    temp['StandardGrowth'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardGrowth']]
    temp['StandardConflict'] = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp['StandardConflict']]


    values = [int(val) for val in temp['StandardThink']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardThink'].insert(0, average)

    values = [int(val) for val in temp['StandardSatis']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardSatis'].insert(0, average)

    values = [int(val) for val in temp['StandardEfficacy']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardEfficacy'].insert(0, average)

    values = [int(val) for val in temp['Standardintrinsic']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['Standardintrinsic'].insert(0, average)

    values = [int(val) for val in temp['StandardApproach']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardApproach'].insert(0, average)

    values = [int(val) for val in temp['StandardGrowth']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardGrowth'].insert(0, average)

    values = [int(val) for val in temp['StandardConflict']]
    # Calculate the average
    average = sum(values) / len(values)
    temp['StandardConflict'].insert(0, average)

    graphs['Morals'] = temp
    #print("morals: ", graphs['Morals'])

def add_comparison(data):

    labels = ['Money', 'JobCareer', 'EducLearning', 'LeisureRecrea', 'SelfGrowth', 'IntimateRel', 'FriendsFamily',
              'SpiritReligion', 'PhysicalHealth']
    values = {}
    column_index = ['81_1', '81_2', '81_3', '81_4', '81_5', '81_6', '81_7', '81_8', '81_10']

    temp_values = []

    for index in column_index:
        column_name = f'Q{index}'
        temp_values.append(data.iloc[0][column_name])
       # print("temp val", temp_values)

    # check if nan
    temp_values = [0 if isinstance(val, float) and np.isnan(val) else val for val in temp_values]

    # if all values are now 0 set to original values
    if all(val == 0 for val in temp_values):
        # Set values to be 1-9
        temp_values = list(range(1, 10))

    label_values = dict(zip(labels, temp_values))

    sorted_label_values = dict(sorted(label_values.items(), key=lambda item: int(item[1])))
    graphs['Comparison'] = sorted_label_values

    #print("comparison: ", graphs['Comparison'])

def add_personal_data(data):
    temp = {}
    temp['First'] = data.iloc[0]['Q1']
    temp['Last'] = data.iloc[0]['RecipientLastName']
    temp['Email'] = data.iloc[0]['Q3']
    graphs['Personal'] = temp


def add_rssm(data, values):
    temp = {}
    # average = {}
    # average = {'RssmRelateSatisAverage': [], 'RssmControlSatisAverage': []}
    temp = {'RssmRelateSatis': [], 'RssmControlSatis': [], 'RssmEsteemFrus': [], 'RssmAutoFrus': []}

    # relatedness satisfaction
    indices = ['Q12_', 'Q416_', 'Q22_', 'Q27_']
    questions = ['3', '5', '8', '22']
    rsSum = 0
    for index in indices:
        rsAvg = 0
        count = 0
        for q in questions:
            idx = index + q
            curr = float(data.iloc[0][idx])
            if not np.isnan(curr):
                rsAvg += curr
                count += 1
        if count == 0:
            count = 1
        rsAvg = rsAvg/count
        rsSum += rsAvg
        temp['RssmRelateSatis'].append(rsAvg)
    temp['RssmRelateSatis'].insert(0, rsSum/4)
    '''
    indicies = ['RSSM Relatedness Satisfaction-weightedAvg', 'Person 3 Relatedness Satisfaction-weightedAvg']
    for index in indices:
        print(index, data.iloc[0][index])
        temp['RssmRelateSatis'].append(data.iloc[0][index])
        rsSum += float(data.iloc[0][index])
    '''

    # control satis
    indices = ['Q12_', 'Q416_', 'Q22_', 'Q27_']
    questions = ['6', '7', '10', '11', '14', '16', '20', '21']
    csSum = 0
    for index in indices:
        csAvg = 0
        count = 0
        for q in questions:
            idx = index + q
            curr = float(data.iloc[0][idx])
            if not np.isnan(curr):
                csAvg += curr
                count += 1
        if count == 0:
            count = 1
        csAvg = csAvg/count
        csSum += csAvg
        temp['RssmControlSatis'].append(csAvg)
    temp['RssmControlSatis'].insert(0, (csSum/4))
    '''
    indices = ['RssmControlSatis1', 'RssmControlSatis2', 'RssmControlSatis3', 'RssmControlSatis4']

    for index in indices:
        temp['RssmControlSatis'].append(data.iloc[0][index])
        csSum += float(data.iloc[0][index])
    '''


    # esteem frus
    indices = ['Q12_', 'Q416_', 'Q22_', 'Q27_']
    questions = ['2', '4', '9', '13', '15', '17', '23', '24']
    efSum = 0
    for index in indices:
        efAvg = 0
        count = 0
        for q in questions:
            idx = index + q
            curr = float(data.iloc[0][idx])
            if not np.isnan(curr):
                efAvg += curr
                count += 1
        if count == 0:
            count = 1
        efAvg = efAvg/count
        efSum += efAvg
        temp['RssmEsteemFrus'].append(efAvg)
    temp['RssmEsteemFrus'].insert(0, (efSum/4))
    '''
    indices = ['RssmEsteemFrus1', 'RssmEsteemFrus2', 'RssmEsteemFrus3', 'RssmEsteemFrus4']
    efSum = 0
    for index in indices:
        temp['RssmEsteemFrus'].append(data.iloc[0][index])
        efSum += float(data.iloc[0][index])
    temp['RssmEsteemFrus'].insert(0, (efSum/4))
    '''

    #auto frus
    indices = ['Q12_', 'Q416_', 'Q22_', 'Q27_']
    questions = ['1', '12', '18', '19']
    afSum = 0
    for index in indices:
        afAvg = 0
        count = 0
        for q in questions:
            idx = index + q
            curr = float(data.iloc[0][idx])
            if not np.isnan(curr):
                afAvg += curr
                count += 1
        if count == 0:
            count = 1
        afAvg = afAvg/count
        afSum += afAvg
        temp['RssmAutoFrus'].append(afAvg)
    temp['RssmAutoFrus'].insert(0, (afSum/4))
    '''
    indices = ['RssmAutoFrus1', 'RssmAutoFrus2', 'RssmAutoFrus3', 'RssmAutoFrus4']
    afSum = 0
    for index in indices:
        temp['RssmAutoFrus'].append(data.iloc[0][index])
        afSum += float(data.iloc[0][index])
    temp['RssmAutoFrus'].insert(0, (afSum/4))
    '''

    graphs['RSSM'] = temp
    #print("RSSM graph", graphs['RSSM'])
    temp = {}
    temp['Overall'] = 'Overall'

    #column_index = ['11_4_TEXT', '11_5_TEXT', '11_6_TEXT', '11_9_TEXT']
    column_index = ['11_4', '11_5', '11_6', '11_9']
    name = ['RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4']
    for index in column_index:
        column_name = f'Q{index}'
        names = name.pop(0)
        temp[names] = data.iloc[0][column_name]

    graphs['RSSMNames'] = temp
    #print("RSSMnames", graphs['RSSMNames'])

# Note: We have BIS and BAS-Total
def add_temperament(data):
    labels = ['FFFS', 'BIS', 'BAS-Total', 'BAS-RI', 'BAS-GDP', 'BAS-RR', 'BAS-I', 'BAS-D', 'BAS-RR', 'BAS-FS']
    temp = {}
    # temp['FFFS'] = data.iloc[0]['FFFS-weightedAvg']
    indicies = ['Q3T', 'Q9T', 'Q14T', 'Q17T', 'Q20T', 'Q23T', 'Q25T']
    bisAvg = 0
    for idx in indicies:
        curr = float(data.iloc[0][idx])
        if not np.isnan(curr):
            if idx == 'Q3T' or idx == 'Q23T':
                bisAvg += curr
            else:
                bisAvg += abs(curr-5)
    temp['BIS'] = bisAvg/7

    # temp['BAS-RI'] = data.iloc[0]['BAS-RI-weightedAvg']
    # temp['BAS-GDP'] = data.iloc[0]['BAS-GDP-weightedAvg']
    # temp['BAS-RR'] = data.iloc[0]['BAS-RR-weightedAvg']
    # temp['BAS-I'] = data.iloc[0]['BAS-I-weightedAvg']
    indicies = ['Q4T', 'Q10T', 'Q13T', 'Q22T']
    basDAvg = 0
    for idx in indicies:
        curr = abs(float(data.iloc[0][idx])-5)
        if not np.isnan(curr):
            basDAvg += curr
    temp['BAS-D'] = basDAvg/4

    indicies = ['Q6T', 'Q11T', 'Q16T', 'Q21T']
    basRRAvg = 0
    for idx in indicies:
        curr = abs(float(data.iloc[0][idx])-5)
        if not np.isnan(curr):
            basRRAvg += curr
    temp['BAS-RR'] = basRRAvg/4

    indicies = ['Q5T', 'Q8T', 'Q15T', 'Q19T', 'Q24T']
    basFAvg = 0
    for idx in indicies:
        curr = abs(float(data.iloc[0][idx])-5)
        if not np.isnan(curr):
            basFAvg += curr
    temp['BAS-FS'] = basFAvg/5

    temp['BAS'] = (basDAvg+basRRAvg+basFAvg)/13
    graphs['Temperament'] = temp

# Note: GoalDescription should be there, StandardDescription shouldn't be
def add_descriptions(data):
    graphs['GoalDescription'] = [data.iloc[0]['Q33'], data.iloc[0]['Q34'], data.iloc[0]['Q35'], data.iloc[0]['Q36']]
    '''
    for i in range(4):
        if i == 0:
           # graphs['GoalDescription'] = [data.iloc[0][f'GoalDescrip{i+1}']]
            graphs['GoalDescription'] = [data.iloc[0]['Q33'], data.iloc[0]['Q34'], data.iloc[0]['Q35'], data.iloc[0]['Q36']]
           # print("goal descrip", graphs['GoalDescription'])
            #graphs['StandardDescription'] = [data.iloc[0][f'StandardDescrip{i+1}']]
            # graphs['StandardDescription'] = [data.iloc[0]['Q486_4_TEXT'], data.iloc[0]['Q486_5_TEXT'], data.iloc[0]['Q486_6_TEXT'], data.iloc[0]['Q486_7_TEXT']]
           # print("standard descrip: ", graphs['StandardDescription'])

        else:
            graphs['GoalDescription'].append(data.iloc[0][f'GoalDescrip{i+1}'])
            # graphs['StandardDescription'].append(data.iloc[0][f'StandardDescrip{i+1}'])
    '''

def add_radar(data):

    temp = {}
    # Note: All of the below line RSSM don't exist?
    temp = {'RadarRSSMDominantIPS': [], 'RadarRSSMDominDistantIPS': [], 'RadarRSSMDistantIPS': [], 'RadarRSSMYieldDistantIPS': [], 'RadarRSSMYieldIPS': [], 'RadarRSSMYieldFriendIPS': [], 'RadarRSSMFriendIPS': [], 'RadarRSSMDominFriendIPS': [], 'RadarRSSMName': [], 'RSSM_YVector': [], 'RSSM_XVector': []}
    #indicies = ['Q13_', 'Q415_', 'Q417_', 'Q418_']
    #check if not np.isnan(curr):

    domineeringLabel = ['CSDomineering1', 'CSDomineering2', 'CSDomineering3', 'CSDomineering4']
    #['CSIPP1 Domineering-weightedAvg','CSIPP2 Domineering-weightedAvg', 'CSIPP3 Domineering-weightedAvg', 'CSIPP4 Domineering-weightedAvg']
    socInhibitLabel = ['CSSocialInhibit1', 'CSSocialInhibit2', 'CSSocialInhibit3', 'CSSocialInhibit4']
    #['CSIPP1 Socially Inhibited-weightedAvg', 'CSIPP2 Socially Inhibited-weightedAvg', 'CSIPP3 Socially Inhibited-weightedAvg', 'CSIPP4 Socially Inhibited-weightedAvg']
    intrusiveLabel = ['CSIntrusive1', 'CSIntrusive2', 'CSIntrusive3', 'CSIntrusive4']
    #['CSIPP1 Intrusive-weightedAvg', 'CSIPP2 Intrusive-weightedAvg', 'CSIPP3 Intrusive-weightedAvg', 'CSIPP4 Intrusive-weightedAvg']
    SelfSacLabel = ['CSSelfSacrificing1', 'CSSelfSacrificing2', 'CSSelfSacrificing3', 'CSSelfSacrificing4']
    #['CSIPP1 Self-Sacrificing-weightedAvg', 'CSIPP2 Self-Sacrificing-weightedAvg', 'CSIPP3 Self-Sacrificing-weightedAvg', 'CSIPP4 Self-Sacrificing-weightedAvg']
    exploitableLabel = ['CSExploitable1','CSExploitable2','CSExploitable3','CSExploitable4' ]
    #['CSIPP1 Exploitable-weightedAvg', 'CSIPP2 Exploitable-weightedAvg', 'CSIPP3 Exploitable-weightedAvg', 'CSIPP4 Exploitable-weightedAvg']
    nonassertLabel = ['CSNonassertive1', 'CSNonassertive2', 'CSNonassertive3', 'CSNonassertive4']
    #['CSIPP1 Nonassertive-weightedAvg',  'CSIPP2 Nonassertive-weightedAvg',  'CSIPP3 Nonassertive-weightedAvg',  'CSIPP4 Nonassertive-weightedAvg']
    # distantLabel = ['CSIPP1 Distant-weightedAvg', 'CSIPP2 Distant-weightedAvg', 'CSIPP3 Distant-weightedAvg', 'CSIPP4 Distant-weightedAvg'] # Old variable names
    distantLabel = ['CSDistantCold1', 'CSDistantCold2', 'CSDistantCold3', 'CSDistantCold4']
    #['CSIPP1 Distant-Cold-weightedAvg', 'CSIPP2 Distant-Cold-weightedAvg', 'CSIPP3 Distant-Cold-weightedAvg', 'CSIPP4 Distant-Cold-weightedAvg']
    selfCentLabel = ['CSSelfCentered1', 'CSSelfCentered2', 'CSSelfCentered3', 'CSSelfCentered4']
    #['CSIPP1 Self-Centered-weightedAvg', 'CSIPP2 Self-Centered-weightedAvg', 'CSIPP3 Self-Centered-weightedAvg', 'CSIPP4 Self-Centered-weightedAvg']

    # domineering - dominant
    d = 0
    for index in domineeringLabel:
        curr = data.iloc[0][index]
        d += float(curr)
        temp['RadarRSSMDominantIPS'].append(curr)
    temp['RadarRSSMDominantIPS'].insert(0, d/4)

    #self centered - dominant distant
    sc = 0
    for index2 in selfCentLabel:
        curr = data.iloc[0][index2]
        sc += float(curr)
        temp['RadarRSSMDominDistantIPS'].append(curr)
    temp['RadarRSSMDominDistantIPS'].insert(0, sc/4)

    # distant - distant
    dc = 0
    for indexDistant in distantLabel:
        curr = data.iloc[0][indexDistant]
        dc += float(curr)
        temp['RadarRSSMDistantIPS'].append(curr)
    temp['RadarRSSMDistantIPS'].insert(0, dc/4)

    # yield distant - socially inhibited
    si = 0
    for index3 in socInhibitLabel:
        curr = data.iloc[0][index3]
        si += float(curr)
        temp['RadarRSSMYieldDistantIPS'].append(curr)
    temp['RadarRSSMYieldDistantIPS'].insert(0, si/4)

    #nonassertive - yield
    n = 0
    for index4 in nonassertLabel:
        curr = data.iloc[0][index4]
        n += float(curr)
        temp['RadarRSSMYieldIPS'].append(curr)
    temp['RadarRSSMYieldIPS'].insert(0, n/4)

    # exploitable - yield friendly
    e = 0
    for index5 in exploitableLabel:
        curr = data.iloc[0][index5]
        e += float(curr)
        temp['RadarRSSMYieldFriendIPS'].append(curr)
    temp['RadarRSSMYieldFriendIPS'].insert(0, e/4)

    # self-sacrificing - friendly
    ss = 0
    for index6 in SelfSacLabel:
        curr = data.iloc[0][index6]
        ss += float(curr)
        temp['RadarRSSMFriendIPS'].append(curr)
    temp['RadarRSSMFriendIPS'].insert(0, ss/4)

    #intrusive - dominant friendly
    i = 0
    for index7 in intrusiveLabel:
        curr = data.iloc[0][index7]
        i += float(curr)
        temp['RadarRSSMDominFriendIPS'].append(curr)
    temp['RadarRSSMDominFriendIPS'].insert(0, i/4)

    graphs['RadarRSSM'] = temp
    temp = {}


    column_index = ['11_4', '11_5', '11_6', '11_9']
    name = ['RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4']
    for index in column_index:
        column_name = f'Q{index}'
        names = name.pop(0)
        temp[names] = data.iloc[0][column_name]

    graphs['RadarRSSMName'] = temp

    graphs['RSSM_YVector'] = [1]
    graphs['RSSM_XVector'] = [0.5]

