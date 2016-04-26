/*
(function(global) { 
    global.start = function() {
        console.log("here");
        global.gapi.load('auth2', function() {
            console.log("where");
            var auth2 = gapi.auth2.init({
                client_id: '487125469761-4anu3rqa9koulgjjkujj38miba15epu9.apps.googleusercontent.com' 
            });
        });
    }
}(this));
$('#googleAuth').click(function() {
    auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(signInCallback);
});

function signInCallback(authResult) {
    if(authResult['code']) {
        $.ajax({
            type: 'POST',
            url: '/googlesignin',
            data: authResult['code'],
            contentType: 'application/octet-stream; charset=utf-8',
            processData: false,
            success: function(response) {
                $('#googleAuth').attr('style', 'display:none');
            }
        });
    } else {
        alert('There was a login error');
    }
};
*/


(function(global) {

    var a = gapi.auth2.getAuthInstance();
    console.log(a.isSignedIn.get());
    console.log(a.currentUser.get());
    //TODO replace with gauth
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
