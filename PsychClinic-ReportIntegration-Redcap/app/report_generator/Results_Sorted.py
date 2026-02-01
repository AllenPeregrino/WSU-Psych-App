import math

def get_sort(data):
    #BIS_BAS: bis, basRR, basD, basFS
    #0-4
    temperament = [0]*4
    #PACI_Revised: gThinking, gSatisfaction, gSelfEfficacy, gIntrinsicMotivation, gApproachOrientation, gGrowthMindset, gLevelConflict
    #1-7
    selfRegulation = [0]*7
    #RSSM: relatednessSatisfaction, controlSatisfaction, selfEsteemFrustration, autonomyFrustration
    #1-5
    beliefsRSSM = [0]*4
    #CSIP: domineering, selfCentered, distantCold, sociallyInhibited, nonassertive, exploitable, selfSacrificing, intrusive
    #0-3
    beliefsCSIP = [0]*8

    final = ""
    all = []
    temperament = [data['Temperament']['BIS'], data['Temperament']['BAS-RR'], data['Temperament']['BAS-D'], data['Temperament']['BAS-FS']]
    tFactors = ["BIS", "BAS: Reward Responsiveness", "BAS: Drive", "BAS: Fun Seeking"]
    selfRegulation = [data['Goals']['GoalThink'], data['Goals']['GoalSatis'], data['Goals']['GoalEfficacy'], data['Goals']['GoalIntrinsic'], data['Goals']['GoalApproach'], data['Goals']['GoalGrowth'], data['Goals']['GoalConflict']]
    srFactors = ["Goal Thinking", "Goal Satisfaction", "Goal Self-Efficacy", "Goal Intrinsic Motivation", "Goal Approach Orientation", "Goal Growth Mindset", "Goal Level of Conflict"]
    beliefsRSSM = [data['RSSM']['RssmRelateSatis'], data['RSSM']['RssmControlSatis'], data['RSSM']['RssmEsteemFrus'], data['RSSM']['RssmAutoFrus']]
    #print("Expected value (1.5625) directly from beliefsRSSM:", beliefsRSSM[2][0])
    rssmFactors = ["Relatedness Satisfaction", "Control Satisfaction", "Self-Esteem Frustration", "Autonomy Frustration"]
    beliefsCSIP = [data['RadarRSSM']['RadarRSSMDominantIPS'], data['RadarRSSM']['RadarRSSMDominDistantIPS'], data['RadarRSSM']['RadarRSSMDistantIPS'], data['RadarRSSM']['RadarRSSMYieldDistantIPS'], data['RadarRSSM']['RadarRSSMYieldIPS'], data['RadarRSSM']['RadarRSSMYieldFriendIPS'], data['RadarRSSM']['RadarRSSMFriendIPS'], data['RadarRSSM']['RadarRSSMDominFriendIPS']]
    csipFactors = ["Domineering", "Self-Centered", "Distant/Cold", "Socially Inhibited", "Nonassertive", "Exploitable", "Self-Sacrificing", "Intrusive"]

    # Convert elements in temperament to float and replace NaN with 2
    temperament = list(map(lambda x: float(x), temperament))
    temperament = list(map(lambda x: 2 if math.isnan(x) else x, temperament))

    # Convert elements in selfRegulation to float and replace NaN with 3
    selfRegulation = list(map(lambda x: list(map(lambda y: float(y), x)), selfRegulation))
    selfRegulation = list(map(lambda x: list(map(lambda y: 3 if isinstance(y, float) and math.isnan(y) else y, x)), selfRegulation))

    # Debug statements for beliefsRSSM conversions
    #print("BEFORE conversion, beliefsRSSM:", beliefsRSSM)

    # Convert elements in beliefsRSSM to float
    beliefsRSSM = list(map(lambda x: list(map(lambda y: float(y), x)), beliefsRSSM))
    #print("After float conversion, beliefsRSSM:", beliefsRSSM)

    # Replace NaN values in beliefsRSSM with 3
    beliefsRSSM = list(map(lambda x: list(map(lambda y: 3 if isinstance(y, float) and math.isnan(y) else y, x)), beliefsRSSM))
    #print("After NaN replacement, beliefsRSSM:", beliefsRSSM)

    # Convert elements in beliefsCSIP to float
    beliefsCSIP = list(map(lambda x: list(map(lambda y: float(y), x)), beliefsCSIP))
    #print("After float conversion, beliefsCSIP:", beliefsCSIP)

    # Replace NaN values in beliefsCSIP with 3
    beliefsCSIP = list(map(lambda x: list(map(lambda y: 3 if isinstance(y, float) and math.isnan(y) else y, x)), beliefsCSIP))
    #print("After NaN replacement, beliefsCSIP:", beliefsCSIP)

    """
    temperament = [3.0, 1.75, 1.75, 1.2] #0-4
    tFactors = ["BIS", "BAS: Reward Responsiveness", "BAS: Drive", "BAS: Fun Seeking"]
    selfRegulation = [[5, 2, 3, 3],[6, 1, 3, 4],[1, 6, 3, 4],[3, 1, 3, 2],[3, 1, 3, 4],[2, 5, 3, 3],[6, 4, 3, 2]] #1-7
    srFactors = ["Goal Thinking", "Goal Satisfaction", "Goal Self-Efficacy", "Goal Intrinsic Motivation", "Goal Approach Orientation", "Goal Growth Mindset", "Goal Level of Conflict"]
    beliefsRSSM = [[1, 6, 5, 3],[3, 1, 5, 3],[3, 1, 5, 3],[2, 5, 5, 3]] #1-5
    rssmFactors = ["Relatedness Satisfaction", "Control Satisfaction", "Self-Esteem Frustration", "Autonomy Frustration"]
    beliefsCSIP = [[5, 0, 2, 1],[6, 0, 2, 1],[1, 0, 2, 1],[3, 0, 2, 1],[3, 0, 2, 1],[2, 0, 2, 1],[6, 0, 2, 1], [5, 2, 2, 1]] #0-3
    csipFactors = ["Domineering", "Self-Centered", "Distant/Cold", "Socially Inhibited", "Nonassertive", "Exploitable", "Self-Sacrificing", "Intrusive"]
    """

    #Temperament
    tVals = []
    tTypes = []
    #Mindfulness Practice (Dimidjian & Linehan, 2009*; Kabat-Zinn, 1990)
    mp = temperament[0]*.8 + (4 - temperament[1])*.1 + (4 - temperament[2])*.1
    tVals.append(mp)
    tTypes.append("Mindfulness Practice")
    #Relaxation Training (Ferguson et al., 2009*)
    rt = temperament[0]*1.0
    tVals.append(rt)
    tTypes.append("Relaxation Training")
    #Interoceptive Exposure (Barlow, 2001; see Forsyth et al., 2009*)
    ie = temperament[0]*.9 + (4 - temperament[3])*.1
    tVals.append(ie)
    tTypes.append("Interoceptive Exposure")
    #Fruzzetti et al. (2009) “Emotion Regulation”
    er = (4 - temperament[0])*.5 + temperament[1]*.5
    tVals.append(er)
    tTypes.append("Emotion Regulation")

    #calculate ranking
    final += "Temperament\n"
    final += "Personalized Therapy Strategies:\n"
    tTemp = tVals.copy()

    if max(tTemp) <= 2.2:
        final += "No significant treatment recommendations\n"
    else:
        for i in range (1, 3):
            idx = tTemp.index(max(tTemp))
            tTemp[idx] = -1
            text = "%d. %s\n" % (i, tTypes[idx])
            final += text

        tSignificant = [z for z in temperament if (z > 3 or z < 1)]
        if len(tSignificant) > 0:
            final += "Targeted Personality Components: \n"
            f = 0
            for ff in range (0, 3):
                if len(tSignificant) == 0 or f >= 3:
                    break

                max_value = max(tSignificant)
                max_index = temperament.index(max_value)
                if max_value > 3:
                    final += "- " + tFactors[max_index] + " (Very High)" + "\n"
                    temperament[max_index] = 2
                    f += 1

                if (temperament[max_index] > 1 and temperament[max_index] < 3):
                    tSignificant.remove(max_value)
                if len(tSignificant) == 0 or f >= 3:
                    break

                min_value = min(tSignificant)
                min_index = temperament.index(min_value)
                if min_value < 1:
                    final += "- " + tFactors[min_index] + " (Very Low)" + "\n"
                    temperament[min_index] = 2
                    f += 1
                if (temperament[min_index] > 1 and temperament[min_index] < 3):
                    tSignificant.remove(min_value)

        else:
            final += "No Significant Factor(s) of Interest \n"

    all.append(final)

    cleanedList = [x if str(x) != 'nan' else 'Missing' for x in data['GoalDescription']]
    #cleanedList = ['a', 'b', 'c', 'd']
    #cleanedList = [x for x in data['GoalDescription'] if str(x) != 'nan']
    for sr in selfRegulation:
        o = sum(sr) / float(len(sr))
        sr.insert(0, o)
    srTexts = []
    srOrder = []

    for x in range(0, len(cleanedList)+1):
        #Personal Goals & Standards
        srVals = []
        srTypes = []
        currSR = ""

        #Motivational Interviewing (Levensky et al., 2009*; Miller & Rollnick, 2002)
        mi = (8 - selfRegulation[1][x])*.4 + (8 - selfRegulation[0][x])*.3 + (8 - selfRegulation[4][x])*.3
        srVals.append(mi)
        srTypes.append("Motivational Interviewing")
        #Value Clarification (Twohig  & Crosby, 2009*)
        vc = (8 - selfRegulation[3][x])*.5 + selfRegulation[6][x]*.5
        srVals.append(vc)
        srTypes.append("Value Clarification")
        #Cognitive Restructuring Techniques (J. Beck, 1995; Riso, du Toit, Stein, & Young, 2007)
        crt = (8 - selfRegulation[0][x])*.2 + (8 - selfRegulation[2][x])*.3 + (8 - selfRegulation[3][x])*.2 + (8 - selfRegulation[4][x])*.3
        srVals.append(crt)
        srTypes.append("Cognitive Restructuring Techniques")
        #Self-monitoring (Humphreys et al., 2009*)
        sm = (8 - selfRegulation[1][x])*.2 + (8 - selfRegulation[2][x])*.4 + selfRegulation[6][x]*.4
        srVals.append(sm)
        srTypes.append("Self-Monitoring")
        #Guided Mastery Therapy (Bandura, 1997; Scott & Cervone, 2009*; Williams, 1992)
        gmt = (8 - selfRegulation[2][x])
        srVals.append(gmt)
        srTypes.append("Guided Mastery Therapy")

        srTemp = srVals.copy()
        #calculate ranking
        if x == 0:
            final = "Personal Goals & Standards: Overall\n"
            final += "Personalized Therapy Strategies:\n"
        else:
            currSR = "Personal Goals & Standards: Goal %d\n" % (x)
            currSR += "Personalized Therapy Strategies:\n"
            srOrder.append(max(srTemp))

        if max(srTemp) <= 3.85:
            if x == 0:
                final += "No significant treatment \nrecommendations\n"
            else:
                currSR += "No significant treatment \nrecommendations\n"
        else:
            if x != 0:
                for i in range (1, 3):
                    idx = srTemp.index(max(srTemp))
                    srTemp[idx] = -1
                    text = "%d. %s\n" % (i, srTypes[idx])
                    if x == 0:
                        final += text
                    else:
                        currSR += text

                currScores = []
                for y in selfRegulation:
                    currScores.append(y[x])
                srSignificant = [z for z in currScores if (z > 5 or z < 3)]

                if len(srSignificant) > 0:
                    currSR += "Targeted Personality Components: \n"
                    f = 0
                    for ff in range (0, 3):
                        if len(srSignificant) == 0 or f >= 3:
                            break

                        print(srSignificant)
                        max_value = max(srSignificant)
                        max_index = currScores.index(max_value)
                        if max_value > 5 :
                            currScores[max_index] = 3.5
                            if srFactors[max_index] == "Goal Level of Conflict":
                                currSR += "- " + srFactors[max_index] + " (Very High)" + "\n"
                                f += 1
                        if (currScores[max_index] > 3 and currScores[max_index] < 5):
                            srSignificant.remove(max_value)
                        if len(srSignificant) == 0 or f >= 3:
                            break

                        print(srSignificant)
                        min_value = min(srSignificant)
                        min_index = currScores.index(min_value)
                        if min_value < 3:
                            currScores[min_index] = 3.5
                            if srFactors[min_index] != "Goal Level of Conflict":
                                currSR += "- " + srFactors[min_index] + " (Very Low)" + "\n"
                                f += 1
                        if (currScores[min_index] > 3 and currScores[min_index] < 5):
                            srSignificant.remove(min_value)

                    if f == 0:
                        currSR += "No Significant Factor(s) of Interest \n"
                else:
                    currSR += "No Significant Factor(s) of Interest \n"

        if x != 0:
            srTexts.append(currSR)
        else:
            all.append(final)

    for i in range (1, 5):
        idx = srOrder.index(max(srOrder))
        srOrder[idx] = -1
        all.append("#"+ str(i) + " " + srTexts[idx])


    for csip in beliefsCSIP:
        o = sum(csip) / float(len(csip))
        csip.insert(0, o)
    namesRSSM = list(data['RSSMNames'].values())
    #namesRSSM = ['1', '2', '3', '4']
    bTexts = []
    bOrder = []

    rs = data["RejectionSensitivity"]
    #rs = 10
    for x in range(0, len(namesRSSM)):
        #Self-Schema
        bVals = []
        bTypes = []
        currB = ""

        #Situational Analysis
        sa = (6 - beliefsRSSM[1][x])*.2 + beliefsRSSM[2][x]*.4 + beliefsRSSM[3][x]*.4
        sa += (3 - beliefsCSIP[0][x])*.31 + beliefsCSIP[4][x]*.23 + beliefsCSIP[5][x]*.23 + beliefsCSIP[6][x]*.23
        bVals.append(sa)
        bTypes.append("Situational Analysis")
        #Cognitive Restructuring Techniques (J. Beck, 1995; Riso, du Toit, Stein, & Young, 2007)
        crt = (6 - beliefsRSSM[0][x])*.4 + (6 - beliefsRSSM[2][x])*.6
        crt += beliefsCSIP[3][x]*.55 + beliefsCSIP[7][x]*.45
        bVals.append(crt)
        bTypes.append("Cognitive Restructuring Techniques")
        #Behavioral tests of negative cognitions (Dobson & Hamilton, 2009)
        bt = (6 - beliefsRSSM[1][x])*.4 + beliefsRSSM[3][x]*.6
        bt += beliefsCSIP[4][x]*.5 + beliefsCSIP[5][x]*.5
        bt += (rs/15)
        bVals.append(bt)
        bTypes.append("Behavioral tests of negative cognitions")

        #calculate ranking
        bTemp = bVals.copy()
        if x == 0:
            final = "Self-Schema: Overall\n"
            final += "Personalized Therapy Strategies:\n"
        else:
            currB = "Self-Schema: Self-with-%s\n" % (namesRSSM[x])
            currB += "Personalized Therapy Strategies:\n"
            bOrder.append(max(bTemp))

        if max(bTemp) <= 4.4:
            if x == 0:
                final += "No significant treatment \nrecommendations\n"
            else:
                currB += "No significant treatment \nrecommendations\n"
        else:
            if x != 0:
                for i in range (1, 3):
                    idx = bTemp.index(max(bTemp))
                    bTemp[idx] = -1
                    text = "%d. %s\n" % (i, bTypes[idx])
                    if x == 0:
                        final += text
                    else:
                        currB += text
                """
                #Print to verify `x` and the structure of `beliefsRSSM`
                print(f"x = {x}")
                print("Current beliefsRSSM:", namesRSSM[x])

                currScoresRSSM = [
                    beliefsRSSM[0][0],  # Relatedness Satisfaction
                    beliefsRSSM[1][0],  # Control Satisfaction
                    beliefsRSSM[2][0],  # Self-Esteem Frustration
                    beliefsRSSM[3][0]   # Autonomy Frustration
                ]
                print("Relatedness Satisfaction:", beliefsRSSM[0][x])
                print("Control Satisfaction:", beliefsRSSM[1][x])
                print("Self-Esteem Frustration:", beliefsRSSM[2][x])  # Should print 1.5625 at x = 0
                print("Autonomy Frustration:", beliefsRSSM[3][x])
                """
                currScoresRSSM = []
                for y in beliefsRSSM:
                    currScoresRSSM.append(y[x])

                currScoresCSIP = []
                for y in beliefsCSIP:
                    currScoresCSIP.append(y[x])
                # print("currScoresRSSM values after assignment:", currScoresRSSM)
                bSignificantRSSM = [z for z in currScoresRSSM if (z > 4 or z < 2)]
                bSignificantCSIP = [z for z in currScoresCSIP if (z > 2 or z < 1)]
                numSugg = 0

                if len(bSignificantRSSM) > 0 or len(bSignificantCSIP) > 0 or rs <= 5 or rs >= 12.22:
                    currB += "Targeted Personality Components: \n"

                    if len(bSignificantRSSM) > 0:
                        max_value = max(bSignificantRSSM)
                        max_index = currScoresRSSM.index(max_value)
                        min_value = min(bSignificantRSSM)
                        min_index = currScoresRSSM.index(min_value)
                        if max_value-4 > 2-min_value:
                            if max_value > 4 and (rssmFactors[max_index] != "Relatedness Satisfaction" and rssmFactors[max_index] != "Control Satisfaction"):
                                currB += "- " + rssmFactors[max_index] + " (Very High)" + "\n"
                                numSugg += 1
                            elif min_value < 2 and (rssmFactors[min_index] != "Self-Esteem Frustration" and rssmFactors[min_index] != "Autonomy Frustration"):
                                currB += "- " + rssmFactors[min_index] + " (Very Low)" + "\n"
                                numSugg += 1
                        else:
                            if min_value < 2 and (rssmFactors[min_index] != "Self-Esteem Frustration" and rssmFactors[min_index] != "Autonomy Frustration"):
                                currB += "- " + rssmFactors[min_index] + " (Very Low)" + "\n"
                                numSugg += 1
                            elif max_value > 4 and (rssmFactors[max_index] != "Relatedness Satisfaction" and rssmFactors[max_index] != "Control Satisfaction"):
                                currB += "- " + rssmFactors[max_index] + " (Very High)" + "\n"
                                numSugg += 1

                    if len(bSignificantCSIP) > 0:
                        lencsip = len(bSignificantCSIP)-1
                        while lencsip > 0:
                            print(bSignificantCSIP)
                            max_value = max(bSignificantCSIP)
                            max_index = currScoresCSIP.index(max_value)
                            min_value = min(bSignificantCSIP)
                            min_index = currScoresCSIP.index(min_value)
                            if max_value-2 < 1-min_value:
                                if max_value > 2:
                                    currB += "- " + csipFactors[max_index] + " (Very High)" + "\n"
                                    numSugg += 1
                                    break
                                elif min_value < 1 and (csipFactors[min_index] == "Self-Sacrificing"):
                                    currB += "- " + csipFactors[min_index] + " (Very Low)" + "\n"
                                    numSugg += 1
                                    break
                            else:
                                if min_value < 1 and (csipFactors[min_index] == "Self-Sacrificing"):
                                    currB += "- " + csipFactors[min_index] + " (Very Low)" + "\n"
                                    numSugg += 1
                                    break
                                elif max_value > 2:
                                    currB += "- " + csipFactors[max_index] + " (Very High)" + "\n"
                                    numSugg += 1
                                    break

                            lencsip -= 1
                            bSignificantCSIP.remove(max_value)
                            if len(bSignificantCSIP) > 0 and (max_value != min_value):
                                bSignificantCSIP.remove(min_value)
                            if len(bSignificantCSIP) == 0:
                                lencsip = 0


                    if rs <= 1.39:
                        currB += "- Rejection Sensitivity (Very Low)" + "\n"
                        numSugg += 1
                    elif rs <= 5:
                        currB += "- Rejection Sensitivity (Low)" + "\n"
                        numSugg += 1
                    elif rs > 15.85:
                        currB += "- Rejection Sensitivity (Very High)" + "\n"
                        numSugg += 1
                    elif rs >= 12.22:
                        currB += "- Rejection Sensitivity (High)" + "\n"
                        numSugg += 1

                    if numSugg == 0:
                        currB += "No Significant Factor(s) of Interest \n"
                else:
                    currB += "No Significant Factor(s) of Interest \n"


        if x != 0:
            bTexts.append(currB)
        else:
            all.append(final)

    for i in range (1, 5):
        idx = bOrder.index(max(bOrder))
        bOrder[idx] = -1
        all.append("#"+ str(i) + " " + bTexts[idx])

    return all