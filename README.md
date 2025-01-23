# Login-Signup and Blog System App

This is a web application that integrates a **Login and Signup** system with a **Blog Management System** built using **Python**, **Flask**, and **MySQL** for the backend. Users can register, log in, and manage their sessions. Doctors can create and manage blog posts, while patients can view categorized blogs. Passwords are securely hashed using the PBKDF2 encryption algorithm.

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

### User Authentication
- **Signup**: Users can register with their details.
- **Login & Logout**: Registered users can log in and manage sessions.
- **Password Hashing**: Secure storage using the **PBKDF2** encryption algorithm.
- **Session Management**: Tracks user login state using Flask sessions.

### Blog Management System
- **Doctors**:
  - Upload blog posts with the following fields: Title, Image, Category, Summary, and Content.
  - Mark blog posts as drafts during upload.
  - View a list of all posts uploaded by them.
- **Patients**:
  - View a list of published blog posts (not marked as drafts).
  - Posts are categorized with titles, images, and truncated summaries (if longer than 15 words).

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Password Encryption**: PBKDF2 (Password-Based Key Derivation Function 2)
- **Session Management**: Flask Sessions
- **Version Control**: Git

## Installation Instructions

### Prerequisites

Before getting started, ensure you have the following software installed:

- **Python 3.x**: [Install Python](https://www.python.org/downloads/)
- **pip**: Python’s package manager (comes with Python 3.x)
- **MySQL**: [Install MySQL](https://dev.mysql.com/downloads/installer/)
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

4. **Configure the Database**:

    Update your `.env` file with your MySQL credentials (ensure the `.env` file is not pushed to version control):

    ```env
    DB_URI=mysql://<username>:<password>@localhost/<database_name>
    ```

    Example:
    ```env
    DB_URI=mysql://root:password@localhost/login_signup
    ```

5. **Run Database Migrations**:

    Set up the database schema using Flask-Migrate:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. **Run the Application**:

    After installation, run the app using the following command:

    ```bash
    python app.py
    ```

    The app will be accessible at `http://127.0.0.1:5000/` in your browser.

## How to Use

### User Features
1. **Signup**:
    - Go to the **Signup** page (`/signup`).
    - Enter a username, email, password, and other details to register a new account.

2. **Login**:
    - Go to the **Login** page (`/login`).
    - Enter your username and password to log in.

3. **Logout**:
    - After logging in, you can log out at any time by clicking the **Logout** button.

### Blog Features
1. **Doctors**:
    - Navigate to the blog management section.
    - Create new blog posts with a title, image, category, summary, and content.
    - Mark posts as drafts during upload.
    - View all blogs they have uploaded.

2. **Patients**:
    - Browse the blog section to view published posts categorized with titles, images, and summaries.
    - Summaries longer than 15 words are truncated.

## Project Structure

The project is structured as follows:

```plaintext
login_signup-app/
│
├── app.py                # Main application file with routes and logic
├── templates/            # HTML files for rendering pages
│   ├── home.html         # Home page after login
│   ├── login.html        # Login page
│   ├── signup.html       # Signup page
│   ├── create_blog.html  # Blog creation page
│   ├── edit_blog.html    # Blog editing page
│   ├── view_blog.html    # Single blog view page
│   └── view_blogs.html   # All blogs view page for patients
├── static/               # Static files like CSS and JS
│   └── style.css         # Custom CSS styles
├── models.py             # Database models
├── requirements.txt      # List of required packages (Flask, Flask-Session, etc.)
├── migrations/           # Database migration scripts
└── .gitignore            # Git ignore file to exclude unnecessary files
```

### Key Files and Their Functions

- **app.py**: Contains the main Flask routes and logic for the app. It handles the user authentication, session management, and routing.
- **models.py**: Defines the database models for users and blogs.
- **templates/ folder**: Contains the HTML files that define the structure of each page (login, signup, blog management, etc.).
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


