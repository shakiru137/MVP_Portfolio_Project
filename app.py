#!/usr/bin/env python3
# Import necessary libraries and modules
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector


# Initialize Flask application
app = Flask(__name__, static_folder='static')

# Set a secret key for session management in Flask
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
# Database connection details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'oluwasegun137'
DB_NAME = 'mybank'

""" Connect to MySQL database """
# Establish connection to the MySQL database
db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

""" Create a cursor object to execute SQL queries """
# Create a cursor object to interact with the database
db_cursor = db_connection.cursor()

# Function to validate if the amount is a positive number
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
        # Get form data from the request
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        """ Save account to database """
        # Insert new account details into the database
        db_cursor.execute("INSERT INTO accounts (name, username, password, balance) VALUES (%s, %s, %s, %s)",
                       (name, username, password, 0))
        db_connection.commit()  # Commit the transaction

        flash('Account created successfully!', 'success')  # Flash success message
        return redirect(url_for('create_account'))  # Redirect to create account page

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login to an existing account."""
    if request.method == 'POST':
        """ Retrieve form data """
        # Get form data from the request
        username = request.form['username']
        password = request.form['password']

        """ Check credentials """
        # Check if the provided credentials match any account in the database
        db_cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = db_cursor.fetchone()  # Fetch the account details

        if account:
            return render_template('account.html', account=account)  # Render account page if credentials are valid
        else:
            return render_template('login.html', error='Invalid credentials')  # Show error if credentials are invalid

    return render_template('login.html')

@app.route('/withdraw_money/<int:account_id>', methods=['GET', 'POST'])
def withdraw_money(account_id):
    """Withdraw money from an account."""
    """ Retrieve account details """
    # Retrieve account details from the database
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        # Get withdrawal amount from the form
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')  # Show error for invalid amount
            return render_template('withdraw_money.html', account=account)

        amount = float(amount)
        """ Retrieve account balance """
        # Retrieve current balance from the database
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        if current_balance >= amount:
            new_balance = current_balance - amount  # Calculate new balance after withdrawal
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))  # Update balance in database
            db_connection.commit()  # Commit the transaction

            flash('Withdrawal successful!', 'success')  # Flash success message
            """ Redirect to prevent form resubmission """
            return render_template('withdraw_money.html', account=account)
            # return redirect(url_for('account', account_id=account_id))
        else:
            flash('Insufficient funds!', 'error')  # Show error for insufficient funds

    return render_template('withdraw_money.html', account=account)

@app.route('/deposit_money/<int:account_id>', methods=['GET', 'POST'])
def deposit_money(account_id):
    """Deposit money to an account."""
    """ Retrieve account details """
    # Retrieve account details from the database
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        # Get deposit amount from the form
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')  # Show error for invalid amount
            return render_template('deposit_money.html', account=account)

        amount = float(amount)
        """ Retrieve account balance """
        # Retrieve current balance from the database
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        current_balance = db_cursor.fetchone()[0]

        new_balance = current_balance + amount  # Calculate new balance after deposit
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))  # Update balance in database
        db_connection.commit()  # Commit the transaction

        flash('Deposit successful!', 'success')  # Flash success message
        """ Redirect to prevent form resubmission """
        return render_template('deposit_money.html', account=account)
        # return redirect(url_for('account', account_id=account_id))

    return render_template('deposit_money.html', account=account)

@app.route('/send_money/<int:sender_id>', methods=['GET', 'POST'])
def send_money(sender_id):
    """Send money from one account to another."""
    """ Retrieve sender's account details """
    # Retrieve sender's account details from the database
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (sender_id,))
    sender_account = db_cursor.fetchone()

    if request.method == 'POST':
        # Get recipient ID and amount from the form
        recipient_id = request.form['recipient_id']
        amount = request.form['amount']

        if not recipient_id.isdigit() or not is_valid_amount(amount):
            flash('Invalid input. Please enter a valid recipient ID and a positive amount.', 'error')  # Show error for invalid input
            return render_template('send_money.html', account=sender_account)

        recipient_id = int(recipient_id)
        amount = float(amount)

        """ Retrieve sender's balance """
        # Retrieve sender's balance from the database
        db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (sender_id,))
        sender_balance = db_cursor.fetchone()[0]

        if sender_balance >= amount:
            """ Update sender's balance """
            # Calculate new sender balance after sending money
            new_sender_balance = sender_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_sender_balance, sender_id))

            """ Retrieve recipient's balance """
            # Retrieve recipient's balance and name from the database
            db_cursor.execute("SELECT balance FROM accounts WHERE id = %s", (recipient_id,))
            recipient_balance_row = db_cursor.fetchone()
            db_cursor.execute("SELECT name FROM accounts WHERE id = %s", (recipient_id,))
            recipient_name_row = db_cursor.fetchone()

            if recipient_balance_row is not None:
                recipient_balance = recipient_balance_row[0]
                recipient_name = recipient_name_row[0]
                
                """ Update recipient's balance """
                # Calculate new recipient balance after receiving money
                new_recipient_balance = recipient_balance + amount
                db_cursor.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_recipient_balance, recipient_id))

                db_connection.commit()  # Commit the transaction
                flash(f'Money sent successfully to {recipient_name}', 'success')  # Flash success message with recipient's name
                return render_template('send_money.html', account=sender_account)
                # return redirect(url_for('account', account_id=sender_id))
            else:
                flash('Recipient account not found!', 'error')  # Show error if recipient account not found
        else:
            flash('Insufficient funds!', 'error')  # Show error for insufficient funds

    return render_template('send_money.html', account=sender_account)

@app.route('/account/<int:account_id>')
def account(account_id):
    """Display account details."""
    """ Retrieve account details """
    # Retrieve account details from the database
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if account:
        return render_template('account.html', account=account, account_id=account_id)  # Render account page with account details
    else:
        return render_template('404.html'), 404  # Show 404 page if account not found

@app.route('/service/', methods=['GET', 'POST'])
def service():
    """Render service page."""
    return render_template('service.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
    """Render About page."""
    return render_template('about.html')

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
