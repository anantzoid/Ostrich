import React from 'react';
import SearchBar from './searchbar';
import AppModal from './appModal';
import gAuth from '../utils/loginUtils.js'; 

const Navbar = React.createClass({
    getInitialState() {
        return {'show_app_modal': this.props.show_app_modal};
    },
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
                    <img className="navbar-logo pull-left" src={this.props.cdn + "logo.png"} alt="Ostrich Logo" />
                    <div className="pull-left navbar-brand-name">Ostrich</div>
                </a>
            </div>

            <div className="navbar-collapse pull-right" id="bs-example-navbar-collapse-1">
                { this.props.user === null ?
                    <ul className="nav navbar-nav navbar-right">
                        <li className="">
                            <a className="page-scroll" href="#" onClick={this._toggleAppModal}>Get App</a>
                        </li>
                        <li className="auth-container">
                            <a id="googleAuth" href="#" onClick={this.startAuth}>Sign in</a>
                        </li>
                    </ul>
                    :
                    <ul className="nav navbar-nav navbar-right">
                        <li className="auth-container">
                            <a id="userProfile" href="#" onClick={this._toggleAppModal}><img src={this.props.user.picture_url} alt="User Avatar" /></a>
                        </li>
                    </ul>
                    }
            </div>
            { this.props.hasOwnProperty('page') && this.props.page !== 'home' ? 
                <SearchBar {...this.props} />
                : null }
        </div>
        <AppModal show={this.state.show_app_modal} hide={this._toggleAppModal} title="Download Ostrich" />
        </nav>
        );
    }
});

export default Navbar;
