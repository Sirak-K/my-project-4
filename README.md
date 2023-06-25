
<p align="center">
  <img src="https://img.shields.io/badge/Python-3-blue?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-3-green?style=for-the-badge&logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/HTML-5-orange?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/CSS-3-blue?style=for-the-badge&logo=css3&logoColor=white">
</p>


# Socialize

![Socialize - Device Mockup](https://github.com/Sirak-K/my-project-4/assets/122515678/8e378d27-aef5-46e3-b702-46a9919060c2)

<p align="center">
  <a href="https://my-project-4-socialize-a58a0308fc72.herokuapp.com" target="_blank">View the deployed version of Socialize.</a>
</p>

# Table of Contents

- [Socialize](#socialize)
- [Table of Contents](#table-of-contents)
- [Project Description](#project-description)
  - [Target Audience](#target-audience)
- [Project Features](#project-features)
  - [Main Features](#main-features)
    - [In-Scope Features](#in-scope-features)
    - [Out-of-Scope Features](#out-of-scope-features)
  - [User Stories](#user-stories)
  - [Technologies Used](#technologies-used)
- [Usage](#usage)
    - [Signing Up - Validation Rules](#signing-up---validation-rules)
      - [Username:](#username)
      - [Password verification:](#password-verification)
      - [Password verification confirmation:](#password-verification-confirmation)
- [File Storage](#file-storage)
  - [Database](#database)
    - [Cloudinary](#cloudinary)
    - [Cloudinary - Configuration](#cloudinary---configuration)
    - [Serving Files with Cloudinary](#serving-files-with-cloudinary)
  - [File Storage - Conclusion](#file-storage---conclusion)
- [Testing \& Validation](#testing--validation)
- [Deployment](#deployment)
- [Installation](#installation)
  - [Cloning](#cloning)
  - [Forking](#forking)
- [Credits \& Sources](#credits--sources)
    - [Images](#images)
      - [Hero/Landing Image (Login-page)](#herolanding-image-login-page)
      - [Default Banner Image](#default-banner-image)
      - [Default Profile Image](#default-profile-image)
      - [A.I-generated Profile Images](#ai-generated-profile-images)
      - [Background Image for Device Mockup](#background-image-for-device-mockup)
    - [Fonts \& Icons](#fonts--icons)
  
# Project Description

Socialize is a dynamic and user-friendly social networking platform that allows users to connect, share, and engage with friends. Built using Django, a Python web framework, Socialize offers a seamless and intuitive user experience with a range of features to enhance social interactions.

## Target Audience
Socialize is designed for individuals who value meaningful social connections and want to engage with friends in a secure and intuitive online environment. It caters to users who seek a user-friendly social networking platform with enhanced customization options and features that encourage active participation and interaction.

# Project Features
## Main Features
### In-Scope Features
#### **Account Registration**
New users can easily sign up for an account to become members of the social network.

#### **Account Authentication**
Existing users can securely log in to access the platform's features, ensuring their personal information remains protected.

#### **Account Password Retrieval**
Users have the ability to reset their passwords in case they forget them. This feature allows users to regain access to their accounts by initiating a password reset process. Users will be prompted to enter their username and provide a new password. The system will verify the information and update the password accordingly. This ensures that users can regain access to their accounts even if they forget their passwords. Go to [Validation Rules](#signing-up-validation-rules) in the Application Usage section of this document for detailed instructions on how to reset a password successfully.

#### **User Profile Customization**
Socialize allows users to personalize their profiles by uploading their own profile images and updating their profile details.
![Profile Editing](https://github.com/Sirak-K/my-project-4/assets/122515678/8dccf655-be3b-4b1e-8930-3be7648613f4)

#### **Post Creation and Editing**
Users can create posts and share their thoughts, experiences, and updates with their friends. The platform supports post editing, enabling users to modify the content of their posts as needed.
![Post Creation](https://github.com/Sirak-K/my-project-4/assets/122515678/381c0aaf-e8e0-4f2c-b2df-fdcd1d5691ee)
![Post Editing And Deletion](https://github.com/Sirak-K/my-project-4/assets/122515678/ea3a42d7-2eab-49b0-a335-be28c14088c2)

#### **Post Interaction**
Users can engage with posts through features such as liking and unliking posts, fostering a sense of appreciation and support within the community. Additionally, users can participate in post discussions by creating comments and sharing their opinions.

#### **User Feed**
Socialize offers a personalized feed that showcases posts created by friends. Users can stay up to date with the activities and updates of their social circle, ensuring they never miss important moments.
![Personalized Feed](https://github.com/Sirak-K/my-project-4/assets/122515678/2c34255c-d179-460f-a9f7-e1582af3e278)

#### **User Search**
Socialize provides a user-friendly search functionality, allowing users to find and connect with other users based on their username or name. Users can send friend requests to expand their social network and control who is a part of their community.
![User Search](https://github.com/Sirak-K/my-project-4/assets/122515678/26cb18fb-a48c-4d46-b6c3-9e21bc5ee917)


#### **Social Networking**
Users can send, cancel, accept and reject friend requests to expand their social network or control who is included in their social network.
![Friends](https://github.com/Sirak-K/my-project-4/assets/122515678/299573b4-55f6-4fe4-8b7b-fade2a71999e)


### Out-of-Scope Features
- Options to embed image & video onto posts.
- Additional profile details such as residence/location & 'last seen'.
- Border color around profile image to indicate if a user is logged in or logged out.
- Delete-button for comments made on posts. 

## User Stories

![Project User Stories](https://github.com/Sirak-K/my-project-4/assets/122515678/b8f8db13-0fac-4d74-9e46-f57e1255aff0)

[View the User Stories on GitHub.](https://github.com/users/Sirak-K/projects/3)


## Technologies Used
- Python
- Django
- HTML
- CSS
- JavaScript
- GitPod as online IDE and workspace
- GitHub as a remote repository

# Usage
1. Open and use your web browser or navigate to the Socialize app by clicking [here](https://my-project-4-socialize-a58a0308fc72.herokuapp.com).
2.  Create a new account by clicking on the "Sign Up" button and following the registration process. 
### Signing Up - Validation Rules
Based on the built-in Django `UserCreationForm`.
#### Username:
-   Required field.
-   Maximum length of 150 characters.
-   Allowed characters: letters, digits, and symbols '@/./+/-/_'.
#### Password verification:
-   Minimum length of 8 characters.
-   Should not be too similar to other personal information.
-   Should not be a commonly used password.
-   Should not be entirely numeric.
#### Password verification confirmation:
-   Should match the entered password for verification. 
4.  Log in to your account using your credentials.  
5.  Explore the various features of the application, such as creating posts, editing your profile, searching for other users, and interacting with friends' posts.  
6.  When you're finished using the application, log out to secure your personal information.


# File Storage

Socialize utilizes a robust file storage solution to manage the storage and retrieval of various files within the project. This section provides an overview of how files are stored and accessed in the application.

## Database
In addition to file storage, the project utilizes PostgreSQL as the relational database management system. The online database service ElephantSQL.com is used to host the PostgreSQL database. This ensures that the application's data is securely stored and can be accessed by the application as needed.

![Model Diagram with dbdiagram.io](https://github.com/Sirak-K/my-project-4/assets/122515678/a65445ac-317a-4590-a802-26f0ea318647)
![Model Diagram with PlantUML](https://github.com/Sirak-K/my-project-4/assets/122515678/eae021c7-5eaa-4506-8b32-dc9fe8da8332)

The project's configuration specifies the necessary connection details to establish a connection with the PostgreSQL database hosted on ElephantSQL.com. This allows the application to interact with the database and perform various data-related operations.

### Cloudinary

Cloudinary, a cloud-based media management platform, is seamlessly integrated into the project to handle the storage and delivery of files. Cloudinary offers a reliable and scalable solution for storing and serving media files, ensuring optimal performance for the application.

With Cloudinary integration, the project leverages its powerful features to upload, manage, and deliver various types of files. This includes user profile pictures, media attachments, and other files utilized within the application.

### Cloudinary - Configuration

The project is configured to use Cloudinary as the primary storage solution for files. When a user uploads a file, it is securely transferred to Cloudinary's servers and stored in their cloud storage. This allows for a centralized and efficient file storage system, eliminating the need for local storage management.

The Django project is set up to utilize Cloudinary as the storage backend for media files and static files. This ensures that all uploaded files are seamlessly handled and stored within the Cloudinary ecosystem.

### Serving Files with Cloudinary

Cloudinary provides a convenient and efficient way to serve files within the Django Social Networking project. When a user requests a file, such as a user profile picture or a media attachment, Cloudinary seamlessly delivers the file directly to the user's browser. This ensures fast and reliable access to the requested files, enhancing the overall user experience.

By leveraging Cloudinary's file delivery capabilities, files within the application are easily accessible and promptly delivered to users as required.

## File Storage - Conclusion

Through the integration of PostgreSQL for database storage and the utilization of Cloudinary for file storage, the Django Social Networking project achieves a robust and efficient solution for managing files and application data. PostgreSQL hosted on ElephantSQL.com ensures secure and reliable data storage, while Cloudinary's seamless integration provides efficient file handling and delivery.

By leveraging PostgreSQL and Cloudinary, the project ensures that files and data are securely stored, easily accessible, and delivered to users in a fast and efficient manner. This enhances the overall user experience and contributes to the success of the Django Social Networking project.

Feel free to explore Cloudinary's extensive documentation to learn more about its advanced features and customization options. Additionally, you can refer to ElephantSQL's documentation for further information on managing PostgreSQL databases in an online environment.

# Testing & Validation

![Testing & Validation - Performance & Responsiveness](https://github.com/Sirak-K/my-project-4/assets/122515678/95cfc5e4-2af2-46b6-b8df-522b4fd833cf)

![validation_html](https://github.com/Sirak-K/my-project-4/assets/122515678/d4d9d53e-7295-4477-8cf1-3866afc95ce3)

<p align="">
  <img src="https://img.shields.io/badge/HTML-5-orange?style=for-the-badge&logo=html5&logoColor=white"> ✓
</p>
<a href="http://jigsaw.w3.org/css-validator/check/referer">
    <img style="border:0;width:88px;height:31px"
        src="http://jigsaw.w3.org/css-validator/images/vcss-blue"
        alt="Valid CSS!" />
    </a>
<p align="left">
  </p>
PEP-8: ✓

flake8: ✓

# Deployment
The project has been deployed to Heroku. 

You can access the deployed version of Socialize [here](https://my-project-4-socialize-a58a0308fc72.herokuapp.com/).

# Installation
 To get started with this project, you can follow the instructions below to clone or fork the repository. 

## Cloning 
To clone the repository to your local machine, use the following command:

    git clone https://github.com/Sirak-K/my-project-4.git

If you prefer using SSH, you can run the following command: `git clone: Sirak-K/my-project-4.git`

## Forking

If you'd like to contribute to this project or create your own version, you can fork the repository. Click the "Fork" button on the top right corner of the repository page, which will create a copy of the repository under your GitHub account.

You can then clone the forked repository using the following command:

    git clone https://github.com/Sirak-K/my-project-4.git

For more information on using Git and GitHub, please see the  [official Git documentation](https://git-scm.com/docs)  and  [GitHub Help](https://docs.github.com/en/github).


# Credits & Sources

### Images
#### Hero/Landing Image (Login-page) 
- Kostas Papaioannou, [Unsplash](https://unsplash.com/@papaioannou_kostas)

#### Default Banner Image 
- Kaikoro Kgd, [Vecteezy](https://sv.vecteezy.com/vektor-konst/518356-abstrakt-bakgrund-morka-och-svarta-overlappningar-001)
#### Default Profile Image 
- David Smith, [AMJ](https://www.asiamediajournal.com/default-pfp/)

#### A.I-generated Profile Images
- [Midjourney](https://docs.midjourney.com/)

#### Background Image for Device Mockup 
- [WallpaperFlare](https://www.wallpaperflare.com/friends-sunrise-young-happy-friendship-sunset-together-wallpaper-aoyvj/download)

### Fonts & Icons
- [FontAwesome](https://fontawesome.com/docs/web/setup/get-started)
