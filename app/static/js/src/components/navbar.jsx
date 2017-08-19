import React from 'react';
import SearchBar from './searchbar';
import AppModal from './appModal';
import FeedbackUtils from '../utils/feedbackUtils.js';
import { gAuth, signout} from '../utils/loginUtils.js'; 

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
        <div className="ribbon-wrapper"><div className="ribbon" onClick={FeedbackUtils.toggleModal}>BETA</div></div>
        <div className="container-fluid">
            <div className="navbar-header">
                <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false" aria-controls="navbar">
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                </button>
                <a className="navbar-brand page-scroll" href="/">
                    <img className="navbar-logo pull-left" src={this.props.host+"static/img/logo.png"} alt="Ostrich Logo" />
                    <div className="pull-left navbar-brand-name">Ostrich</div>
                </a>
            </div>

            <div className="navbar-collapse collapse text-left" id="bs-example-navbar-collapse-1">
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
                        <li className="dropdown auth-container">
                            <a data-toggle="dropdown" className="dropdown-toggle" id="userProfile" href="#" >
                                <img src={this.props.user.picture_url} alt="User Avatar" />
                                <span>{this.props.user.first_name}
                                <b className="caret"></b>
                                </span>
                            </a>
                            <ul className="dropdown-menu">
                            <li><a className="disabled">My Orders (Coming Soon)</a></li>
                            <li><a href="#" onClick={this._toggleAppModal}>Get App</a></li>
                            <li><a href="#" onClick={signout}>Signout</a></li>
                        </ul>
                        </li>
                    </ul>
                    }
            </div>
            { this.props.hasOwnProperty('page') && this.props.page !== 'home' ? 
                <SearchBar {...this.props} />
                : null }
        </div>
        <AppModal show={this.state.show_app_modal} hide={this._toggleAppModal} {...this.props} title="Download Ostrich" />
        </nav>
        );
    }
});

export default Navbar;
