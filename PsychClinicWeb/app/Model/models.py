from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


surveyThoughtsPos=db.Table('surveyThoughtsPos',
                 db.Column('survey_id',db.Integer, db.ForeignKey('survey.id')),
                  db.Column('thoughtspositive_id',db.Integer, db.ForeignKey('thoughtspositive.id'))
                )           
surveyThoughtsNeg=db.Table('surveyThoughtsNeg',
                 db.Column('survey_id',db.Integer, db.ForeignKey('survey.id')),
                  db.Column('thoughtsnegative_id',db.Integer, db.ForeignKey('thoughtsnegative.id'))
                )    
surveyFeelingsPos=db.Table('surveyFeelingsPos',
                 db.Column('survey_id',db.Integer, db.ForeignKey('survey.id')),
                  db.Column('feelingspositive_id',db.Integer, db.ForeignKey('feelingspositive.id'))
                )       

surveyFeelingsNeg=db.Table('surveyFeelingsNeg',
                 db.Column('survey_id',db.Integer, db.ForeignKey('survey.id')),
                  db.Column('feelingsnegative_id',db.Integer, db.ForeignKey('feelingsnegative.id'))
        )

surveyBehaviorMc=db.Table('surveyBehaviorMc',
                 db.Column('survey_id',db.Integer, db.ForeignKey('survey.id')),
                  db.Column('behaviormc_id',db.Integer, db.ForeignKey('behaviormc.id'))
        )
class Thoughtspositive(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    
    def __repr__(self):
        return '<ID: {} Thoughts Positive {} >'.format(self.id, self.name)

class Thoughtsnegative(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    
    def __repr__(self):
        return '<ID: {} Thoughts Negative {} >'.format(self.id, self.name)

class Feelingspositive(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    
    def __repr__(self):
        return '<ID: {} Feelings Positive {} >'.format(self.id, self.name)

class Feelingsnegative(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    
    def __repr__(self):
        return '<ID: {} Feelings Negative {} >'.format(self.id, self.name)

class Behaviormc(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20))
    
    def __repr__(self):
        return '<ID: {} Behavior MC {} >'.format(self.id, self.name)

class User(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email= db.Column(db.String(120),unique=True,index=True)
    password_hash=db.Column(db.String(128))
    survey=db.relationship('Survey', backref='writer', lazy='dynamic')
    #1 is admin, 0 are normal users
    admin = db.Column(db.Integer)
    signature = db.relationship('Signature', backref='User', lazy='dynamic')

    def repr(self):
        return '<ID: {} Username: {}>'.format(self.id,self.username)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password_hash,password)

class Signature(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    ifThen = db.Column(db.String(100))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    survey_id=db.relationship('Survey', backref='Signature', lazy=True)
    situationList = db.relationship('SituationList', backref='writer', lazy=True)

class Survey(db.Model, UserMixin):
    signature_id = db.Column(db.Integer,db.ForeignKey('signature.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    thoughts_pos= db.relationship('Thoughtspositive', secondary=surveyThoughtsPos,primaryjoin=(surveyThoughtsPos.c.survey_id==id), backref=db.backref('surveyThoughtsPos',lazy='dynamic'), lazy='dynamic')
    thoughts_neg= db.relationship('Thoughtsnegative', secondary=surveyThoughtsNeg,primaryjoin=(surveyThoughtsNeg.c.survey_id==id), backref=db.backref('surveyThoughtsNeg',lazy='dynamic'), lazy='dynamic')
    
    feelings_pos= db.relationship('Feelingspositive', secondary=surveyFeelingsPos,primaryjoin=(surveyFeelingsPos.c.survey_id==id), backref=db.backref('surveyFeelingsPos',lazy='dynamic'), lazy='dynamic')
    feelings_neg= db.relationship('Feelingsnegative', secondary=surveyFeelingsNeg,primaryjoin=(surveyFeelingsNeg.c.survey_id==id), backref=db.backref('surveyFeelingsNeg',lazy='dynamic'), lazy='dynamic')
    behaviors_mc= db.relationship('Behaviormc', secondary=surveyBehaviorMc,primaryjoin=(surveyBehaviorMc.c.survey_id==id), backref=db.backref('surveyBehaviorMc',lazy='dynamic'), lazy='dynamic')
    

    situation = db.Column(db.String(30))

    what_happened = db.Column(db.String(150))

    thoughts_meaning_of_event = db.Column(db.String(150))
    thoughts_summary = db.Column(db.String(50))

    behaviors_description = db.Column(db.String(150))
    behaviors_outcome = db.Column(db.String(150))
    
   
   
    def get_thoughtspos(self):
        return self.thoughts_pos
    def get_thoughtsneg(self):
        return self.thoughts_neg
    def get_feelingspos(self):
        return self.feelings_pos
    def get_feelingsneg(self):
        return self.feelings_neg
    def get_behaviors(self):
        return self.behaviors_mc
    def get_situationList(self):
        return self.situationlist
    def get_thoughtspos2(self):
       test =[]
       for t in self.thoughts_pos:
           test.append(t.thoughtspositive_id)
           
    

class SituationList(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    signature_id = db.Column(db.Integer,db.ForeignKey('signature.id'))
    situation = db.Column(db.String(30))


