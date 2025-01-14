# Login-Signup App

This is a simple **Login and Signup** web application built using **Python**, **Flask**, and **SQLite** for the backend. The app allows users to register, log in, and manage their sessions. The passwords are securely hashed using the PBKDF2 encryption algorithm.

## Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Installation Instructions](#installation-instructions)
4. [How to Use](#how-to-use)
5. [Project Structure](#project-structure)
6. [Contributing](#contributing)
7. [License](#license)
8. [Acknowledgements](#acknowledgements)

## Features

- **User Authentication**: Users can sign up with their username and password.
- **Login & Logout**: Once registered, users can log in and log out.
- **Password Hashing**: Passwords are stored securely using the **PBKDF2** encryption algorithm.
- **Session Management**: The app keeps track of the user's login state using Flask sessions.
- **Responsive UI**: Built using **Bootstrap** for a responsive user interface.

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite (File-based database)
- **Password Encryption**: PBKDF2 (Password-Based Key Derivation Function 2)
- **Session Management**: Flask Sessions
- **Version Control**: Git

## Installation Instructions

### Prerequisites

Before getting started, ensure you have the following software installed:

- **Python 3.x**: [Install Python](https://www.python.org/downloads/)
- **pip**: Python’s package manager (comes with Python 3.x)
- **Virtual Environment (optional but recommended)**: Isolates project dependencies.

### Step-by-Step Installation

1. **Clone the repository**:

    Open your terminal or command prompt and clone the repository:

    ```bash
    git clone https://github.com/imrj18/login_signup-app.git
    cd login_signup-app
    ```

2. **Create a Virtual Environment** (optional but recommended):

    For **Windows**:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

    For **macOS/Linux**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install Dependencies**:

    Install the required dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the Database**:

    The app uses an SQLite database. The database will be created automatically when you run the app for the first time. 

    If you wish to manually create it or need more details, the database file is stored in `app.db`.

5. **Run the Application**:

    After installation, run the app using the following command:

    ```bash
    python app.py
    ```

    The app will be accessible at `http://127.0.0.1:5000/` in your browser.

## How to Use

1. **Signup**:
    - Go to the **Signup** page (`/signup`).
    - Enter a username and password to register a new account.
   
2. **Login**:
    - Go to the **Login** page (`/login`).
    - Enter your username and password to log in.
   
3. **Logout**:
    - After logging in, you can log out at any time by clicking the **Logout** button.

## Project Structure

The project is structured as follows:

```plaintext
login_signup-app/
│
├── app.py                # Main application file with routes and logic
├── templates/            # HTML files for rendering pages
│   ├── home.html         # Home page after login
│   ├── login.html        # Login page
│   └── signup.html       # Signup page
├── static/               # Static files like CSS and JS
│   └── style.css         # Custom CSS styles
├── requirements.txt      # List of required packages (Flask, Flask-Session, etc.)
└── .gitignore            # Git ignore file to exclude unnecessary files
```

### Key Files and Their Functions

- **app.py**: Contains the main Flask routes and logic for the app. It handles the user authentication, session management, and routing.
- **templates/ folder**: Contains the HTML files that define the structure of each page (home, login, signup).
- **static/ folder**: Contains static assets such as CSS, JavaScript, and images. 

## Contributing

1. Fork this repository.
2. Clone your fork: `git clone https://github.com/your-username/login_signup-app.git`
3. Create a new branch: `git checkout -b feature-name`
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to your branch: `git push origin feature-name`
6. Submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- **Flask Documentation**: [Flask Docs](https://flask.palletsprojects.com/)
- **Bootstrap**: [Bootstrap Docs](https://getbootstrap.com/)

