# Pure Bank Project

Welcome to the Pure Bank Project! This repository contains the code and documentation for a comprehensive banking application developed using Flask and other web technologies.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Screenshots](#screenshots)
- [Links](#links)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Pure Bank Project is a web-based banking application designed to provide users with essential banking functionalities. This includes account creation, logging in, depositing money, withdrawing money, sending money, and viewing account details. The project uses Flask as the web framework and MySQL as the database.

### Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Flask
- **Database:** MySQL

## Features

- **Account Creation:** Allows users to create a new bank account.
- **Login:** Users can log in to their account securely.
- **Deposit Money:** Users can deposit funds into their accounts.
- **Withdraw Money:** Users can withdraw funds from their accounts.
- **Send Money:** Users can transfer money between accounts.
- **Account Details:** Users can view their account details and transaction history.
- **Responsive Design:** The application is designed to be responsive and functional on various devices.
- **Error Handling**: Handles errors such as insufficient funds and invalid credentials.

## Project Structure

- **`app/`**: Contains the main application code.
- **`static/`**: Includes static files such as CSS, images, and JavaScript.
- **`templates/`**: Holds HTML files for rendering web pages.
- **`tests/`**: Contains unit tests for different application routes and functionalities.

## Installation

To set up the Pure Bank Project on your local machine, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/shakiru137/MVP_Portfolio_Project
   ```

Navigation

- Navigate to the project directory: cd MVP_Portfolio_Project

Virtual Environment

- Create a virtual environment: python3 -m venv venv
- Activate the virtual environment:
  - On Windows: venv\Scripts\activate
  - On macOS and Linux: source venv/bin/activate

Dependencies

- Install required dependencies: pip install -r requirements.txt

Database Setup

- Create a MySQL database named pure_bank
- Update database configuration in (link unavailable) with your MySQL credentials
- Run database migrations: flask db upgrade

Running the Application

- Run the application: flask run

Usage

- Access the application in your web browser at http://localhost:5000
- Home Page: Overview and navigation options
- Account Management: Create account, log in, view account details, manage transactions
- Transaction History: View detailed transaction history for each account

Testing

- Run tests: pytest

Screenshots and Links

- Deployed Site: [Pure Bank Live](replace with actual link)
- Final Project Blog Article: [Pure Bank Project Blog](replace with actual link)
- Author's LinkedIn: [Shakiru Oluwasegun Yusuf](replace with actual link)

Contributing

- Fork the repository
- Create a new branch: git checkout -b feature-branch
- Make changes and commit: git commit -m 'Add new feature'
- Push to the branch: git push origin feature-branch
- Open a Pull Request

License

- This project is licensed under the MIT License
- See the LICENSE file for details

Related Projects

- Flask Mega-Tutorial
- Flask-SQLAlchemy
