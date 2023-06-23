

# Socialize

![Socialize - Device Mockup](https://github.com/Sirak-K/my-project-4/assets/122515678/8e378d27-aef5-46e3-b702-46a9919060c2)

<p align="center">
  <a href="https://sirak-k.github.io/my-project-4" target="_blank">View the deployed version on GitHub Pages.</a>
</p>

# Table of Contents

- [Socialize](#socialize)
- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
  - [Target Audience](#target-audience)
- [Project Features](#project-features)
  - [Main Features](#main-features)
    - [In-Scope Implementations](#in-scope-implementations)
    - [Out of Scope Implementations](#out-of-scope-implementations)
  - [User Stories](#user-stories)
  - [Technologies Used](#technologies-used)
- [Installation and Usage](#installation-and-usage)
  - [Prerequisites](#prerequisites)
  - [Project Installation](#project-installation)
  - [Project Configuration](#project-configuration)
  - [Application Usage](#application-usage)
      - [Signing Up - Validation Rules](#signing-up---validation-rules)
        - [Username:](#username)
        - [Password verification:](#password-verification)
        - [Password verification confirmation:](#password-verification-confirmation)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
- [Database](#database)
  - [Database Setup](#database-setup)
      - [Database Setup Prerequisites](#database-setup-prerequisites)
  - [Database Configuration](#database-configuration)
  - [Database Design](#database-design)
    - [Database Diagrams](#database-diagrams)
# Project Description

Socialize is a dynamic and user-friendly social networking platform that allows users to connect, share, and engage with friends. Built using Django, Python's web framework, Socialize offers a seamless and intuitive user experience with a range of features to enhance social interactions.

## Target Audience
Socialize is designed for individuals who value meaningful social connections and want to engage with friends in a secure and intuitive online environment. It caters to users who seek a user-friendly social networking platform with enhanced customization options and features that encourage active participation and interaction.

# Project Features

## Main Features
### In-Scope Implementations
- **Account Registration :** New users can easily sign up for an account to become members of the social network.

- **Account Authentication:** Existing users can securely log in to access the platform's features, ensuring their personal information remains protected.

- **Account Password Retrieval:** Users have the ability to reset their passwords in case they forget them. This feature allows users to regain access to their accounts by initiating a password reset process. Users will be prompted to enter their username and provide a new password. The system will verify the information and update the password accordingly. This ensures that users can regain access to their accounts even if they forget their passwords. Go to [Validation Rules](#signing-up-validation-rules) in the Application Usage section of this document for detailed instructions on how to reset a password successfully.

- **User Profile Customization:** Socialize allows users to personalize their profiles by uploading their own profile images and profile banners, expressing their unique aesthetic style and preferences.
![MF - 1 - Profile Editing](https://github.com/Sirak-K/my-project-4/assets/122515678/8dccf655-be3b-4b1e-8930-3be7648613f4)

- **Post Creation and Editing:** Users can create posts and share their thoughts, experiences, and updates with their friends. The platform supports post editing, enabling users to modify the content of their posts as needed.
![MF - 2 - Post Creation](https://github.com/Sirak-K/my-project-4/assets/122515678/381c0aaf-e8e0-4f2c-b2df-fdcd1d5691ee)
![MF - 3 - Post Editing And Deletion](https://github.com/Sirak-K/my-project-4/assets/122515678/ea3a42d7-2eab-49b0-a335-be28c14088c2)

- **Post Interaction:** Users can engage with posts through features such as liking and unliking posts, fostering a sense of appreciation and support within the community. Additionally, users can participate in post discussions by creating comments and sharing their opinions.

- **Personalized Feed:** Socialize offers a personalized feed that showcases posts created by friends. Users can stay up to date with the activities and updates of their social circle, ensuring they never miss important moments.
![MF - 4 - Personalized Feed and Engagement](https://github.com/Sirak-K/my-project-4/assets/122515678/2c34255c-d179-460f-a9f7-e1582af3e278)

- **User Search and Connections:** Socialize provides a user-friendly search functionality, allowing users to find and connect with other users based on their username or name. Users can send friend requests to expand their social network and control who is a part of their community.
![MF - 5 - User Search](https://github.com/Sirak-K/my-project-4/assets/122515678/26cb18fb-a48c-4d46-b6c3-9e21bc5ee917)


- **Social Networking:** Users can send, cancel, accept and reject friend requests to expand their social network or control who is included in their social network.
![MF - 6 - Social Networking   Friends](https://github.com/Sirak-K/my-project-4/assets/122515678/299573b4-55f6-4fe4-8b7b-fade2a71999e)


### Out of Scope Implementations
- Options to embed image & video onto posts.
- Additional profile details such as residence/location & 'last seen'.
- Border color around profile image to indicate if a user is logged in or logged out.

## User Stories

![User Stories - Socialize](https://github.com/Sirak-K/my-project-4/assets/122515678/b8f8db13-0fac-4d74-9e46-f57e1255aff0)

[View the User Stories on GitHub.](https://github.com/users/Sirak-K/projects/3)


## Technologies Used

- Python
- Django
- HTML
- CSS
- JavaScript
- VS Code as a local IDE.
- GitHub as a remote repository
- GitHub Pages to deploy the website.

# Installation and Usage

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
##### Password verification:
-   Minimum length of 8 characters.
-   Should not be too similar to other personal information.
-   Should not be a commonly used password.
-   Should not be entirely numeric.
##### Password verification confirmation:
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


# Database
## Database Setup
In the Django Social Networking App, we use a relational database management system to store and manage our application data. This section will guide you through the steps of setting up the database for your project.

#### Database Setup Prerequisites
Before proceeding with the database setup, make sure you have the following prerequisites in place:

- Database server installed on your system
- Database client libraries installed
- Django framework installed

## Database Configuration
To configure your Django application to use the database, follow these steps:

1. Open the project in your chosen editor.

2. Locate the settings.py file in the project's directory.
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

3. Replace the placeholders with the appropriate values for your database setup.

4. Install and configure the appropriate database server based on your chosen database engine.


## Database Design
### Database Diagrams

![DB Model Design - with dbdiagram.io](https://github.com/Sirak-K/my-project-4/assets/122515678/a65445ac-317a-4590-a802-26f0ea318647)
![DB Model Design - PlantUML](https://github.com/Sirak-K/my-project-4/assets/122515678/eae021c7-5eaa-4506-8b32-dc9fe8da8332)
