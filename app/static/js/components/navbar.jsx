import React from 'react';

const Navbar = React.createClass({
    startAuth() {
        auth2.grantOfflineAccess({'redirect_uri':'postmessage'}).then(this.signInCallback);
    },
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
    },
    render() {
        return(
        <nav className="navbar navbar-default">
        <div className="container-fluid">
            <div className="navbar-header">
               <a className="navbar-brand page-scroll" href="#page-top">
                    <img className="navbar-logo pull-left" src="/static/img/logo.png" />
                    <div className="pull-left navbar-brand-name">Ostrich</div>
                </a>
            </div>

            <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul className="nav navbar-nav navbar-right">
                    <li className="">
                        <a className="page-scroll" href="#about">About</a>
                    </li>
                    <li className="">
                        { this.props.user === null ?
                            <a id="googleAuth" href="#" onClick={this.startAuth}>Sign in with Google</a>
                            :
                            <a id="userProfile"><img src={this.props.user.picture_url}/></a>
                        }
                    </li>
               </ul>
            </div>
        </div>
        </nav>
        );
    }
});

export default Navbar;
