import pandas as pd
graphs = {}

def get_data(current):
    df = pd.read_csv(current)
    recent = df.tail(1)
    values = ['GoalThink', 'GoalSatis', 'GoalEfficacy', 'GoalIntrinsic', 'GoalApproach', 'GoalGrowth', 'GoalConflict', # Goal graphs
              'StandardThink', 'StandardSatis', 'StandardEfficacy', 'Standardintrinsic', 'StandardApproach', 'StandardGrowth', 'StandardConflict',# Moral Standard Graphs
              'RssmRelateSatis', 'RssmControlSatis', 'RssmEsteemFrus', 'RssmAutoFrus' , 'RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4'# RSSM graphs
              ]
    add_goals(recent, values[:7])
    add_morals(recent, values[7:])
    add_rssm(recent, values[14:])
    add_temperament(recent)
    add_descriptions(recent)
    add_comparison(recent)
    add_personal_data(recent)
    return graphs

def add_goals(data, values):
    temp = {}
    # There are eight graphs for goals
    for i in range(7):
        checker = 0
        if f'{values[i]}Total' in data.columns:
            temp[values[i]] = [data.iloc[0][f'{values[i]}Total']]
            checker = 1

        for x in range(4):
            if checker == 1:
                temp[values[i]].append(data.iloc[0][f'{values[i]}{x+1}'])
            else:
                temp[values[i]] = [data.iloc[0][f'{values[i]}{x+1}']]
                checker = 1
    graphs['Goals'] = temp

def add_morals(data, values):
    temp = {}
    # There are seven graphs for moral standards
    for i in range(7):
        cur = values.pop(0)
        checker = 0
        if f'{cur}Total' in data.columns:
            temp[cur] = [data.iloc[0][f'{cur}Total']]
            checker = 1
        elif cur == 'StandardIntrinsic':
            temp[cur] = [data.ioloc[0]['StandardintrinsicTotal']]
            checker = 1

        for x in range(4):
            if checker == 1:
                temp[cur].append(data.iloc[0][f'{cur}{x+1}'])
            else:
                temp[cur] = [data.iloc[0][f'{cur}{x+1}']]
                checker = 1
    graphs['Morals'] = temp

def add_comparison(data):

    labels = ['ValueRankMoney', 'ValueRankJobCareer', 'ValueRankEducLearning', 'ValueRankLeisureRecrea', 'ValueRankSelfGrowth', 'ValueRankIntimateRel', 'ValueRankFriendsFamily',
              'ValueRankSpiritReligion', 'ValueRankPhysicalHealth']
    values = {}
    for item in labels:
        values[f'{item[9:]}'] = data.iloc[0][item]
    graphs['Comparison'] = sorted(values, reverse=False)
    
def add_personal_data(data):
    temp = {}
    temp['First'] = data.iloc[0]['RecipientFirstName']
    temp['Last'] = data.iloc[0]['RecipientLastName']
    temp['Email'] = data.iloc[0]['RecipientEmail']
    graphs['Personal'] = temp


def add_rssm(data, values):
    temp = {}
    # There are 4 graphs for rssm values
    for i in range(4):
        cur = values.pop(0)
        checker = 0
        if f'{cur}Total' in data.columns:
            temp[cur] = [data.iloc[0][f'{cur}Total']]
            checker = 1

        for x in range(4):
            if checker == 1:
                temp[cur].append(data.iloc[0][f'{cur}{x+1}'])
            else:
                temp[cur] = [data.iloc[0][f'{cur}{x+1}']]
                checker = 1
    graphs['RSSM'] = temp
    temp = {}
    temp['Overall'] = 'Overall'
    for i in range(4):
        cur = values.pop(0)
        temp[cur] = data.iloc[0][f'{cur}']
    
    graphs['RSSMNames'] = temp


def add_temperament(data):
    labels = ['FFFS', 'BIS', 'BAS-Total', 'BAS-RI', 'BAS-GDP', 'BAS-RR', 'BAS-I']
    temp = {}
    for item in labels:
        temp[item] = data.iloc[0][item]
    graphs['Temperament'] = temp
    
def add_descriptions(data):
    for i in range(4):
        if i == 0:
            graphs['GoalDescription'] = [data.iloc[0][f'GoalDescrip{i+1}']]
            graphs['StandardDescription'] = [data.iloc[0][f'StandardDescrip{i+1}']]
        else:
            graphs['GoalDescription'].append(data.iloc[0][f'GoalDescrip{i+1}'])
            graphs['StandardDescription'].append(data.iloc[0][f'StandardDescrip{i+1}'])
        
def add_radar(data):
    print("hi")