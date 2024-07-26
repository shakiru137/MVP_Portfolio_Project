#!/usr/bin/env python3
"""
This module sets up a Flask application for a banking system with basic functionalities
such as account creation, login, deposit, withdrawal, money transfer, and transaction history.
It uses MySQL as the database and bcrypt for password hashing.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import mysql.connector

# Initialize the Flask application
app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'oluwasegun137'
DB_NAME = 'mybank'

# Establish a connection to the MySQL database
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

# Create a cursor object to interact with the database
db_cursor = db_connection.cursor()

# Initialize bcrypt for password hashing
bcrypt = Bcrypt(app)

def is_valid_amount(amount):
    """
    Validates if the input amount is a positive number.

    :param amount: The amount to validate
    :return: True if the amount is valid, False otherwise
    """
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False

@app.route('/')
def index():
    """
    Renders the home page.

    :return: Rendered HTML of the home page
    """
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """
    Handles account creation. Hashes the password and stores the account details in the database.

    :return: Rendered HTML of the account creation page or redirects to the same page after account creation
    """
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db_cursor.execute("INSERT INTO accounts (name, username, password, balance) VALUES (%s, %s, %s, %s)",
                          (name, username, hash_password, 0))
        db_connection.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('create_account'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login by verifying the username and password.

    :return: Rendered HTML of the login page or account page if login is successful
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = db_cursor.fetchone()

        if account and bcrypt.check_password_hash(account[3], password):
            return render_template('account.html', account=account)
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')

def log_transaction(account_id, transaction_type, amount):
    """
    Logs a transaction in the database.

    :param account_id: ID of the account
    :param transaction_type: Type of transaction (withdrawal, deposit, transfer, receive)
    :param amount: Amount involved in the transaction
    """
    db_cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", 
                      (account_id, transaction_type, amount))
    db_connection.commit()

@app.route('/withdraw_money/<int:account_id>', methods=['GET', 'POST'])
def withdraw_money(account_id):
    """
    Handles money withdrawal from an account.

    :param account_id: ID of the account
    :return: Rendered HTML of the withdrawal page
    """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('withdraw_money.html', account=account)

        amount = float(amount)
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        if current_balance >= amount:
            new_balance = current_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
            db_connection.commit()
            log_transaction(account_id, 'withdrawal', amount)

            flash('Withdrawal successful!', 'success')
            return render_template('withdraw_money.html', account=account)
        else:
            flash('Insufficient funds!', 'error')

    return render_template('withdraw_money.html', account=account)

@app.route('/deposit_money/<int:account_id>', methods=['GET', 'POST'])
def deposit_money(account_id):
    """
    Handles money deposit into an account.

    :param account_id: ID of the account
    :return: Rendered HTML of the deposit page
    """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('deposit_money.html', account=account)

        amount = float(amount)
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        new_balance = current_balance + amount
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
        db_connection.commit()
        log_transaction(account_id, 'deposit', amount)

        flash('Deposit successful!', 'success')
        return render_template('deposit_money.html', account=account)

    return render_template('deposit_money.html', account=account)

@app.route('/send_money/<int:sender_id>', methods=['GET', 'POST'])
def send_money(sender_id):
    """
    Handles money transfer between accounts.

    :param sender_id: ID of the sender's account
    :return: Rendered HTML of the send money page
    """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (sender_id,))
    sender_account = db_cursor.fetchone()

    if request.method == 'POST':
        recipient_id = request.form['recipient_id']
        amount = request.form['amount']

        if not recipient_id.isdigit() or not is_valid_amount(amount):
            flash('Invalid input. Please enter a valid recipient ID and a positive amount.', 'error')
            return render_template('send_money.html', account=sender_account)

        recipient_id = int(recipient_id)
        amount = float(amount)

        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (sender_id,))
        sender_balance = db_cursor.fetchone()[0]

        if sender_balance >= amount:
            new_sender_balance = sender_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_sender_balance, sender_id))

            db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (recipient_id,))
            recipient_balance_row = db_cursor.fetchone()

            if recipient_balance_row is not None:
                recipient_balance = recipient_balance_row[0]
                new_recipient_balance = recipient_balance + amount
                db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_recipient_balance, recipient_id))

                db_connection.commit()
                log_transaction(sender_id, 'transfer', amount)
                log_transaction(recipient_id, 'receive', amount)

                flash('Money sent successfully!', 'success')
                return render_template('send_money.html', account=sender_account)
            else:
                flash('Recipient account not found!', 'error')
        else:
            flash('Insufficient funds!', 'error')

    return render_template('send_money.html', account=sender_account)

@app.route('/account/<int:account_id>')
def account(account_id):
    """
    Displays account details.

    :param account_id: ID of the account
    :return: Rendered HTML of the account page or 404 page if account not found
    """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if account:
        return render_template('account.html', account=account, account_id=account_id)
    else:
        return render_template('404.html'), 404

@app.route('/transaction_history/<int:account_id>')
def transaction_history(account_id):
    """
    Displays transaction history for an account.

    :param account_id: ID of the account
    :return: Rendered HTML of the transaction history page
    """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    db_cursor.execute("SELECT * FROM transactions WHERE account_id = %s ORDER BY timestamp DESC", (account_id,))
    transactions = db_cursor.fetchall()

    return render_template('transaction_history.html', transactions=transactions, account=account)

@app.route('/service/', methods=['GET', 'POST'])
def service():
    """
    Renders the service page.

    :return: Rendered HTML of the service page
    """
    return render_template('service.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
    """
    Renders the about page.

    :return: Rendered HTML of the about page
    """
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
