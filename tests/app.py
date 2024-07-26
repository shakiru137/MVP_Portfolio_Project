"""
This module sets up a Flask application for a banking system with basic functionalities
such as account creation, login, deposit, withdrawal, money transfer, and transaction history.
It uses MySQL as the database and bcrypt for password hashing and random for generating new
account number and transaction number.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import mysql.connector
import random

# Initialize Flask application
app = Flask(__name__, static_folder='static')
app.secret_key = 'i_do_not_have_it_yet'

# Database configuration
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'oluwasegun137'
DB_NAME = 'PURE_BANK'

# Initialize the bcrypt object for password hashing
bcrypt = Bcrypt(app)

def get_db_connection():
    """Create and return a new database connection."""
    db_connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return db_connection

def is_username_taken(username):
    """Check if the username is already taken.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if username is taken, False otherwise.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
    user = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()
    return user is not None

def is_valid_amount(amount):
    """Validate if the amount is a positive number.

    Args:
        amount (str): The amount to validate.

    Returns:
        bool: True if amount is a positive number, False otherwise.
    """
    try:
        amount = float(amount)
        return amount > 0
    except ValueError:
        return False

def generate_account_number(db_cursor):
    """Generate a unique 10-digit account number starting with '00' or '01'.

    Args:
        db_cursor (mysql.connector.cursor): The database cursor for checking uniqueness.

    Returns:
        str: A unique 10-digit account number.
    """
    while True:
        # Choose a prefix of "00" or "01"
        prefix = random.choice(["00", "01"])
        # Generate the remaining 8 digits
        remaining_digits = ''.join(random.choices('0123456789', k=8))
        # Combine prefix and remaining digits
        account_number = prefix + remaining_digits
        
        # Check if the account number already exists in the database
        db_cursor.execute("SELECT COUNT(*) FROM accounts WHERE account_number = %s", (account_number,))
        if db_cursor.fetchone()[0] == 0:
            # Account number is unique
            return account_number

def generate_transaction_number(db_cursor):
    """Generate a unique 18-digit transaction number."""
    while True:
        # Generate an 18-digit number as a string
        transaction_number = ''.join(random.choices('0123456789', k=18))
        
        # Check if the transaction number already exists in the database
        db_cursor.execute("SELECT COUNT(*) FROM transactions WHERE transaction_number = %s", (transaction_number,))
        if db_cursor.fetchone()[0] == 0:
            # Transaction number is unique
            return transaction_number

