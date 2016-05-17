let gAuth = function(){
    return new Promise(function(resolve, reject) {
        auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(signInCallback);

        function signInCallback(authResult) {
            if(authResult['code']) {
                $.ajax({
                    type: 'POST',
                    url: '/googlesignin',
                    data: {'data': authResult['code']},
                    success: function(response) {
                        window.renderApp($.extend(true, JSON.parse(store.props), response.data));
                        /*
                        var headerAuth = new CustomEvent('headerAuth', {'detail': response.data.user});
                        window.dispatchEvent(headerAuth);

                        var orderAuth = new CustomEvent('orderAuth', {'detail': response.data.user});
                        window.dispatchEvent(orderAuth);
                        */

                        resolve(response);
                    }
                });
            } else {
                alert('There was a login error');
            }
        } 
    });
}
module.exports = gAuth;

/*
(function(global) {

    global.onSignIn = function(googleUser) {
        var id_token = googleUser.getAuthResponse().id_token;
        var xhr = new XMLHttpRequest();
        xhr.open('POST', 'http://localhost:5000/googlesignin');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            console.log('Signed in as:' + xhr.responseText);
        };
        xhr.send('idtoken=' + id_token);    
    }
}(this));
*/
