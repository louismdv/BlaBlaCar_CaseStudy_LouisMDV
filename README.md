# BlaBlaCar_CaseStudy_LouisMDV

Thank you for taking the time to check my code. This repository is private and contains the subject and my code to draw Bus routes on a map.

Here are the steps to follow to run the code:

1. This python program uses the open routing service API. So you will need to login to open routing service either using an account or your GitHub account. 
From there, you can get a free API key.
Here is the link to the login page:
```bash
    https://account.heigit.org/login 
```
Once logged-in click on your persona icon to get your API key. Once you have your key hold on to it!

2. The next step will be creating a dot .env file. From the root directory run:
```bash
    touch .env
```
And add your API key in the file as below:
```bash
    ORS_API_KEY = "api-key-here"
```
3. Now we need to create and activate a virtual environment to store all the packages we are going to use in this program:
```bash
    python3 -m venv venv
    source venv/bin/activate
```
4. Once the venv is activated you can install the required packages for the program to work:
```bash    
    pip install -r requirements.txt
```

To launch the program just run:
```bash
    python draw_route.py
```
You can input your own Bus stations with coordinates or use the tester.py:
```bash
    python tester.py
```
That's it! Enjoy tracing Bus routes!

Louis
