from flask import render_template, flash, redirect, url_for, make_response
from flask import request
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from flask_migrate import Migrate

from models import User, Customer
from flask import Flask
from database import db
from sqlalchemy import text

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    # Check if a token or other non-cookie authentication is being used
    token = request.headers.get('Authorization')
    if token:
        # Use the token to find and return the user
        user = User.query.filter_by(api_token=token).first()
        if user:
            return user
    # If no token is found, return None to indicate that no user was authenticated
    return None


@app.route('/')
@login_required
def index():
    # Get All the users from the Database
    users = User.query.all()

    # Get All the Customers from the Database
    customers = Customer.query.all()

    # 'user' is the current user in the session
    # 'customers' list of Customers
    # 'users' list of Users
    return render_template('index.html', user=current_user, customers=customers, users=users)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['cpassword']
        email = request.form['email']

        if password != confirm_password:
            flash('Password Does not Match.')
            response = make_response(redirect(url_for('register')))
            response.data = b'Password Does not Match.'
            return response
        
        if len(password) < 8:
            flash('Password Does not meet the required length')
            response = make_response(redirect(url_for('register')))
            response.data = b'Password Does not meet the required length'
            return response

        user_by_username = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()

        if user_by_username:
            flash('Username already exists.')
            response = make_response(redirect(url_for('register')))
            response.data = b'Username already exists.'
            return response
            # return redirect(url_for('register'))
        elif user_by_email:
            flash('Email already exists. Please Sign-in')
            response = make_response(redirect(url_for('login')))
            response.data = b'Email already exists.'
            return response
            # return redirect(url_for('login'))
        else:
            new_user = User(username=username, email=email)

            # Hashing the Password
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully.')
            response = make_response(redirect(url_for('login')))
            response.data = b'Account created successfully.'
            return response

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            flash("You are already logged in.")
            return redirect(url_for('index'))
        return render_template('login.html', role='User')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Invalid username or password.')

            if role.lower() == 'admin':
                response = make_response(redirect(url_for('admin')))
                response.data = b'Invalid username or password.'
                return response
            else:
                response = make_response(redirect(url_for('login')))
                response.data = b'Invalid username or password.'
                return response

        login_user(user)

        flash('Logged in successfully.')
        response = make_response(redirect(url_for('index')))
        response.data = b'Logged in successfully.'
        return response


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html', role='Admin')


@app.route('/reset-password', methods=['POST'])
@login_required
def resetPassword():
    current_pass = request.form['cpass']
    new_pass = request.form['npass']
    confirm_pass = request.form['cnpass']
    if current_user.check_password(current_pass):
        if new_pass == confirm_pass and len(new_pass) < 8:
            current_user.set_password(confirm_pass)
            db.session.commit()
            flash("Password Updated.")
            response = make_response(redirect(url_for('index')))
            response.data = b'Password Updated.'
            return response
        else:
            flash("Password Does not Matched.")
            response = make_response(redirect(url_for('index')))
            response.data = b'Password Does not Matched.'
            return response
    else:
        flash("Incorrect Current Password.")
        response = make_response(redirect(url_for('index')))
        response.data = b'Incorrect Current Password.'
        return response


@app.route('/add-customer', methods=['POST'])
@login_required
def addCustomer():
    if not current_user.is_authenticated:
        response = make_response(redirect(url_for('index')))
        response.data = b'Unauth'
        return response
    customer = Customer(first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'],
                        account_number=request.form['account'], balance=request.form['balance'],
                        user_id=current_user.id, sort_code=request.form['scode'])
    db.session.add(customer)
    db.session.commit()

    flash("Customer Added")
    response = make_response(redirect(url_for('index')))
    response.data = b'Customer Added'
    return response


@app.route('/add-user', methods=['POST'])
@login_required
def addUser():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists.')
        response = make_response(redirect(url_for('index')))
        response.data = b'Username already exists.'
        return response
    else:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully.')
        response = make_response(redirect(url_for('index')))
        response.data = b'Account created successfully.'
        return response


@app.route('/delete-user/<user_id>', methods=['GET'])
def deleteUser(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    customers = Customer.query.filter_by(user_id=int(user_id))
    for customer in customers:
        db.session.delete(customer)

    db.session.delete(user)

    db.session.commit()
    flash("User Deleted")
    response = make_response(redirect(url_for('index')))
    response.data = b'User Deleted'
    return response


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.')
    return redirect(url_for('login'))


@app.route('/customer/<cus_id>')
@login_required
def customer(cus_id):
    customer = Customer.query.filter_by(id=cus_id).first()

    return render_template('customer.html', customer=customer, user=current_user)


@app.route('/update-customer/<cus_id>', methods=['POST'])
def updateCustomer(cus_id):
    customer = Customer.query.filter_by(id=cus_id).first()

    customer.first_name = request.form['fname']
    customer.last_name = request.form['lname']
    customer.email = request.form['email']
    customer.account_number = request.form['account']
    customer.sort_code = request.form['scode']
    customer.balance = request.form['balance']

    db.session.commit()
    flash(f"Customer with ID: {customer.id} updated")

    return redirect(url_for('index'))


@app.route('/delete-customer/<cus_id>')
@login_required
def deleteCustomer(cus_id):
    customer = Customer.query.filter_by(id=cus_id).first()

    db.session.delete(customer)
    db.session.commit()

    flash(f"Customer with ID: {cus_id} Deleted")
    response = make_response(redirect(url_for('index')))
    response.data = b'Customer Deleted'
    return response


@app.route('/test')
def test():
    return render_template('login.html')


print(__name__)
if __name__ == '__main__':
    app.app_context().push()
    app.run()
