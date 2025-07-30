# BlaBlaCar_CaseStudy_LouisMDV

Thank you for taking the time to check my code. This repository is private and contains the subject and my code to trace Bus routes on an a map.

Here are the steps to follow to make the code executable:

1. This python program uses the open routing service API so you will need to login to open routing service either using an account or your GitHub account.
From there, you can get a free API key.
Here is the link to their login page:
    https://account.heigit.org/login
Once logged-in click on your persona icon to get your API key. Once you have your key hold on to it!

2. The next step will be creating a dot .env file:
    > touch .env
And add your API key to it as below:
    > ORS_API_KEY = "api-key-here"

3. Now we need to create and activate a virtual environment to store all the packages we are going to use in this program:
    > python3 -m venv venv
    > source venv/bin/activate

4. Once the venv is activated you can install the requirement packages for the program to run:
    > pip install -r requirements.txt

That's it! Enjoy tracing Bus routes!

Louis
