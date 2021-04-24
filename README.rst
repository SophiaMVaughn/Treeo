================================
Treeo Django Web Application
================================



The web application is a django project.


User Model
==========
First were going to go over the user account structure(it is and extention of the default django user). There are three account profiles(seperate classes linked through foreign keys to the user account as detailed in the django docunemtatoin) admin user and provider. Each account has some inherent properties most of these of the Jango defaults however we did add some for email confirmation , a profile picture, and we added a phone number. Each user account profile has more values related to that specific profile for example the patient profile has a fields for the survey. We also store the relationships between the patients and providers here. Each of these profiles can be accessed by using their related name. You will use these to query these objects. In our project there are a number of Django apps will go into each one of them in detail now.


Django Apps
============

1) Users_acc
- In this app the control all the functions related to the user account these include logging in and logging out registering a new user approving provider accounts as admin and various other admin functions as well as the survey functions.

2) upload_download
- In the upload download section we have the functions for uploading a file and downloading file the files are protected against files being overridden for having the same name as well as protections in the code for the correct file types, the correct file size and the correct file name length. This also specifies the type of file as either a certificate license or other type of document.

3) ReqAppt
- This is the request appointment section in the request appointment section we have all the functionality related to requesting an appointment approving an appointment or rejecting an appointment there's also code here for the calendar.

4) patient_log
- In the patient log we have all the functions related to storing users patient log we also have all the functions related to the generating the JavaScript charts using charge as these query the database and then return the data as a serialized series of values.

5) messaging
- This is the current messaging system which which has a HTML page and view function for every possible combination of patient provider and user

Depreciated
5) blogsys
- This is the current messaging system which which has a HTML page and view function for every possible combination of patient provider and user

6) apptArchive
- Here's the code for the archived appointments this is where the providers will make notes on said archived appointments and all users will be able to view whatever appointments they have that have been archived.



Dependencies
============
In this project in order to accomplish the scope we are relying on several dependencies
They are located in the requirement.txt

1) First our framework django

2) next we use the MySQL connector in order to connect to the Azure database provided to us by Treeo.

3) We also needed to install pillow in order to handle user profile pictures

4) We installed chart js as as the front end in order to handle our charts.

5) We installed Babel for various language dependencies in the framework.

6) We then installed zoom US in order to interface with the zoom API

7) We also installed twillo in order to be able to send calls and text messages

8) The django phone number field and django phone numbers was used for several features involving the phone numbers that we store for user accounts.

9) Celery and flower are being used in order to run our asynchronous task queue in addition to these a local installation of their default messaging service rabbit MQ is required

10) we also are using the django time zone detect module this allows us to make sure that the times displayed are correct in all browsers by comparing the UTC offset of the browser to the appropriate time zones. This module, however, is flawed and does not always return the appropriate time zone. We compensated for this in the code especially in the charts page. It's important to note that a bespoke implementation might be a better fit, though the method for measuring the user's time zone using the UTC offset is still viable, though you could also go for an implementation using their public IP address to determine what time zone they are in.

11) we also are using the django_otp module To generate the one time passwords for two factor authentication.

12) we also are using the django guardian module to implement object based permissions.





Installation
============
In order to run this framework you will need to have at least one user account created that is an administrator you can create this account directly from the django shell by crating a superuser account and then modifying its values either in the admin panel or in your database directly from their all accounts to me added to the normal means or through the django shell though there may be some profile issues adding accounts through the shell.
You must also be running a celery worker so the tasks execute properly.




Deployment
---------
In order to deploy a django application you must make some changes involving the static files and debug flag.
Also the celery and flower server configuration must be completed.



License
=======
The License of the packages are available on their respective pypi.org pages .

