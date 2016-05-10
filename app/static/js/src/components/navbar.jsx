import React from 'react';
import SearchBar from './searchbar';
import gAuth from '../google_auth.js'; 

const Navbar = React.createClass({
    startAuth() {
        gAuth().then(function(response) {
            $(".auth-container").html('<a id="userProfile"><img src="'+response.data.picture_url+'"/></a>');
        });
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
                    <li className="auth-container">
                        { this.props.user === null ?
                            <a id="googleAuth" href="#" onClick={this.startAuth}>Sign in with Google</a>
                            :
                            <a id="userProfile"><img src={this.props.user.picture_url}/></a>
                        }
                    </li>
               </ul>
               { this.props.hasOwnProperty('page') && this.props.page !== 'home' ? 
                    <SearchBar {...this.props} />
                   :
                    null
                }
            </div>
        </div>
        </nav>
        );
    }
});

export default Navbar;
