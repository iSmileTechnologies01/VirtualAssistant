## Overview
That's the simpliest API building based on the wifi script, I modify the file "index.js" to "wifi_module.js" to make the arrangement looks better.

after successfully start the server, go to "localhost:3000/search" using browser or Postman, you will see a list of wifi options in JSON format

# Requirement
package: nodemon, express, check-internet-connected
commands: 
        `npm init`
        `npm install --save-dev nodemon`
        `npm install express --save`
        `npm install check-internet-connected`

# Run
`npm run start`

# How to use
- To get all the Wifi connection available around you: 

simply navigate to `http://localhost:3000/search` or type `curl http://localhost:3000` in your terminal

- To connect to specific Wifi through SSID and PASSWORD:

Use HTTP POST request with corresponding request body.

Type `curl -X POST -H "Content-Type: application/json" -d "{ \"Password\": \"YOUR_PASSWORD\" }" http://localhost:3000/connect/YOUR_SSID` in your terminal. *Replace YOUR_PASSWORD with your password and YOUR_SSID with your ssid*