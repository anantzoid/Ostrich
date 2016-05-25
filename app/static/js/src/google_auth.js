let gAuth = function(){
    return new Promise(function(resolve, reject) {
        auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(signInCallback);

        function signInCallback(authResult) {
            if(authResult['code']) {
                $.ajax({
                    type: 'POST',
                    url: '/googlesignin',
                    data: {'data': authResult['code']},
                    beforeSend: () => { loaderBackdrop(true) },
                    success: function(response) {
                        // NOTE temporary. Since prop changes are not passed down to child.
                        // Will have to look into it.
                        location.reload();

                        window.renderApp($.extend(true, JSON.parse(store.props), response.data));
                        /*
                        var headerAuth = new CustomEvent('headerAuth', {'detail': response.data.user});
                        window.dispatchEvent(headerAuth);

                        var orderAuth = new CustomEvent('orderAuth', {'detail': response.data.user});
                        window.dispatchEvent(orderAuth);
                        */

                        resolve(response);
                        loaderBackdrop(false);       
                    },
                    error: () => {
                        loaderBackdrop(false);       
                    }
                });
            } else {
                alert('There was a login error');
            }
        } 
    });

    function loaderBackdrop(state) {
        const loader = '<div class="loader modal-backdrop fade in"><div class="loader-img"><img src="/static/img/loading.gif"></div></div>';
        if(state) {
            $('body').append(loader);
        } else {
            $('.loader').remove();
        }
    }
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
