# Vista Pakistan
Vista Pakistan is a website for tourist support agencies. Vista Pakistan's website is developed as a final year project at Riphah International College, Thokar Campus Lahore, by the students of Batch-1, Associated Degree Program (ADP) Computer Sciences. Members of this project are:
- Moeez Raza
- Ubaid Ullah
- Umar Awais
- Ali Raza
## Requirements
Here is the list of programs and software required to Vista Pakistan website:
- Python3
- MySQL _or_ XAMPP
## Installation
This tutorial will only guide to run the Vista Pakistan website on localhost mode.

**[Step-1]** Download the ZIP file from GitHub by clicking `<> code` > `Download ZIP`.

**[Step-2]** Exract the .zip file by right clicking and select `Extract here`.

**[Step-3]** Open `vista_pakistan` folder and create a new file named as `gmail.py`, make sure that file extensions are not hidden.

**[Step-4]** Right click on `gmail.py` and select option `Edit with IDLE` and type the following code:
```
gmail = "yourname@gmail.com"
password = "your app password"
```
Replace `yourname@gmail.com` with your actual gmail account and replace `your app password` with your actual gmail app password.

App password is not you Gmail account's password. You can generate an app password from: https://myaccount.google.com/apppasswords

**[Step-5]** Create a new Database `vistad`. **If you're using XAMPP then:**
- start both `Apache` and `MySQL` services
- go to: http://localhost/ and select PhpMyAdmin
- Click on new at left pan
- Write `vistad` and create database.

**If you are not using XAMPP or PHPMyAdmin** then simply open MySQL command line window and run the following SQL command:
```
CREATE DATABASE `vistad`;
```

**[Step-6]** Open the command window/Terminal in the root extracted folder. _Make sure you are not in the sub-folder of the extracted folder_.

**[Step-7]** Run the following commands in the terminal/Command Line window.
> python -m venv venv

> .\venv\Scripts\activate

> pip install -r .\requirements.txt

> python manage.py migrate

Creating admin user is optional but required to access the admin site.
> python manage.py createsuperuser

Set your name, email and a strong password your super-user will be created to login in vista admin.

To start development server run the following command:
> python manage.py runserver

To open the website in browser go to: http://localhost:8000/

To open vista admin go to: http://localhost:8000/admin/
