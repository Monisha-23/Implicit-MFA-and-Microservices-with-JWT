# Implicit-MFA-and-Microservices-with-JWT

Data Security is the most crucial part of this digital era, everything we store online right from our account details to our  personal notes are been a target for a long time. We can't
eliminate the increasing data breaches or cyber attacks but we can make it complicate for the hackers to access the data. We can add an extra layer of protection to the data stored 
online so that the user can get accessed correctly without anyone impersonating. In my point of the main reasons of data breach starts when the user is *not autenticated aorrectly* or 
the there is *no enough protection for database*.

## About the project

As already mentioned about the main problem of data breaches, we can state that to overcome those issuse , developers had come with explicit way of authenticating the user and
protecting the database. While in this project would like to concentrate on 2 major solutions and adding some implicit ways to enhance it's performance and security too. And the two fields 
are the following :
 * MFA, Multifactor authentication : Using more than one method to verify the user and authenticating them, which includes traditional username and password, biometrics, otp etc.
 * Microservices : Microservices are an architectural and organizational approach to software development where software is composed of small independent services that communicate 
 over well-defined APIs
 
 ## Project Strategy
 
 In this project, I want to introduce to some ***implicit combinations of MFA***, which may add up extra security and also put up some innovative methodology of verifing a user.
 
        * Image as Passcode : We can use image as an digital fingureprint. Every user while register use a unique image to verify themselves. In the databse the image is not been stored instead,
                                   a hashcode is generated from that image and stored. While logging in , the user has to use the same image to authenticate themselves. Any change in the image i.e. croping or expanding or
                                   resizing etc. then the image will not be valid and thus the user is not authenticated.
 
        * Mouse Events as Passcode :  We can use mouse events like single or double clicks and scroll ups and downs to create an strong password, instead of creating 8- or 16- long password, we
                                 use some couple of clicks or scrolls to create a password. When ever an user logs in or signs up, a windows opens up and all the user's mouse events are reconized in that window later on closing 
                                 the window, the user's events are converted to hashcode before storing in the database. hence the user can use the same mouse events pattern to authenticate themselves everytime.
 
        * Patternized OTP : As we are familiar to OTP, we get an OTP and we enter the OTP and the user is authenticated. So instead of typing or entering OTP, we can patternize the OTP as we see in 
                               andorid or iOS lock patterns. For example if we get an OTP like 3-9-12 then the user is suppose to connect the dots at 3rd,9th and 12th position. In this way we can decrease the risk of bruteforce
                               attacks.
 
 This is one part of project, another part of this project includes data security using microservices. Practically we are seprating main data from the sensitive data, we will create an microservices 
 and store our sensitive data. But even we are seperating it, we still need a proper authentication so that the user can't access the data directly or to ensure there is no unautheorisaed access to 
 data. So we can use *Microservices with JWT*. How does this work ?
 
Step 1 : When ever the user creates an account in the main server, then automatically an account is created in other microservices too. 
Step 2 : If the user wants to access any data from microservices and requests the page, then the microservices creates an JWT, sends to gateway and asks the user to authenticate them using OTP.
Step 3 : If the user is authenticated then, the gateway adds an autheniction header to the JWT send by the microservices and sends it back.
Step 4 : Later the microservices check the signature of the token and if the user is validiated then sends back the requested page to user.

Thus, this way can add extra layers of security to the application which protects your sensitive data and also authenticates the user in more effective way.

## How to Run ?

* Install all the requirements provided in the requirements.txt
* Add your email id and password in views.py in main/userapp/views.py

```python 
  smtp = smtplib.SMTP('<Your-email-id>', 587)
  smtp.ehlo()
  smtp.starttls()
  smtp.login('<From-email-id>', '<email-password>')
```
 
* Run **main application** on *8000* server

 > py manage.py runserver 8000

* Run **api application** on *5000* server

> py manage.py runserver 5000

That's it, we're done!

## Tech-Stacks Invoved

<img src = "https://img.shields.io/badge/-HTML-yellow?style=for-the-badge&logo=HTML5" height = "40">&nbsp;&nbsp;<img src = "https://img.shields.io/badge/-CSS-blue?style=for-the-badge&logo=CSS3" height = "40">&nbsp;&nbsp;<img src = "https://img.shields.io/badge/-BOOTSTRAP-orange?style=for-the-badge&logo=Bootstrap" height = "40">&nbsp;&nbsp;<img src = "https://img.shields.io/badge/-DJANGO-green?style=for-the-badge&logo=DJANGO" height = "40">&nbsp;&nbsp;<img src = "https://img.shields.io/badge/-DJANGORESTFRAMEWORK-red?style=for-the-badge&logo=DJANGO-RESTFRAMEWORK" height = "40">

## Project Reference

<b>Source Code - https://github.com/Monisha-23/Implicit-MFA-and-Microservices-with-JWT</b>

## About The Developers

<table>
<tr>
  <td>

<a href = "https://github.com/Monisha-23">Chippada Monisha</a><br>
A third year undergraduate in B.Tech, Computer Science and Engineering at Guru Ghasidas Vishwavidyalaya, Bilaspur, India.<br/>
  </td>
</tr>
</table>

#### Reference And Copyright

 - Website copyright 2020 @ <a href = "https://github.com/Monisha-23">Chippada Monisha</a> 
 - Theme Reference  - Bootstrap
 - Code Snippet Reference - Codepen and W3Schools
 - Image Copyright - Unslash

 
 
 