@app.route('/')
def index():
    """Render the index page."""
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    """Handle account creation.

    GET: Render the account creation form.
    POST: Create a new account if form data is valid.
    """
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        if is_username_taken(username):
            flash('Username already taken. Please choose another username.', 'error')
            return render_template('create_account.html')

        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()
        account_number = generate_account_number(db_cursor)
        db_cursor.execute("INSERT INTO accounts (name, username, password, balance, account_number) VALUES (%s, %s, %s, %s, %s)",
                          (name, username, hash_password, 0, account_number))
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

        flash('Account created successfully!', 'success')
        return redirect(url_for('create_account'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login.

    GET: Render the login form.
    POST: Verify user credentials and log in if valid.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_connection = get_db_connection()
        db_cursor = db_connection.cursor()
        db_cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = db_cursor.fetchone()
        db_cursor.close()
        db_connection.close()

        if account:
            stored_password = account[3]  # Assuming password is the 4th column
            try:
                if bcrypt.check_password_hash(stored_password, password):
                    return render_template('account.html', account=account)
                else:
                    error = 'Invalid credentials'
            except ValueError:
                error = 'Invalid password hash'
        else:
            error = 'Invalid credentials'

        return render_template('login.html', error=error)

    return render_template('login.html')

def log_transaction(account_number, transaction_type, amount):
    """Log a transaction in the database.

    Args:
        account_number (str): The account number involved in the transaction.
        transaction_type (str): The type of transaction (e.g., 'withdrawal', 'deposit').
        amount (float): The amount of the transaction.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    
    # Generate a unique 18-digit transaction number
    transaction_number = generate_transaction_number(db_cursor)
    
    # Insert the transaction record into the database
    db_cursor.execute("INSERT INTO transactions (transaction_number, account_number, type, amount) VALUES (%s, %s, %s, %s)", 
                      (transaction_number, account_number, transaction_type, amount))
    
    db_connection.commit()
    db_cursor.close()
    db_connection.close()

@app.route('/withdraw_money/<string:account_number>', methods=['GET', 'POST'])
def withdraw_money(account_number):
    """Handle money withdrawal from an account.

    GET: Render the withdrawal form.
    POST: Process the withdrawal if the form data is valid.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('withdraw_money.html', account=account)

        amount = float(amount)
        db_cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        current_balance = db_cursor.fetchone()[0]

        if current_balance >= amount:
            new_balance = current_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
            db_connection.commit()
            log_transaction(account_number, 'withdrawal', amount)

            flash('Withdrawal successful!', 'success')
            return render_template('withdraw_money.html', account=account)
        else:
            flash('Insufficient funds!', 'error')

    db_cursor.close()
    db_connection.close()
    return render_template('withdraw_money.html', account=account)

@app.route('/deposit_money/<string:account_number>', methods=['GET', 'POST'])
def deposit_money(account_number):
    """Handle money deposit into an account.

    GET: Render the deposit form.
    POST: Process the deposit if the form data is valid.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
    account = db_cursor.fetchone()

    if request.method == 'POST':
        amount = request.form['amount']

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('deposit_money.html', account=account)

        amount = float(amount)
        db_cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_number,))
        current_balance = db_cursor.fetchone()[0]

        new_balance = current_balance + amount
        db_cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_number))
        db_connection.commit()
        log_transaction(account_number, 'deposit', amount)

        flash('Deposit successful!', 'success')
        return render_template('deposit_money.html', account=account)

    db_cursor.close()
    db_connection.close()
    return render_template('deposit_money.html', account=account)

@app.route('/send_money/<string:sender_number>', methods=['GET', 'POST'])
def send_money(sender_number):
    """Handle sending money from one account to another.

    GET: Render the send money form.
    POST: Process the money transfer if the form data is valid.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (sender_number,))
    sender_account = db_cursor.fetchone()

    if request.method == 'POST':
        recipient_number = request.form['recipient_number']
        amount = request.form['amount']

        if recipient_number == sender_number:
            flash("Can't send money to yourself!", 'error')
            return render_template('send_money.html', account=sender_account)

        if not is_valid_amount(amount):
            flash('Invalid amount. Please enter a positive number.', 'error')
            return render_template('send_money.html', account=sender_account)

        amount = float(amount)

        db_cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (sender_number,))
        sender_balance = db_cursor.fetchone()[0]

        if sender_balance >= amount:
            new_sender_balance = sender_balance - amount
            db_cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_sender_balance, sender_number))

            db_cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (recipient_number,))
            recipient_balance_row = db_cursor.fetchone()

            if recipient_balance_row is not None:
                recipient_balance = recipient_balance_row[0]
                new_recipient_balance = recipient_balance + amount
                db_cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_recipient_balance, recipient_number))

                db_connection.commit()
                log_transaction(sender_number, 'transfer', amount)
                log_transaction(recipient_number, 'receive', amount)

                flash('Money sent successfully!', 'success')
                return render_template('send_money.html', account=sender_account)
            else:
                flash('Recipient account not found!', 'error')
        else:
            flash('Insufficient funds!', 'error')

    db_cursor.close()
    db_connection.close()
    return render_template('send_money.html', account=sender_account)


@app.route('/account/<string:account_number>')
def account(account_number):
    """Display account details.

    Args:
        account_number (str): The number of the account to display.

    Returns:
        Rendered template with account details or 404 page if account not found.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
    account = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()

    if account:
        return render_template('account.html', account=account)
    else:
        return render_template('404.html'), 404

@app.route('/transaction_history/<string:account_number>')
def transaction_history(account_number):
    """Display transaction history for an account.

    Args:
        account_number (str): The number of the account to display transaction history for.

    Returns:
        Rendered template with transaction history.
    """
    db_connection = get_db_connection()
    db_cursor = db_connection.cursor()

    # Fetch account details
    db_cursor.execute("SELECT * FROM accounts WHERE account_number = %s", (account_number,))
    account = db_cursor.fetchone()

    # Fetch transaction history
    db_cursor.execute("SELECT * FROM transactions WHERE account_number = %s ORDER BY timestamp DESC", (account_number,))
    transactions = db_cursor.fetchall()

    db_cursor.close()
    db_connection.close()
    return render_template('transaction_history.html', transactions=transactions, account=account)

@app.route('/service/', methods=['GET', 'POST'])
def service():
    """Render the service page."""
    return render_template('service.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
    """Render the about page."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
