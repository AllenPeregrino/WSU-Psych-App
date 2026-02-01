import numpy as np
import pandas as pd
import math
graphs = {}

def get_data(current, i):
    global graphs
    df = pd.read_csv(current)
    recent = df.iloc[[i]]
    #recent = df.tail(1)
    
    
    rssm_labels = [
        'RssmRelateSatis', 'RssmControlSatis', 'RssmEsteemFrus', 'RssmAutoFrus',
        'RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4'
    ]
    add_goals(recent)
    # add_morals(recent, values[7:])
    add_rssm(recent, rssm_labels)
    add_temperament(recent)
    add_descriptions(recent)
    add_comparison(recent)
    add_personal_data(recent)
    add_radar(recent)
    add_sensitivity(recent)
    add_components(recent)
    add_clinical(recent)

    return graphs

def add_clinical(data):
    graphs['Clinician'] = False
    if data.iloc[0]['client_question'] == 'Yes':
        graphs['Clinician'] = True
        graphs['ClinicianName'] = data.iloc[0]['client_name']

#refactored for redcaps
def add_sensitivity(data):
    temp = {}
    idx1 = ['situation1_q1', 'situation2_q1', 'situation3_q1', 'situation4_q1', 'situation5_q1', 'situation6_q1', 'situation7_q1', 'situation8_q1', 'situation9_q1']
    idx2 = ['situation1_q2', 'situation2_q2', 'situation3_q2', 'situation4_q2', 'situation5_q2', 'situation6_q2', 'situation7_q2', 'situation8_q2', 'situation9_q2']

    idx1 = list(map(lambda x:float(data.iloc[0][x]), idx1))
    idx1 = list(map(lambda x:1 if math.isnan(x) else x, idx1))
    idx2 = list(map(lambda x:float(data.iloc[0][x]), idx2))
    idx2 = list(map(lambda x:1 if math.isnan(x) else x, idx2))

    total = [x*y for x,y in zip(idx1,idx2)]
    graphs['RejectionSensitivity'] = sum(total)/9


#goal questions have been changed but pruner has not been updated
def add_goals(data):
    global graphs
    
    # 11 goal dimensions and their REDCap-calculated columns
    goal_dims = {
        'Accessibility':   ['goal1_accessibility', 'goal2_accessibility', 'goal3_accessibility', 'goal4_accessibility'],
        'PerceivedProgress': ['goal1_perceived_progress', 'goal2_perceived_progress', 'goal3_perceived_progress', 'goal4_perceived_progress'],
        'SelfEfficacy':    ['goal1_self_efficacy', 'goal2_self_efficacy', 'goal3_self_efficacy', 'goal4_self_efficacy'],
        'Approach':        ['goal1_approach', 'goal2_approach', 'goal3_approach', 'goal4_approach'],
        'Avoidance':       ['goal1_avoidance', 'goal2_avoidance', 'goal3_avoidance', 'goal4_avoidance'],
        'SelfConcordance': ['goal1_self_concordance', 'goal2_self_concordance', 'goal3_self_concordance', 'goal4_self_concordance'],
        'Meaning':         ['goal1_meaning', 'goal2_meaning', 'goal3_meaning', 'goal4_meaning'],
        'PsychNeedSatisfaction': ['goal1_psych_need_satisfaction', 'goal2_psych_need_satisfaction', 'goal3_psych_need_satisfaction', 'goal4_psych_need_satisfaction'],
        'ControlSatisfaction':   ['goal1_control_satisfaction', 'goal2_control_satisfaction', 'goal3_control_satisfaction', 'goal4_control_satisfaction'],
        'Relatedness':           ['goal1_relatedness', 'goal2_relatedness', 'goal3_relatedness', 'goal4_relatedness'],
        'GoalConflict':          ['goal1_goal_conflict', 'goal2_goal_conflict', 'goal3_goal_conflict', 'goal4_goal_conflict']
    }

    temp = {}

    for dim, cols in goal_dims.items():
        # Pull values for the 4 goals
        values = []
        for col in cols:
            val = data.iloc[0].get(col, 0)  # fallback to 0 if column missing
            if isinstance(val, float) and np.isnan(val):
                val = None
            values.append(val)

        # Compute mean of non-missing values
        non_missing = [v for v in values if v is not None]
        mean_val = sum(non_missing) / len(non_missing) if non_missing else 0

        # Store with mean at index 0, then goal values
        temp[dim] = [mean_val] + [v if v is not None else 0 for v in values]

    graphs['Goals'] = temp

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

#refactor completed
def add_comparison(data):

    labels = [ 'Job/Career', 'Education/Learning', 'Leisure/Recreation', 'Self-Growth', 'Intimate Relationships', 'Friends & Family',
              'Spirit/Religion', 'Physical Health']
    values = {}
    column_index = ['job_career_rank', 'education_learning_rank', 'leisure_recreation_rank', 'self_rank', 'intimate_rank', 'friends_rank', 'spirituality_religion_rank', 'physical_rank']

    temp_values = []

    for index in column_index:
        temp_values.append(data.iloc[0][index])
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


