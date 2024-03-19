import pdb

from flask_login import login_user, logout_user

from . import client
from models import Customer, User
from app import db



def test_resetPassword_success(client):

    user = User(username='testuser4343', email='testemail4343@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    reset_form = {
        'cpass': 'testpassword',
        'npass': 'testpassword123',
        'cnpass': 'testpassword123',
    }
    response = client.post('/reset-password', data=reset_form)

    assert response.status_code == 302
    assert response.data == b'Password Updated.'
    db.session.delete(user)
    db.session.commit()


def test_resetPassword_wrongCurrentpass(client):
    user = User(username='testuser4343', email='testemail4343@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    reset_form = {
        'cpass': 'testpassword321',
        'npass': 'testpassword123',
        'cnpass': 'testpassword123',
    }
    response = client.post('/reset-password', data=reset_form)

    assert response.status_code == 302
    assert response.data == b'Incorrect Current Password.'
    db.session.delete(user)
    db.session.commit()

def test_resetPassword_unMatchedPass(client):
    user = User(username='testuser4343', email='testemail4343@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    reset_form = {
        'cpass': 'testpassword',
        'npass': 'testpassword123',
        'cnpass': 'testpassword321',
    }
    response = client.post('/reset-password', data=reset_form)

    assert response.status_code == 302
    assert response.data == b'Password Does not Matched.'

    db.session.delete(user)
    db.session.commit()