import pdb

from flask_login import login_user, logout_user

from . import client
from models import Customer, User
from app import db



def test_DeleteUser_Success(client):
    admin = User(username='testuser999', email='testemai999@example.com', role='admin')
    admin.set_password('testpassword')
    db.session.add(admin)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser999',
        'password': 'testpassword',
        'role': 'regular',
    })

    add_user = {
        'username': 'testuser888',
        'email': 'testuser888@example.com',
        'password': 'testpassword',

    }

    client.post('/add-user', data=add_user)
    user = User.query.filter_by(username='testuser888').first()
    response = client.get(f'/delete-user/{user.id}', data=add_user)

    assert response.status_code == 302
    assert response.data == b'User Deleted'
    db.session.delete(admin)
    db.session.commit()

