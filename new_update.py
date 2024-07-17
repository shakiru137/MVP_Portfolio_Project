#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

"""
Flask Banking Application

This is a simple Flask application that demonstrates basic banking functionalities such as creating an account, logging in, withdrawing money, depositing money, and sending money between accounts.

The application uses MySQL as its database and requires the following environment variables to be set:

- DB_HOST: The hostname or IP address of the MySQL server.
- DB_USER: The username to connect to the MySQL server.
- DB_PASSWORD: The password to connect to the MySQL server.
- DB_NAME: The name of the MySQL database to use.

To run the application, simply execute the following command:

    python3 app.py

The application will be available at http://localhost:5000.
"""

""" Database Configuration """
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'oluwasegun137'
DB_NAME = 'mybank'

""" Connect to MySQL database """
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

""" Create a cursor object to execute SQL queries  """
db_cursor = db_connection.cursor()

def is_valid_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False

@app.route('/')
def index():
    """Render index page."""
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """Create a new account."""
    if request.method == 'POST':
        """ Retrieve form data """
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        """ Save account to database """
        db_cursor.execute("INSERT INTO accounts (name, username, password, balance) VALUES (%s, %s, %s, %s)",
                       (name, username, password, 0))
        db_connection.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('create_account'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to an existing account."""
    if request.method == 'POST':
        """ Retrieve form data """
        username = request.form['username']
        password = request.form['password']

        """ Check credentials """
        db_cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = db_cursor.fetchone()

        if account:
            return render_template('account.html', account=account)
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

@app.route('/withdraw_money/<int:account_id>', methods=['GET', 'POST'])
def withdraw_money(account_id):
    """Withdraw money from an account."""
    """ Retrieve account details """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('withdraw_money.html', account=account)

        amount = float(amount)
        """ Retrieve account balance """
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        if current_balance >= amount:
            new_balance = current_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
            db_connection.commit()

            flash('Withdrawal successful!', 'success')
            """ Redirect to prevent form resubmission """
            return render_template('withdraw_money.html', account=account)
            # return redirect(url_for('account', account_id=account_id))
        else:
            flash('Insufficient funds!', 'error')

    return render_template('withdraw_money.html', account=account)

@app.route('/deposit_money/<int:account_id>', methods=['GET', 'POST'])
def deposit_money(account_id):
    """Deposit money to an account."""
    """ Retrieve account details """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('deposit_money.html', account=account)

        amount = float(amount)
        """ Retrieve account balance """
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        new_balance = current_balance + amount
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
        db_connection.commit()

        flash('Deposit successful!', 'success')
        """ Redirect to prevent form resubmission """
        return render_template('deposit_money.html', account=account)
        # return redirect(url_for('account', account_id=account_id))

    return render_template('deposit_money.html', account=account)

def process_transaction(sender_id, recipient_id, amount):
    # Convert amount to float and validate
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError as e:
        return str(e)

    try:
        # Begin transaction
        db_connection.start_transaction()

        # Retrieve sender's balance
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", (sender_id,))
        sender_balance_row = db_cursor.fetchone()
        if sender_balance_row is None:
            raise ValueError("Sender account not found")
        sender_balance = sender_balance_row[0]

        # Check if sender has enough balance
        if sender_balance < amount:
            raise ValueError("Insufficient funds")

        # Retrieve recipient's balance
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s FOR UPDATE", (recipient_id,))
        recipient_balance_row = db_cursor.fetchone()
        if recipient_balance_row is None:
            raise ValueError("Recipient account not found")
        recipient_balance = recipient_balance_row[0]

        # Update balances
        new_sender_balance = sender_balance - amount
        new_recipient_balance = recipient_balance + amount
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_sender_balance, sender_id))
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_recipient_balance, recipient_id))

        # Commit transaction
        db_connection.commit()

        return "Transaction successful"
    except mysql.connector.Error as err:
        # Rollback in case of error
        db_connection.rollback()
        return f"Error: {err}"
    except ValueError as e:
        # Rollback in case of validation error
        db_connection.rollback()
        return str(e)

@app.route('/send_money/<int:sender_id>', methods=['GET', 'POST'])
def send_money(sender_id):
    """Send money from one account to another."""
    """ Retrieve sender's account details """
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

        result = process_transaction(sender_id, recipient_id, amount)
        flash(result, 'success' if result == "Transaction successful" else 'error')

        return render_template('send_money.html', account=sender_account)

    return render_template('send_money.html', account=sender_account)

@app.route('/account/<int:account_id>')
def account(account_id):
    """Display account details."""
    """ Retrieve account details """
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if account:
        return render_template('account.html', account=account, account_id=account_id)
    else:
        return render_template('404.html'), 404

@app.route('/service/', methods=['GET', 'POST'])
def service():
    """Render service page."""
    return render_template('service.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
    """Render About page."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

