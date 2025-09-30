from app import create_app, db
from app.Model.models import Thoughtspositive, Thoughtsnegative, Feelingspositive, Feelingsnegative, Behaviormc

app = create_app()

@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Thoughtspositive.query.count() == 0:
        thoughtspos = ['I can handle this difficult task. With some effort, I can make things better in this situation. If I try hard enough, I can get what I want in this situation.',
                    'A burden has been lifted from my mind. A threat or harm has been removed from this situation.',
                    'I feel that things are going to be fine in this situation. Somehow things might work out in this situation. In the end, there’s a chance that everything  will be OK.',
                    'Someone else has been very helpful to me in this situation. I’ve been treated very well in this situation. Someone else deserves a lot of credit for this good situation.',
                    'There is nothing I need to be doing right now. Everything is fine for now. For the moment, there is nothing I need to be concerned about.',
                    'I’m very pleased with what I’ve accomplished here. I had a role in things turning out great. I deserve credit for what I’ve done.',
                    'Things turned out great. I’ve gotten what I wanted in this situation. Things have gone wonderfully well in this situation.',
                    'I am accepted. They appreciate me for who I am. They like me.',
                    'This is interesting, engaging. This is something I enjoy giving my full attention to.',
                    'I had fun. This was enjoyable. I had a good time.'
                    ]
        for t in thoughtspos:
            db.session.add(Thoughtspositive(name=t))
    if Thoughtsnegative.query.count() == 0:

        thoughtsneg = ['Someone or something is getting in my way. This is interfering with what I want. My efforts have been blocked.', 
                    'I was hoping for better. That was not what I wanted.',
                    'I am not wanted. I have been rejected. They disapprove of or dislike me.',
                    'I’ve been dealt with shabbily. I’ve been cheated or wronged. Someone else is to blame for this bad situation. I’ve been mistreated.',
                    'I don’t know whether I can handle what is happening or about to happen. I might not be able to deal with it. Something bad might happen.',
                    'I don’t know why things are going so badly. I don’t understand why things are not better. This isn’t the way things should be.',
                    'I should have done something differently in this situation. I wish I hadn’t done what I’ve done',
                    'This situation is not what I expected it to be. I never would have guessed that this would happen.  What is happening here could not be predicted.' ,
                    'I am to blame for this bad situation. Things are bad because of me. I’ve done something wrong.'  
                    ]
        for t in thoughtsneg:
            db.session.add(Thoughtsnegative(name=t))
    if Feelingspositive.query.count() == 0:
        feelingspos = ['Interested, involved, intrigued',
        'Eager, determined',
        'Joyful, happy, lighthearted',
       'Tranquil, calm, serene',
       'Relieved',
       'Surprised, amazed, astonished',
       'Hopeful, optimistic',
       'Proud, pleased, triumphant',
       'Grateful, appreciative, thankful',
       'Accepted, liked, appreciated',
       'Excited, stimulated, passionate',
       'Pleasurable, enjoyment, fun'
        ]
        for t in feelingspos:
            db.session.add(Feelingspositive(name=t))
    if Feelingsnegative.query.count() == 0:
        feelingsneg = ['Bored, indifferent, apathetic',
        'Guilty, remorseful, ashamed',
        'Sad, depressed, unhappy',
        'Nervous, anxious, tense',
        'Annoyed, resentful, irritated',
        'Angry, pissed off, mad',
        'Regretful, dissatisfied, disappointed in myself',
        'Defeated, resigned',
        'Afraid, fear, scared',
        'Frustrated, exasperated',
        'Concerned, worried']
        for t in feelingsneg:
            db.session.add(Feelingsnegative(name=t))
    if Behaviormc.query.count() == 0:
        behavior = [
            'To connect, feel closer to someone, accepted/liked',
            'To do something well, be effective, accomplish something',
            'To get something I wanted',
            'To help, offer assistance, be supportive',
            'To understand, learn, figure something out',
            'To be authentic, real, honest',
            'To not embarrass myself, not say/do something stupid',
            'To make my own decision, have a feeling of choice, do what I want',
            'To correct something that someone else did that was unfair, not right',
            'To meet someone else’s expectations, not make them angry or to disappoint them',
            'To get away from something that I didn’t like',
            'To get support, help/assistance from others',
            'To make up for harm I’ve caused',
            'To avoid something that made me too anxious',
            'To get to a safe place, escape from something that seemed threatening, dangerous'

        ]
        for t in behavior:
            db.session.add(Behaviormc(name=t))
        # for t in thoughtsneg:
        #     db.session.add(Thoughtsnegative(name=t))
        # for t in feelingspos:
        #     db.session.add(Feelingspositive(name=t))
        # for t in feelingsneg:
        #     db.session.add(Feelingsnegative(name=t))
        # for t in behavior:
        #     db.session.add(Behaviormc(name=t))
    db.session.commit()
    


if __name__ == "__main__":
    app.run(debug=True)