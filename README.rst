================================
Treeo Django Web Application
================================



The web application is a django project.


User Model
==========
First we're going to go over the user account structure (it is an extention of the default Django user). 
There are three account profiles (seperate classes linked through foreign keys to the user account as detailed in the Django docunemtation): admin, patient, and provider. 
Each account has some inherent properties. Most of these are the Django defaults, however we did add some new properties for email confirmation, a profile picture, and a phone number.
Each user account profile has more values related to that specific profile. For example, the patient profile has field for the survey. 
We also store the relationships between the patients and providers here. 
Each of these profiles can be accessed by using their related name. You will use these to query these objects. 
In our project there are a number of Django apps that will be explained in detail.


Django Apps
============

1) users_acc
- In this app, the control all the functions related to the user account is managed here. This includes: logging in and logging out, registering a new user, survey functions, approving provider accounts as admin, and various other admin functions.

2) upload_download
- In the upload download section, we have the functions for uploading a file and downloading a file. The files are protected from being overwritten by files with the exact same name. There are also protections in the code for the correct file types, the correct file size, and the correct file name length. This also specifies the type of file as either a certificate, license, or other type of document.

3) ReqAppt
- This is the request appointment section. In here, we have all the functionality related to requesting an appointment, approving or rejecting an appointment, and the calendar.

4) patient_log
- In the patient log we have all the functions related to storing users patient log. There is also all the functions related to the generating the JavaScript charts using charge as these query the database and then return the data as a serialized series of values.

5) blogsys
- This is the current messaging system which which has a HTML page and view function for every possible combination of patient and provider.

6) apptArchive
- Here's the code for the archived appointments. This is where the providers will make notes on archived appointments. All users will be able to view any archived appointments that they have.



Dependencies
============
In this project, in order to accomplish the scope, we are relying on several dependencies.
They are located in the requirement.txt file.

1) The framework Django.

2) The MySQL connector in order to connect to the Azure database provided to us by Treeo.

3) Pillow to handle user profile pictures.

4) Chart js as the front end in order to handle the charts.

5) Babel for various language dependencies in the framework.

6) Zoom US in order to interface with the Zoom API.

7) Twillo in order to be able to send calls and text messages.

8) The django phone number field and django phone numbers was used for several features involving the phone numbers that we store for user accounts.

9) Celery and Flower are being used in order to run our asynchronous task queue. In addition, a local installation of their default messaging service rabbit MQ is required.

10) The django time zone detect module. This allows us to make sure that the times displayed are correct in all browsers by comparing the UTC offset of the browser to the appropriate time zones. This module, however, is flawed and does not always return the appropriate time zone. We compensated for this in the code especially in the charts page. It's important to note that a bespoke implementation might be a better fit, though the method for measuring the user's time zone using the UTC offset is still viable, though you could also go for an implementation using their public IP address to determine what time zone they are in.




Installation
============
In order to run this framework you will need to have at least one user account created that is an admin. You can create this account directly from the Django shell by creating a superuser account and then modifying its values either in the admin panel or in your database directly. From there, all accounts are added through the normal means or through the Django shell, though there may be some profile issues when adding accounts through the shell.
You must also be running a celery worker, so the tasks execute properly.
celery -A Treeo worker -l info --pool=solo
flower -A Treeo --port=5555



Deployment
----------
In order to deploy a Django application you must make some changes involving the static files and debug flag.
The celery and flower server configuration must be completed using these commands in separate terminals.




License
=======
The License of the packages are available on their respective pypi.org pages .

