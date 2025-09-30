import math

def get_sort(data):
    #BIS_BAS: bis, basRR, basD, basFS
    temperament = [0]*4
    #PACI_Revised: gThinking, gSatisfaction, gSelfEfficacy, gIntrinsicMotivation, gApproachOrientation, gGrowthMindset, gLevelConflict
    selfRegulation = [0]*7
    #RSSM: relatednessSatisfaction, controlSatisfaction, selfEsteemFrustration, autonomyFrustration
    beliefsRSSM = [0]*4
    #CSIP: domineering, selfCentered, distantCold, sociallyInhibited, nonassertive, exploitable, selfSacrificing, intrusive
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

    # temperament = list(map(lambda x:float(x), temperament))
    # temperament = list(map(lambda x:2 if math.isnan(x) else x, temperament))
    # selfRegulation = list(map(lambda x:list(map(lambda y:float(y), x)), selfRegulation))
    # selfRegulation = list(map(lambda x:list(map(lambda y:3 if math.isnan(y) else y, x)), selfRegulation))
    # print("BEFORE conversion, beliefsRSSM:", beliefsRSSM)
    # beliefsRSSM = list(map(lambda x:list(map(lambda y:float(y), x)), beliefsRSSM))
    # print("After conversion, beliefsRSSM:", beliefsRSSM)
    # beliefsRSSM = list(map(lambda x:list(map(lambda y:3 if math.isnan(y) else y, x)), beliefsRSSM))
    # print("After conversion, beliefsRSSM:", beliefsRSSM)
    # beliefsCSIP = list(map(lambda x:list(map(lambda y:float(y), x)), beliefsCSIP))
    # print("After conversion, beliefsRSSM:", beliefsRSSM)
    # beliefsCSIP = list(map(lambda x:list(map(lambda y:3 if math.isnan(y) else y, x)), beliefsCSIP))
    # print("After conversion, beliefsRSSM:", beliefsRSSM)

    #Temperament
    tVals = []
    tTypes = []
    #Acceptance and commitment therapy (Hayes, Stroshahl, & Wilson, 1999)
    act = temperament[0]*.5 + (4 - temperament[2])*.5
    tVals.append(act)
    tTypes.append("Acceptance and commitment therapy")
    #Mindfulness Practice (Dimidjian & Linehan, 2009*; Kabat-Zinn, 1990)
    mp = temperament[0]*.3 + (4 - temperament[1])*.4 + (4 - temperament[2])*.3
    tVals.append(mp)
    tTypes.append("Mindfulness Practice")
    #Relaxation Training (Ferguson et al., 2009*)
    rt = temperament[0]*1.0
    tVals.append(rt)
    tTypes.append("Relaxation Training")
    #Emotion Regulation Interventions for Anger (Donohue et al., 2009*)
    eria = temperament[0]*.3 + (4 - temperament[1])*.35 + (4 - temperament[2])*.35
    tVals.append(eria)
    tTypes.append("Emotion Regulation Interventions for Anger")
    #Interoceptive Exposure (Barlow, 2001; see Forsyth et al., 2009*)
    ie = temperament[0]*1.0
    tVals.append(ie)
    tTypes.append("Interoceptive Exposure")
    #Live (In Vivo) Exposure (Hazlett-Stevens & Craske, 2009*)
    le = temperament[0]*1.0
    tVals.append(le)
    tTypes.append("Live (In Vivo) Exposure")
    #Fruzzetti et al. (2009) “Emotion Regulation”
    er = temperament[0]*.35 + (4 - temperament[1])*.35 + (4 - temperament[2])*.15 + (4 - temperament[2])*.15
    tVals.append(er)
    tTypes.append("Emotion Regulation")

    #calculate ranking
    final += "Temperament: \n"
    tTemp = tVals.copy()

    if max(tTemp) <= 2.2:
        final += "No significant treatment \nrecommendations\n"
    else:
        for i in range (1, 3):
            idx = tTemp.index(max(tTemp))
            tTemp[idx] = -1
            text = "%d. %s\n" % (i, tTypes[idx])
            final += text

        tSignificant = [z for z in temperament if (z > 3 or z < 1)]
        if len(tSignificant) > 0:
            final += "Significant Factor(s) of \nInterest: \n"
        for i, s in enumerate(temperament):
            if s < 1:
                final += "- " + tFactors[i] + " (Very Low)" + "\n"
            elif s > 3:
                final += "- " + tFactors[i] + " (Very High)" + "\n"
    all.append(final)

    cleanedList = [x if str(x) != 'nan' else 'Missing' for x in data['GoalDescription']]
    #cleanedList = [x for x in data['GoalDescription'] if str(x) != 'nan']
    for sr in selfRegulation:
        o = sum(sr) / float(len(sr))
        sr.insert(0, o)
    srTexts = []
    srOrder = []

    for x in range(0, len(cleanedList)+1):
        #Self-Regulation
        srVals = []
        srTypes = []
        currSR = ""

        #Schema change therapy (Newman, 2009*; Young, Klosko, & Weishaar, 2000)
        sct = (8 - selfRegulation[1][x])*.4 + (8 - selfRegulation[2][x])*.3 + (8 - selfRegulation[4][x])*.3
        srVals.append(sct)
        srTypes.append("Schema change therapy")
        #Situational Analysis
        sa = (8 - selfRegulation[3][x])*.33 + (8 - selfRegulation[5][x])*.33 + selfRegulation[6][x]*.34
        srVals.append(sa)
        srTypes.append("Situational Analysis")
        #Cognitive Restructuring Techniques (J. Beck, 1995; Riso, du Toit, Stein, & Young, 2007)
        crt = (8 - selfRegulation[0][x])*.2 + (8 - selfRegulation[2][x])*.3 + (8 - selfRegulation[3][x])*.2 + (8 - selfRegulation[4][x])*.3
        srVals.append(crt)
        srTypes.append("Cognitive Restructuring Techniques")
        #Behavioral tests of negative cognitions (Dobson & Hamilton, 2009)
        btnc = (8 - selfRegulation[1][x])*.2 + (8 - selfRegulation[2][x])*.4 + selfRegulation[6][x]*.4
        srVals.append(btnc)
        srTypes.append("Behavioral tests of negative cognitions")
        #Interpersonal Psychotherapy
        ip = (8 - selfRegulation[2][x])*.32 + (8 - selfRegulation[3][x])*.36 + (8 - selfRegulation[5][x])*.32
        srVals.append(ip)
        srTypes.append("Interpersonal Psychotherapy")

        srTemp = srVals.copy()
        #calculate ranking
        if x == 0:
            final = "Self-Regulation: Overall\n"
        else:
            currSR = "Self-Regulation: Goal %d\n" % (x)
            srOrder.append(max(srTemp))

        if max(srTemp) <= 3.85:
            if x == 0:
                final += "No significant treatment \nrecommendations\n"
            else:
                currSR += "No significant treatment \nrecommendations\n"
        else:
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
            srSignificant = [z for z in currScores if (z > 5.5 or z < 2.5)]
            if len(srSignificant) > 0:
                currSR += "Significant Factor(s) of \nInterest: \n"
            for i, s in enumerate(currScores):
                if s > 5.5:
                    currSR += "- " + srFactors[i] + " (Very High)" + "\n"
                if s < 2.5:
                    currSR += "- " + srFactors[i] + " (Very Low)" + "\n"

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
    bTexts = []
    bOrder = []

    rs = data["RejectionSensitivity"]
    for x in range(0, len(namesRSSM)):
        #Beliefs
        bVals = []
        bTypes = []
        currB = ""

        #Motivational Interviewing (Levensky et al., 2009*; Miller & Rollnick, 2002)
        mi = (6 - beliefsRSSM[1][x])*.45 + beliefsRSSM[3][x]*.55
        mi += (3 - beliefsCSIP[1][x])*.4 + beliefsCSIP[4][x]*.3 + beliefsCSIP[5][x]*.3
        mi += (rs/15)
        bVals.append(mi)
        bTypes.append("Motivational Interviewing")
        #Value Clarification (Twohig  & Crosby, 2009*)
        vc = (6 - beliefsRSSM[1][x])*.2 + (6 - beliefsRSSM[2][x])*.4 + beliefsRSSM[3][x]*.4
        vc += (3 - beliefsCSIP[0][x])*.31 + beliefsCSIP[4][x]*.23 + beliefsCSIP[5][x]*.23 + beliefsCSIP[6][x]*.23
        vc += (rs/15)*.9
        bVals.append(vc)
        bTypes.append("Value Clarification")
        #Guided Mastery Therapy (Bandura, 1997; Scott & Cervone, 2009*; Williams, 1992)
        gmt = (6 - beliefsRSSM[0][x])*.4 + (6 - beliefsRSSM[2][x])*.6
        gmt += beliefsCSIP[3][x]*.55 + beliefsCSIP[7][x]*.45
        gmt += (rs/15)*.8
        bVals.append(gmt)
        bTypes.append("Guided Mastery Therapy")
        #Self-monitoring (Humphreys et al., 2009*)
        sm = (6 - beliefsRSSM[1][x])*.4 + beliefsRSSM[3][x]*.6
        sm += beliefsCSIP[4][x]*.5 + beliefsCSIP[5][x]*.5
        sm += (rs/15)
        bVals.append(sm)
        bTypes.append("Self-monitoring")
        #Self-management therapy (Rehm, 1990; Rehm & Adams, 2009*)
        smt = (6 - beliefsRSSM[1][x])*.5 + (6 - beliefsRSSM[2][x])*.5
        smt += beliefsCSIP[2][x]*.34 + beliefsCSIP[3][x]*.33 + beliefsCSIP[6][x]*.33
        smt += (rs/15)*.9
        bVals.append(smt)
        bTypes.append("Self-management therapy")

        #calculate ranking
        bTemp = bVals.copy()
        if x == 0:
            final = "Beliefs: Overall\n"
        else:
            currB = "Beliefs: Self-with-%s\n" % (namesRSSM[x])
            bOrder.append(max(bTemp))

        if max(bTemp) <= 4.4:
            if x == 0:
               final += "No significant treatment \nrecommendations\n"
            else:
                currB += "No significant treatment \nrecommendations\n"
        else:
            for i in range (1, 3):
                idx = bTemp.index(max(bTemp))
                bTemp[idx] = -1
                text = "%d. %s\n" % (i, bTypes[idx])
                if x == 0:
                    final += text
                else:
                    currB += text

            # Print to verify `x` and the structure of `beliefsRSSM`
            #print(f"x = {x}")
            #print("Current beliefsRSSM:", beliefsRSSM)

            currScoresRSSM = [
                beliefsRSSM[0][0],  # Relatedness Satisfaction
                beliefsRSSM[1][0],  # Control Satisfaction
                beliefsRSSM[2][0],  # Self-Esteem Frustration
                beliefsRSSM[3][0]   # Autonomy Frustration
            ]
            #print("Relatedness Satisfaction:", beliefsRSSM[0][x])
            #print("Control Satisfaction:", beliefsRSSM[1][x])
            #print("Self-Esteem Frustration:", beliefsRSSM[2][x])  # Should print 1.5625 at x = 0
            #print("Autonomy Frustration:", beliefsRSSM[3][x])

            currScoresCSIP = []
            for y in beliefsCSIP:
                currScoresCSIP.append(y[x])
            # print("currScoresRSSM values after assignment:", currScoresRSSM)
            bSignificantRSSM = [z for z in currScoresRSSM if (z > 4 or z < 2)]
            bSignificantCSIP = [z for z in currScoresCSIP if (z > 2 or z < 1)]
            if len(bSignificantRSSM) > 0 or len(bSignificantCSIP) > 0:
                currB += "Significant Factor(s) of \nInterest: \n"
            for i, s in enumerate(currScoresRSSM):
                #print(f"Score from beliefsRSSM for {rssmFactors[i]} is: {s}")

                if rssmFactors[i] == "Self-Esteem Frustration":
                    if 1.0 <= s <= 1.49:
                        currB += "- " + rssmFactors[i] + " (Very Low)" + "\n"
                    elif 1.5 <= s <= 1.99:
                        currB += "- " + rssmFactors[i] + " (Low)" + "\n"
                    elif 2.0 <= s <= 2.49:
                        currB += "- " + rssmFactors[i] + " (Low Average)" + "\n"
                    elif 2.5 <= s <= 3.5:
                        currB += "- " + rssmFactors[i] + " (Average)" + "\n"
                    elif 3.51 <= s <= 3.99:
                        currB += "- " + rssmFactors[i] + " (High Average)" + "\n"
                    elif 4.0 <= s <= 4.49:
                        currB += "- " + rssmFactors[i] + " (High)" + "\n"
                    elif 4.5 <= s <= 5.0:
                        currB += "- " + rssmFactors[i] + " (Very High)" + "\n"
                else:
                    if s > 4:
                        currB += "- " + rssmFactors[i] + " (Very High)" + "\n"
                    elif s < 2:
                        currB += "- " + rssmFactors[i] + " (Very Low)" + "\n"
            for i, s in enumerate(currScoresCSIP):
                if s > 2:
                    currB += "- " + csipFactors[i] + " (Very High)" + "\n"
                elif s < 1:
                    currB += "- " + csipFactors[i] + " (Very Low)" + "\n"
            if rs <= 1.39:
                currB += "- Rejection Sensitivity (Very Low)" + "\n"
            elif rs <= 5:
                currB += "- Rejection Sensitivity (Low)" + "\n"
            elif rs <= 15.85:
                currB += "- Rejection Sensitivity (High)" + "\n"
            elif rs > 15.85:
                currB += "- Rejection Sensitivity (Very High)" + "\n"

        if x != 0:
            bTexts.append(currB)
        else:
            all.append(final)

    for i in range (1, 5):
        idx = bOrder.index(max(bOrder))
        bOrder[idx] = -1
        all.append("#"+ str(i) + " " + bTexts[idx])

    return all