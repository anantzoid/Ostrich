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
                        $(".auth-container").html('<a id="userProfile"><img src="'+response.data.picture_url+'"/></a>');
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
