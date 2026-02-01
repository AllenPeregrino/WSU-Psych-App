# These tests use Flask's test client and a mocked MongoDB instance (via mongomock)
# to test the behavior of key routes in the application. We're focusing on:
# - Route-level integration (simulating requests/responses)
# - Access control (e.g., login-required views)
# - Page rendering and expected content
# - Mocking external services like OpenAI and Qualtrics reporting

import pytest
import mongomock
from mongoengine import connect, disconnect
from flask import url_for
from app import create_app
from app.Model.models import User, Survey, Signature
from unittest.mock import patch

# Creates a test client and replaces MongoDB with in-memory mock (mongomock)
@pytest.fixture(scope='function')
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    disconnect(alias='default')
    connect('testdb', alias='default', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    for model in [User, Survey, Signature]:
        model.drop_collection()

    ctx.pop()
    disconnect(alias='default')

# Inserts a new user (regular or admin) for use in route tests
def create_user(username, password, email, admin=0):
    user = User(username=username, email=email, admin=admin)
    user.set_password(password)
    user.save()
    return user

# Integration Test: User login and logout flow
def test_login_logout(client):
    create_user("selinanguyen", "1234", "selina@wsu.edu")

    response = client.post('/login', data={
        'username': 'selinanguyen',
        'password': '1234',
        'remember_me': False
    }, follow_redirects=True)
    assert b"Welcome to the Mindful Portal!" in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b"Sign In" in response.data

# Integration Test: Admin user sees admin landing page
def test_admin_login_redirect(client):
    create_user("walt", "1234", "walt@wsu.edu", admin=1)

    response = client.post('/login', data={
        'username': 'walt',
        'password': '1234',
        'remember_me': False
    }, follow_redirects=True)
    assert b"Welcome to the Admin Mindful Portal!" in response.data

    response = client.get('/logout', follow_redirects=True)
    assert b"Sign In" in response.data

# Index should redirect to login if not authenticated
def test_access_index_requires_login(client):
    response = client.get('/index', follow_redirects=True)
    assert b"Sign In" in response.data

# Past Situations page loads after login
def test_past_situations_page(client):
    user = create_user("aaron", "1234", "aaron@wsu.edu")

    client.post('/login', data={
        'username': 'aaron',
        'password': '1234'
    }, follow_redirects=True)

    response = client.get('/pastSituations', follow_redirects=True)
    assert b"Past Situations" in response.data

# Information page renders for authenticated users
def test_information_page(client):
    user = create_user("selina", "1234", "selina@wsu.edu")

    client.post('/login', data={
        'username': 'selina',
        'password': '1234'
    }, follow_redirects=True)

    response = client.get('/information', follow_redirects=True)
    assert b"Information" in response.data

def test_qsort_page_access(client):
    create_user("admin", "admin123", "admin@wsu.edu", admin=1)

    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)

    response = client.get('/qsort', follow_redirects=True)
    assert b"User Qsort Entry" in response.data

def test_admin_index_view(client):
    create_user("admin", "admin123", "admin@wsu.edu", admin=1)

    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)

    response = client.get('/admin_index', follow_redirects=True)
    assert b"Admin" in response.data or b"Users" in response.data

# Integration Test: Search page loads after login
def test_search_page_access(client):
    create_user("selina", "1234", "selina@wsu.edu")

    client.post('/login', data={
        'username': 'selina',
        'password': '1234'
    }, follow_redirects=True)

    response = client.get('/search', follow_redirects=True)
    assert b"Search" in response.data

# Integration Test: Handles error if generate_report fails due to missing file
# Patches out the external CSV + report functions so we can test logic without file dependencies
@patch('app.Controller.routes.get_survey', return_value=None)
@patch('app.Controller.routes.create_report', return_value=None)
def test_generate_report_fail_if_missing_file(mock_report, mock_get_survey, client):
    create_user("admin", "admin123", "admin@wsu.edu", admin=1)

    client.post('/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)

    response = client.get('/generate_report')
    assert b"Error generating report" in response.data or response.status_code == 500