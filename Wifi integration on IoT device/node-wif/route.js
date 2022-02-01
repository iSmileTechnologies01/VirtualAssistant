'use strict';
module.exports = function(app){
    var wifi = require('./wifi_module');
    app.route('/check')
        .get(wifi.check_internet);
    app.route('/search')
        .get(wifi.list_all_wifi);

    app.route('/connect/:Ssid')
        .post(wifi.conenect_to_wifi);
}