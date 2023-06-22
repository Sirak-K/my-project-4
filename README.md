

![Last commit](https://img.shields.io/github/last-commit/sirak-k/my-project-4) 

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
  - [Key Features](#key-features)
  - [Target Audience](#target-audience)
  - [Technologies Used](#technologies-used)
- [2) Installation and Usage](#2-installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Project Installation](#project-installation)
  - [Project Configuration](#project-configuration)
  - [Application Usage](#application-usage)
      - [Signing Up - Validation Rules](#signing-up---validation-rules)
        - [Username:](#username)
        - [Password:](#password)
        - [Password confirmation:](#password-confirmation)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
- [3) Database](#3-database)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites-1)
  - [Configuration](#configuration)
  - [Design](#design)
    - [Database Diagrams](#database-diagrams)

# Project Description

Socialize is a dynamic and user-friendly social networking platform that allows users to connect, share, and engage with friends. Built using Django, Python's web framework, Socialize offers a seamless and intuitive user experience with a range of features to enhance social interactions.

## Key Features

- **User Registration and Authentication:** New users can easily sign up for an account to become members of the social network. Existing users can securely log in to access the platform's features, ensuring their personal information remains protected.

- **Profile Customization:** Socialize allows users to personalize their profiles by uploading their own profile images and profile banners, expressing their unique aesthetic style and preferences.

- **Post Creation and Editing:** Users can create and share their thoughts, experiences, and updates with their friends. The platform supports post editing, enabling users to modify the content of their posts as needed.

- **Personalized Feed:** Socialize offers a personalized feed that showcases posts created by friends. Users can stay up to date with the activities and updates of their social circle, ensuring they never miss important moments.

- **Engagement and Interaction:** Users can engage with posts through features such as liking and unliking posts, fostering a sense of appreciation and support within the community. Additionally, users can participate in post discussions by creating comments and sharing their opinions.

- **User Search and Connections:** Socialize provides a user-friendly search functionality, allowing users to find and connect with other users based on their username or name. Users can send friend requests to expand their social network and control who is a part of their community.

## Target Audience

Socialize is designed for individuals who value meaningful social connections and want to engage with friends in a secure and intuitive online environment. It caters to users who seek a user-friendly social networking platform with enhanced customization options and features that encourage active participation and interaction.

## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- VS Code as a local IDE.
- GitHub as a remote repository
- GitHub Pages to deploy the website.

# 2) Installation and Usage

## Prerequisites

Before proceeding with the installation and usage of the Django Social Networking App, make sure you have the following prerequisites in place:

-   Python installed on your system
-   Django framework installed
-   MySQL server installed and running

## Project Installation
1.  Clone the repository to your local machine:
`git clone https://github.com/your-username/django-socialize.git`
2.  Navigate to the project directory:
    `cd django-socialize`
3.  Create a virtual environment:
    `python -m venv env`
4.  Activate the virtual environment:
    -   For Windows:
        `env\Scripts\activate` 
    -   For macOS/Linux: 
        `source env/bin/activate`
        
5.  Install the project dependencies:    
    `pip install -r requirements.txt`
    
## Project Configuration
1.  Open the project in your chosen editor.
2.  Locate the `settings.py` file in the project's directory.
3.  In the `DATABASES` setting, ensure that the configuration matches the following:
    
    `DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<database_name>',
            'USER': '<database_username>',
            'PASSWORD': '<database_password>',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }` 
    
4.  Run the database migrations to set up the database schema:
`python manage.py migrate`

## Application Usage
1.  Start the development server:
    `python manage.py runserver`
2.  Open your web browser and visit `http://localhost:8000` to access the Django Social Networking App.
3.  Create a new account by clicking on the "Sign Up" button and following the registration process. Based on the built-in Django `UserCreationForm`
#### Signing Up - Validation Rules

##### Username:
-   Required field.
-   Maximum length of 150 characters.
-   Allowed characters: letters, digits, and symbols '@/./+/-/_'.
##### Password:
-   Minimum length of 8 characters.
-   Should not be too similar to other personal information.
-   Should not be a commonly used password.
-   Should not be entirely numeric.
##### Password confirmation:
-   Should match the entered password for verification. 

4.  Log in to your account using your credentials.  
5.  Explore the various features of the application, such as creating posts, editing your profile, searching for other users, and interacting with friends' posts.  
6.  When you're finished using the application, log out to secure your personal information.

## Troubleshooting

-   If you encounter any issues during installation or usage, refer to the project's documentation or seek support from the community.
    
-   Make sure the MySQL server is running and accessible with the provided configuration.
    
-   Double-check that you have installed all the necessary dependencies and packages specified in the `requirements.txt` file.
    

## Best Practices

-   It is recommended to set up a virtual environment for your project to keep the dependencies isolated.
    
-   Regularly update your project dependencies to benefit from the latest bug fixes and security patches.
    
-   Implement proper user authentication and authorization mechanisms to ensure the security of user data.
    
By following these installation and usage instructions, you can successfully set up and use the Socialize app on your local machine.


# 3) Database
Setup
In the Django Social Networking App, we use a relational database management system to store and manage our application data. This section will guide you through the steps of setting up the database for your project.

Prerequisites
Before proceeding with the database setup, make sure you have the following prerequisites in place:

Database server installed on your system
Database client libraries installed
Django framework installed
Configuration
To configure your Django application to use the database, follow these steps:

Open the project in your chosen editor.

Locate the settings.py file in the project's directory.

In the DATABASES setting, ensure that the configuration matches the following:

DATABASES = {
    'default': {
        'ENGINE': '<database_engine>',
        'NAME': '<database_name>',
        'USER': '<database_username>',
        'PASSWORD': '<database_password>',
        'HOST': '<database_host>',
        'PORT': '<database_port>',
    }
}

- <database_engine>: The database engine used by your chosen database (e.g., 'django.db.backends.mysql' for MySQL, 'django.db.backends.postgresql' for PostgreSQL, etc.).
- <database_name>: The name of your database.
- <database_username>: The username for accessing the database.
- <database_password>: The password for the database user.
- <database_host>: The hostname or IP address where the database is hosted.
- <database_port>: The port number for the database connection.

Replace the placeholders with the appropriate values for your database setup.

Install and configure the appropriate database server based on your chosen database engine.


## Design
### Database Diagrams

![DB Model Design - with dbdiagram.io](https://github.com/Sirak-K/my-project-4/assets/122515678/a65445ac-317a-4590-a802-26f0ea318647)
![DB Model Design - PlantUML](https://github.com/Sirak-K/my-project-4/assets/122515678/eae021c7-5eaa-4506-8b32-dc9fe8da8332)
