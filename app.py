#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'oluwasegun137'
DB_NAME = 'mybank'

db_connection = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

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
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        db_cursor.execute("INSERT INTO accounts (name, username, password, balance) VALUES (%s, %s, %s, %s)",
                       (name, username, password, 0))
        db_connection.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('create_account'))

    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db_cursor.execute("SELECT * FROM accounts WHERE username = %s AND password = %s", (username, password))
        account = db_cursor.fetchone()

        if account:
            return render_template('account.html', account=account)
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html')

def log_transaction(account_id, transaction_type, amount):
    db_cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", 
                      (account_id, transaction_type, amount))
    db_connection.commit()

@app.route('/withdraw_money/<int:account_id>', methods=['GET', 'POST'])
def withdraw_money(account_id):
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
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    if account:
        return render_template('account.html', account=account, account_id=account_id)
    else:
        return render_template('404.html'), 404

@app.route('/transaction_history/<int:account_id>')
def transaction_history(account_id):
    # Fetch account details
    db_cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
    account = db_cursor.fetchone()

    # Fetch transaction history
    db_cursor.execute("SELECT * FROM transactions WHERE account_id = %s ORDER BY timestamp DESC", (account_id,))
    transactions = db_cursor.fetchall()

    return render_template('transaction_history.html', transactions=transactions, account=account)


@app.route('/service/', methods=['GET', 'POST'])
def service():
    return render_template('service.html')

@app.route('/about/', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
