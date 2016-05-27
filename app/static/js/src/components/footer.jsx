import React from 'react';

const Footer = React.createClass({
    render() {
        return (
                <footer className="footer">
                    <div className="container">
                        <div className="row footer-top">
                            <div className="col-lg-3">
                                <img className="footer-logo pull-left" src="/static/img/logo.png" />
                                <div className="pull-left footer-brand-name">Ostrich</div>
                            </div>
                            <div className="col-lg-6">
                            </div>
                            <div className="col-lg-3">
                                <a target="_blank" href='https://play.google.com/store/apps/details?id=in.hasslefree.ostrichbooks&hl=en&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img id="play-store" alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png'/></a>
                                <a target="_blank" href="#"><img id="slack-app-footer" src="/static/img/slack.png" /></a>
                            </div>
                        </div>
                        <div className="row footer-bottom">
                            <div className="col-lg-3">
                                <div className="left-info">
                                    <a href="mailto:contact@ostrichapp.in">Contact Us</a>
                                    <a href="/terms">Terms and Conditions</a>
                                </div>
                            </div>
                            <div className="col-lg-6">
                            </div>
                            <div className="col-lg-3 social-container">
                                <a href="https://www.facebook.com/Ostrichapp/" target="_blank">
                                    <svg viewBox="0 0 24 24">
                                        <path fill="#00bcd4" d="M17,2V2H17V6H15C14.31,6 14,6.81 14,7.5V10H14L17,10V14H14V22H10V14H7V10H10V6A4,4 0 0,1 14,2H17Z" />
                                    </svg>
                                </a>
                                <a href=" https://twitter.com/ostrichappin" target="_blank">
                                    <svg viewBox="0 0 24 24">
                                        <path fill="#00bcd4" d="M22.46,6C21.69,6.35 20.86,6.58 20,6.69C20.88,6.16 21.56,5.32 21.88,4.31C21.05,4.81 20.13,5.16 19.16,5.36C18.37,4.5 17.26,4 16,4C13.65,4 11.73,5.92 11.73,8.29C11.73,8.63 11.77,8.96 11.84,9.27C8.28,9.09 5.11,7.38 3,4.79C2.63,5.42 2.42,6.16 2.42,6.94C2.42,8.43 3.17,9.75 4.33,10.5C3.62,10.5 2.96,10.3 2.38,10C2.38,10 2.38,10 2.38,10.03C2.38,12.11 3.86,13.85 5.82,14.24C5.46,14.34 5.08,14.39 4.69,14.39C4.42,14.39 4.15,14.36 3.89,14.31C4.43,16 6,17.26 7.89,17.29C6.43,18.45 4.58,19.13 2.56,19.13C2.22,19.13 1.88,19.11 1.54,19.07C3.44,20.29 5.7,21 8.12,21C16,21 20.33,14.46 20.33,8.79C20.33,8.6 20.33,8.42 20.32,8.23C21.16,7.63 21.88,6.87 22.46,6Z" />
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>
                </footer>
            );
    }
});

export default Footer;
