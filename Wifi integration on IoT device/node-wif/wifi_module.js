

// npm package  https://www.npmjs.com/package/node-wifi

// Running the command

// https://www.npmjs.com/package/node-wifi
// node index.js


// Get request
// /getwifi  returns all avaialble wifis to connect
// Post request
// /connect pst request gets ssid and password from web/ desktop and connects to wifi

'use strict';
const wifi = require('node-wifi');
const checkInternetConnected = require('check-internet-connected');

function checkInternet(cb){
  require('dns').lookup('google.com',function(err){
    if(err && err.code == "ENOTFOUND"){
      cb(false);
    }else{
      cb(true);
    }
  })
}

exports.check_internet = function(req,res){
  // res.json({test:"No"});
  checkInternetConnected()
    .then((result) => {
      console.log(result);
      res.json({status:"Yes"});
    })
    .catch((ex) => {
      console.log(ex);
      res.json({status:"No"});
    });
  // checkInternet(function(isConnected){
  //   if(isConnected){
  //     console.log("success");
  //     res.json({status:"Yes"});
  //   }else{
  //     console.log("success");
  //     res.json({status:"No"});

  //   }
  // });
}
 
//   Displays all available nearby wifis
  // Scan networks
exports.list_all_wifi = function(req,res){
  wifi.init({
    iface: null 
  });
  wifi.scan((error, networks) => {
    if (error) {
      console.log("error scanning networks");
      console.log(error);
    } else {
      console.log("available networks: ");
      console.log(networks);
      res.json(networks);
    }
  });
}


  
 // trys to connect with wifi with name Utkarsh and password Utkarshwifi
exports.conenect_to_wifi = function(req,res){
  var ssid_para = req.params.Ssid;
  console.log(ssid_para);
  var password_para = req.body.Password;
  console.log(password_para);
  wifi.init({
    iface: null 
  });
  wifi.connect({ ssid: ssid_para, password: password_para }, error => {
    if (error) {
      console.log("failed to connect with wifi");
      console.log(error);
      res.json({status: 'fail',message:'Failed to connect with wifi'});
    }
    else { 
    console.log("Wifi connected");
    console.log('Connected');
    res.json({status: 'success',message: "You are now connected to Internet!"})
    }
  });

}