# changed it for full name, no first and last
def add_personal_data(data):
    temp = {}

    #this is full name 
    temp['First'] = data.iloc[0]['name']

    #temp['Last'] = data.iloc[0]['RecipientLastName']
    temp['Email'] = data.iloc[0]['email_conf']
    graphs['Personal'] = temp

#refactor complete
def add_rssm(data, values):
    temp = {}
    # average = {}
    # average = {'RssmRelateSatisAverage': [], 'RssmControlSatisAverage': []}
    temp = {'RssmRelateSatis': [], 'RssmControlSatis': [], 'RssmEsteemFrus': [], 'RssmAutoFrus': []}

    # relatedness satisfaction
    indices = ['rssmrelatesatis1', 'rssmrelatesatis2', 'rssmrelatesatis3', 'rssmrelatesatis4']
    #indicies = ['RSSM Relatedness Satisfaction-weightedAvg', 'Person 3 Relatedness Satisfaction-weightedAvg']
    rsSum = 0
    for index in indices:
        temp['RssmRelateSatis'].append(data.iloc[0][index])
        rsSum += float(data.iloc[0][index])
    temp['RssmRelateSatis'].insert(0, (rsSum/4))
    '''
    indicies = ['RSSM Relatedness Satisfaction-weightedAvg', 'Person 3 Relatedness Satisfaction-weightedAvg']
    for index in indices:
        print(index, data.iloc[0][index])
        temp['RssmRelateSatis'].append(data.iloc[0][index])
        rsSum += float(data.iloc[0][index])
    '''

    # control satis
    indices = ['rssmcontrolsatis1', 'rssmcontrolsatis2', 'rssmcontrolsatis3', 'rssmcontrolsatis4']
    csSum = 0
    for index in indices:
        temp['RssmControlSatis'].append(data.iloc[0][index])
        csSum += float(data.iloc[0][index])
    temp['RssmControlSatis'].insert(0, (csSum/4))
    '''
    indices = ['RssmControlSatis1', 'RssmControlSatis2', 'RssmControlSatis3', 'RssmControlSatis4']

    for index in indices:
        temp['RssmControlSatis'].append(data.iloc[0][index])
        csSum += float(data.iloc[0][index])
    '''


    # esteem frus
    indices = ['rssmesteemfrus1', 'rssmesteemfrus2', 'rssmesteemfrus3', 'rssmesteemfrus4']
    efSum = 0
    for index in indices:
        temp['RssmEsteemFrus'].append(data.iloc[0][index])
        efSum += float(data.iloc[0][index])
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
    #refactored
    indices = ['rssmautofrus1', 'rssmautofrus2', 'rssmautofrus3', 'rssmautofrus4']
    afSum = 0
    for index in indices:
        temp['RssmAutoFrus'].append(data.iloc[0][index])
        afSum += float(data.iloc[0][index])
    temp['RssmAutoFrus'].insert(0, (afSum/4))

    graphs['RSSM'] = temp
    #print("RSSM graph", graphs['RSSM'])
    temp = {}
    temp['Overall'] = 'Overall'

    column_index = ['final_person_1', 'final_person_2', 'final_person_3', 'final_person_4']
    #column_index = ['11_4', '11_5', '11_6', '11_9']
    name = ['RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4']
    for index in column_index:
        names = name.pop(0)
        temp[names] = data.iloc[0][index]

    graphs['RSSMNames'] = temp
    #print("RSSMnames", graphs['RSSMNames'])

# Note: We have BIS and BAS-Total
    #refactored complete
def add_temperament(data):
    labels = ['FFFS', 'BIS', 'BAS-Total', 'BAS-RI', 'BAS-GDP', 'BAS-RR', 'BAS-I', 'BAS-D', 'BAS-RR', 'BAS-FS']
    temp = {}
    # temp['FFFS'] = data.iloc[0]['FFFS-weightedAvg']
    indicies = ['bad', 'scolding', 'angry_at_me', 'unpleasant', 'done_poorly', 'few_fears', 'worry_mistakes']
    bisAvg = 0
    for idx in indicies:
        curr = float(data.iloc[0][idx])
        if not np.isnan(curr):
            if idx == 'bad' or idx == 'few_fears':
                bisAvg += curr
            else:
                bisAvg += abs(curr-5)
    temp['BIS'] = bisAvg/7

    # temp['BAS-RI'] = data.iloc[0]['BAS-RI-weightedAvg']
    # temp['BAS-GDP'] = data.iloc[0]['BAS-GDP-weightedAvg']
    # temp['BAS-RR'] = data.iloc[0]['BAS-RR-weightedAvg']
    # temp['BAS-I'] = data.iloc[0]['BAS-I-weightedAvg']
    indicies = ['get_what_i_want', 'all_out', 'chance_move', 'no_restrictions']
    basDAvg = 0
    for idx in indicies:
        curr = abs(float(data.iloc[0][idx])-5)
        if not np.isnan(curr):
            basDAvg += curr
    temp['BAS-D'] = basDAvg/4

    indicies = ['try_something_new', 'for_fun', 'spur_moment', 'crave_excitement']
    basRRAvg = 0
    for idx in indicies:
        curr = abs(float(data.iloc[0][idx])-5)
        if not np.isnan(curr):
            basRRAvg += curr
    temp['BAS-RR'] = basRRAvg/4

    indicies = ['doing_well', 'get_want', 'opportunity_excited', 'good_things', 'win_contest']
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
    graphs['GoalDescription'] = [data.iloc[0]['goal1'], data.iloc[0]['goal2'], data.iloc[0]['goal3'], data.iloc[0]['goal4']]
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

