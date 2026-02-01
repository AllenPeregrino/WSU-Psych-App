import pytest
import mongomock
from mongoengine import connect, disconnect

from app.Model.models import (
    User, Survey, Feelingspositive, Feelingsnegative,
    Thoughtspositive, Thoughtsnegative, Behaviormc,
    Signature, SituationList
)

# Use mongomock to simulate an in-memory MongoDB for safe, isolated tests
@pytest.fixture(autouse=True)
def mongo_mock():
    connect("testdb", host="mongodb://localhost", mongo_client_class=mongomock.MongoClient)
    yield
    for model in [User, Survey, Feelingspositive, Feelingsnegative, Thoughtspositive, Thoughtsnegative, Behaviormc, Signature, SituationList]:
        model.drop_collection()
    disconnect()

# Test hashing and checking a user password
def test_user_password_hashing():
    u = User(username="john", firstname="John", lastname="Yate", email="john.yates@wsu.edu")
    u.set_password("covid")
    assert not u.get_password("flu")
    assert u.get_password("covid")

# Test password hashing for multiple users with correct and incorrect passwords
def test_password_hashing_multiple():
    users = [
        ("selinanguyen", "1234", "123"),
        ("Oni", "test1234", "test"),
        ("aaronluck", "test#001", "test"),
    ]
    for uname, correct_pw, wrong_pw in users:
        u = User(username=uname, email=f"{uname}@wsu.edu")
        u.set_password(correct_pw)
        u.save()
        assert u.get_password(correct_pw)
        assert not u.get_password(wrong_pw)

# Test creating a Survey and associating it with a User
def test_create_survey():
    user = User(username="selina", firstname="Selina", lastname="Nguyen", email="selina@wsu.edu")
    user.set_password("1234")
    user.save()

    survey = Survey(user=user, thoughts_meaning_of_event="this is a thought", behaviors_description="desc").save()
    assert survey.user.id == user.id
    assert survey.thoughts_meaning_of_event == "this is a thought"

# Test setting and retrieving specific survey fields
def test_survey_fields():
    s = Survey(thoughts_meaning_of_event='test3', behaviors_description='test7').save()
    assert s.behaviors_description == 'test7'
    assert s.thoughts_meaning_of_event != 'test10'

# Test that a survey correctly references its associated user
def test_survey_user_relationship():
    u = User(username='aaron', email='aaron@wsu.edu').save()
    survey = Survey(user=u).save()
    assert survey.user.id == u.id

#  Test creating an admin user and verifying credentials and admin flag
def test_creating_admin_user():
    u = User(username='walt', firstname='walt', lastname='scott', email='walt@wsu.edu', admin=1).save()
    u.set_password('1234')
    assert u.admin == 1
    assert u.get_password('1234')

# Test saving and retrieving positive feelings, thoughts, and behaviors from survey
def test_positive_choices_retrieval():
    u = User(username='aaron', email='aaron@wsu.edu').save()
    survey = Survey(user=u).save()

    fp = Feelingspositive(name="Interested").save()
    tp = Thoughtspositive(name="A burden has been lifted").save()
    beh = Behaviormc(name="To connect").save()

    survey.feelings_pos = [str(fp.id)]
    survey.thoughts_pos = [str(tp.id)]
    survey.behaviors_mc = [str(beh.id)]
    survey.save()

    assert survey.get_feelingspos()[0].name == "Interested"
    assert survey.get_thoughtspos()[0].name.startswith("A burden")
    assert survey.get_behaviors()[0].name.startswith("To connect")

# Test saving and retrieving negative feelings and thoughts from survey
def test_negative_choices_retrieval():
    u = User(username='aaron', email='aaron@wsu.edu').save()
    survey = Survey(user=u).save()

    fn = Feelingsnegative(name="Bored").save()
    tn = Thoughtsnegative(name="I don’t know whether I can handle...").save()

    survey.feelings_neg = [str(fn.id)]
    survey.thoughts_neg = [str(tn.id)]
    survey.save()

    assert "Bored" in survey.get_feelingsneg()[0].name
    assert "handle" in survey.get_thoughtsneg()[0].name

# Test linking a SituationList entry to a Signature and verifying the connection
def test_signature_and_situationlist():
    u = User(username="aaron", email="aaron@wsu.edu").save()
    sig = Signature(user=u, ifThen="If stressed, then breathe").save()
    situation = SituationList(signature=sig, situation="During class").save()

    sig.situationList = [situation]
    sig.save()

    assert sig.situationList[0].situation == "During class"
    assert sig.user.id == u.id

# Test that Signature and Survey can reference each other correctly
def test_signature_links_to_survey():
    user = User(username='sam', email='sam@wsu.edu').save()
    sig = Signature(user=user, ifThen="If sad, then journal").save()
    survey = Survey(user=user, signature=sig).save()

    sig.survey = survey
    sig.save()

    assert sig.survey.id == survey.id
    assert survey.signature.id == sig.id