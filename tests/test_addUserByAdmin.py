import pdb

from flask_login import login_user, logout_user

from . import client
from models import Customer, User
from app import db



def test_addUser_Success(client):
    admin = User(username='testuser4343', email='testemail4343@example.com', role='admin')
    admin.set_password('testpassword')
    db.session.add(admin)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    add_user = {
        'username': 'testuser222',
        'email': 'testemail111@example.com',
        'password': 'testpassword',

    }
    response = client.post('/add-user', data=add_user)

    assert response.status_code == 302
    assert response.data == b'Account created successfully.'
    user = User.query.filter_by(username='testuser222').first()
    db.session.delete(admin)
    db.session.delete(user)
    db.session.commit()


def test_addUser_UserExist(client):
    admin = User(username='testuser4343', email='testemail4343@example.com', role='admin')
    admin.set_password('testpassword')
    db.session.add(admin)
    db.session.commit()

    user = User(username='testuser0000', email='testuser0000@example.com')
    user.set_password('testpassword')
    db.session.add(user)
    db.session.commit()

    # Admin Login
    client.post('/login', data={
        'username': 'testuser4343',
        'password': 'testpassword',
        'role': 'regular',
    })

    reset_form = {
        'username': 'testuser0000',
        'email': 'testuser0000@example.com',
        'password': 'testpassword',

    }
    response = client.post('/add-user', data=reset_form)

    assert response.status_code == 302
    assert response.data == b'Username already exists.'
    db.session.delete(admin)
    db.session.delete(user)
    db.session.commit()
