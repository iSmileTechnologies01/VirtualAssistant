# Introduction
This is a demo user interface for user to connect to Internet through Wifi. (Still under development)

Developed using Flask. Calling API from my own implementation: https://github.com/LoneRan/Simple-wifi-API

# Requirement
python3
flask

Make sure the Node.js API is running before you proceed, use `npm run start` to run Node.js API running at background. Refer to README.md of API for more information.

After API is running in background:
To start flask application: `python3 -m flask run`

# How to use
1. Navigate to `http://localhost:5000`
2. Click the icon in the middle to next step
3. select wifi you want to connect to and type in the password
4. click 'submit'