#refactor complete
def add_radar(data):

    temp = {}
    # Note: All of the below line RSSM don't exist?
    temp = {'RadarRSSMDominantIPS': [], 'RadarRSSMDominDistantIPS': [], 'RadarRSSMDistantIPS': [], 'RadarRSSMYieldDistantIPS': [], 'RadarRSSMYieldIPS': [], 'RadarRSSMYieldFriendIPS': [], 'RadarRSSMFriendIPS': [], 'RadarRSSMDominFriendIPS': [], 'RadarRSSMName': [], 'RSSM_YVector': [], 'RSSM_XVector': []}
    #indicies = ['Q13_', 'Q415_', 'Q417_', 'Q418_']
    #check if not np.isnan(curr):

    domineeringLabel = ['csdomineering1', 'csdomineering2', 'csdomineering3', 'csdomineering4']
    #['CSIPP1 Domineering-weightedAvg','CSIPP2 Domineering-weightedAvg', 'CSIPP3 Domineering-weightedAvg', 'CSIPP4 Domineering-weightedAvg']
    socInhibitLabel = ['cssocialinhibit1', 'cssocialinhibit2', 'cssocialinhibit3', 'cssocialinhibit4']
    #['CSIPP1 Socially Inhibited-weightedAvg', 'CSIPP2 Socially Inhibited-weightedAvg', 'CSIPP3 Socially Inhibited-weightedAvg', 'CSIPP4 Socially Inhibited-weightedAvg']
    intrusiveLabel = ['csintrusive1', 'csintrusive2', 'csintrusive3', 'csintrusive4']
    #['CSIPP1 Intrusive-weightedAvg', 'CSIPP2 Intrusive-weightedAvg', 'CSIPP3 Intrusive-weightedAvg', 'CSIPP4 Intrusive-weightedAvg']
    SelfSacLabel = ['csselfsacrificing1', 'csselfsacrificing2', 'csselfsacrificing3', 'csselfsacrificing4']
    #['CSIPP1 Self-Sacrificing-weightedAvg', 'CSIPP2 Self-Sacrificing-weightedAvg', 'CSIPP3 Self-Sacrificing-weightedAvg', 'CSIPP4 Self-Sacrificing-weightedAvg']
    exploitableLabel = ['csexploitable1','csexploitable2','csexploitable3','csexploitable4' ]
    #['CSIPP1 Exploitable-weightedAvg', 'CSIPP2 Exploitable-weightedAvg', 'CSIPP3 Exploitable-weightedAvg', 'CSIPP4 Exploitable-weightedAvg']
    nonassertLabel = ['csnonassertive1', 'csnonassertive2', 'csnonassertive3', 'csnonassertive4']
    #['CSIPP1 Nonassertive-weightedAvg',  'CSIPP2 Nonassertive-weightedAvg',  'CSIPP3 Nonassertive-weightedAvg',  'CSIPP4 Nonassertive-weightedAvg']
    # distantLabel = ['CSIPP1 Distant-weightedAvg', 'CSIPP2 Distant-weightedAvg', 'CSIPP3 Distant-weightedAvg', 'CSIPP4 Distant-weightedAvg'] # Old variable names
    distantLabel = ['csdistantcold1', 'csdistantcold2', 'csdistantcold3', 'csdistantcold4']
    #['CSIPP1 Distant-Cold-weightedAvg', 'CSIPP2 Distant-Cold-weightedAvg', 'CSIPP3 Distant-Cold-weightedAvg', 'CSIPP4 Distant-Cold-weightedAvg']
    selfCentLabel = ['csselfcentered1', 'csselfcentered2', 'csselfcentered3', 'csselfcentered4']
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


    column_index = ['final_person_1', 'final_person_2', 'final_person_3', 'final_person_4']
    #column_index = ['11_4', '11_5', '11_6', '11_9']
    name = ['RSSMName1', 'RSSMName2', 'RSSMName3', 'RSSMName4']
    for index in column_index:
        names = name.pop(0)
        temp[names] = data.iloc[0][index]

    graphs['RadarRSSMName'] = temp

    graphs['RSSM_YVector'] = [1]
    graphs['RSSM_XVector'] = [0.5]

def add_components(data):
    options = {}
    name = ['total_survey', 'temperament', 'self-concept', 'goals']
    column_index = ['choose_assessments___1', 'choose_assessments___2', 'choose_assessments___3', 'choose_assessments___4']
    for index in column_index:
        names = name.pop(0)
        options[names] = data.iloc[0][index]

    graphs['components'] = options