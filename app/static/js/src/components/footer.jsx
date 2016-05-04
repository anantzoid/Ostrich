import React from 'react';

const Footer = React.createClass({
    render() {
        return (
                <footer className="footer">
                    <div className="container">
                        <div className="row">
                            <div className="col-lg-3">

                                <img className="footer-logo pull-left" src="/static/img/logo.png" />
                                <div className="pull-left footer-brand-name">Ostrich</div>
                            </div>
                            <div className="col-lg-6">
                            </div>
                            <div className="col-lg-3">
                                Terms and Conditions
                            </div>
                        </div>
                    </div>
                </footer>
            );
    }
});

export default Footer;
