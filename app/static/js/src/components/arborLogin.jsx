import React from 'react';
import ArborNavbar from './arborNavbar';
import Footer from './footer';
import { gAuth } from '../utils/loginUtils.js'; 

const ArborLogin = React.createClass({
    startAuth() {
        gAuth().then(function(response) {
            location.reload();
        });
    },
    render() {
        return(
            <div className="arbor">
                <ArborNavbar {...this.props} />
                <section className="arbor-login">
                    <div className="container">
                        <div className="row">
                            <div className="col-lg-2"></div>
                            <div className="col-lg-9">
                                <h3>Welcome to Paypal's Arbor Dashboard. Please Login to Continue</h3>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-lg-4"></div>
                            <div className="col-lg-4">
                                <div className="login-container">
                                    <div><a href="#" onClick={this.startAuth}><img className="order-gauth mt20" src={this.props.cdn + "auth/btn_google_signin_dark_normal_web.png"} alt="Ostrich Sign in" srcSet={this.props.cdn + "auth/btn_google_signin_dark_normal_web@2x.png 2x"}/></a></div>
                            </div> 
                            </div>
                        </div>
                    </div>
                </section>
                <Footer {...this.props} />
           </div> 
            );
    }
});

module.exports = ArborLogin;
