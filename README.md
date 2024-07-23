# Pure Bank Project

Welcome to the Pure Bank Project! This repository contains the code and documentation for a comprehensive banking application developed using Flask and other web technologies.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
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

2. **Navigation:**

- Navigate to the project directory:

```bash
cd MVP_Portfolio_Project
```

3. **Virtual Environment**

- Create a virtual environment:

```bash
python3 -m venv venv
```

- Activate the virtual environment:
  - On Windows: venv\Scripts\activate
  - On macOS and Linux: source venv/bin/activate

4. **Dependencies**

- Install required dependencies:

```bash
pip install -r requirements.txt
```

5. **Database Setup**

- Create a MySQL database named mybank
- Update database configuration in (link unavailable) with your MySQL credentials
- Run database migrations:

```bash
flask db upgrade
```

6. **Running the Application**

- Run the application:

```bash
flask run
```

7. **Usage**

- Access the application in your web browser at http://localhost:5000
- Home Page: Overview and navigation options
- Account Management: Create account, log in, view account details, manage transactions
- Transaction History: View detailed transaction history for each account

8 **Testing**

- Run tests:

```bash
pytest
```

9. **Screenshots and Links**

- **Deployed Site:** [Pure Bank Live](https://youtu.be/qtPoXgTuAlo)
- **Final Project Blog Article:** [Pure Bank Project Blog](https://shakiru137.github.io/Blog-Post/)
- **Author's LinkedIn:** [Shakiru Oluwasegun Yusuf](http://linkedin.com/in/yusuf-shakiru-oluwasegun)
- **Project’s Landing Page:** [Pure Bank Landing Page](https://shakiru137.github.io/Landing_Page/)
- **GitHub Repository:** [Pure Bank Repository](https://github.com/shakiru137/MVP_Portfolio_Project)

10. **Contributing**

- Fork the repository
- Create a new branch: git checkout -b feature-branch
- Make changes and commit: git commit -m 'Add new feature'
- Push to the branch: git push origin feature-branch
- Open a Pull Request

11. **License**

- This project is licensed under the ALXSWE PROGRAM License

12. **Related Projects**

- Flask Mega-Tutorial
- Flask-SQLAlchemy
