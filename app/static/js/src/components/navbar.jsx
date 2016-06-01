import React from 'react';
import SearchBar from './searchbar';
import AppModal from './appModal';
import gAuth from '../utils/loginUtils.js'; 

const Navbar = React.createClass({
    getInitialState() {
        return {'show_app_modal': this.props.show_app_modal};
    },
    /*
    componentDidMount() {
        window.addEventListener('headerAuth', this._postAuth);
    }, 
    _postAuth(event) {
        this.setState({'user': event.detail})
    },
    */
    _toggleAppModal(title) {
        this.setState({
            'show_app_modal': !this.state.show_app_modal
        });
    },
    startAuth() {
        gAuth().then(function(response) {
            console.log("User Logged in!");
        });
    },
    render() {
        return(
        <nav className="navbar navbar-default">
        <div className="container-fluid">
            <div className="navbar-header">
               <a className="navbar-brand page-scroll" href="/">
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
                            <a id="googleAuth" href="#" onClick={this.startAuth}>Sign in</a>
                            :
                            <a id="userProfile" href="#" onClick={this._toggleAppModal}><img src={this.props.user.picture_url}/></a>
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
        <AppModal show={this.state.show_app_modal} hide={this._toggleAppModal} title="Download Ostrich" />
        </nav>
        );
    }
});

export default Navbar;
