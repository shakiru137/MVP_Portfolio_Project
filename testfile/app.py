from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secret key for session management

# Mock user data
users = {'admin': 'password123'}

@app.route('/')
def home():
    """Render the home page."""
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password match
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            return redirect(url_for('account'))
        else:
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/account')
def account():
    """Render the account page if user is logged in."""
    if 'username' in session:
        username = session['username']
        return render_template('account.html', username=username)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
