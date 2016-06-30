let gAuth = function(){
    return new Promise(function(resolve, reject) {
        auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(signInCallback);

        function signInCallback(authResult) {
            let client = store.props.hasOwnProperty('client') ? store.props.client:null;
            if(authResult['code']) {
                $.ajax({
                    type: 'POST',
                    url: store.props.host + 'googlesignin',
                    data: {'data': authResult['code'], 'client': client},
                    beforeSend: () => { loaderBackdrop(true) },
                    success: function(response) {
                        loaderBackdrop(false);       
                        store.props = $.extend(true, store.props, response.data);
                        window.renderApp(store.props);
                        /*
                        var headerAuth = new CustomEvent('headerAuth', {'detail': response.data.user});
                        window.dispatchEvent(headerAuth);

                        var orderAuth = new CustomEvent('orderAuth', {'detail': response.data.user});
                        window.dispatchEvent(orderAuth);
                        */

                        resolve(response);
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

}

let signout = function() {
    $.ajax({
        type: 'POST',
        url: '/signout',
        beforeSend: () => { loaderBackdrop(true) },
        success: function(response) {
            loaderBackdrop(false);       
            store.props.user = null;
            window.renderApp(store.props);
        },
        error: () => {
            loaderBackdrop(false);       
        }
    });
 
}

function loaderBackdrop(state) {
    const loader = '<div class="loader modal-backdrop fade in"><div class="loader-img"><img src="'+store.props.cdn + 'loading.gif" /></div></div>';
    if(state) {
        $('body').append(loader);
    } else {
        $('.loader').remove();
    }
}

module.exports = {
    gAuth: gAuth,
    signout: signout
};

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
