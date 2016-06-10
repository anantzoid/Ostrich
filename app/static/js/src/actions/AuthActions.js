import alt from '../alt';

class AuthActions {
    startAuth() {
        auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(this.signInCallback);
    }
    // TODO Move to approriate place 
    signInCallback(authResult) {
        if(authResult['code']) {
            $.ajax({
                type: 'POST',
                url: '/googlesignin',
                data: {'data': authResult['code']},
                success: function(response) {
                    $('#googleAuth').attr('style', 'display:none');
                    // NOTE this will not work. use flux flow
                    $('#userProfile img').attr('src', response.data.picture_url)
                    $('#userProfile').show();
                }
            });
        } else {
            alert('There was a login error');
        }
    }

}

module.exports = alt.createActions(AuthActions);
