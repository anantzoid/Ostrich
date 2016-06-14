import React from 'react';

const Footer = React.createClass({
    componentDidMount() {
        $('.search-links').hide();
    },
    render() {
        let search_links = [];
        if (this.props.hasOwnProperty('categories')) {
            for(let category of this.props.categories) {
                let link_title = 'Rent '+category.category_name+' books in Bangalore, ';
                search_links.push(<a className="" href={category.slug_url} title={link_title}>{link_title}</a>);
                link_title = 'Rent '+category.category_name+' books in Bengaluru, ';
                search_links.push(<a className="" href={category.slug_url} title={link_title}>{link_title}</a>);
            }
        } 
    
        return (
                <footer className="footer">
                    <div className="container">
                        <div className="row footer-top">
                            <div className="col-lg-9 col-xs-12">
                                <ul className="clearfix footer-links">
                                    <li key="about" className="footer-info-li">
                                        <h4>About</h4>
                                        <ul className="footer-info-subul">
                                            <li>
                                                <a href="mailto:contact@ostrichapp.in">Contact Us</a>
                                            </li>
                                            <li>
                                                <a href="/terms">Terms and Conditions</a>
                                            </li>
                                        </ul>
                                    </li>
                                    <li key="social" className="footer-info-li">
                                        <h4>Stay in touch</h4>
                                        <ul className="footer-info-subul">
                                            <li>
                                                <a href="https://www.facebook.com/Ostrichapp" target="_blank">Facebook</a>
                                            </li>
                                            <li>
                                                <a href="https://twitter.com/ostrichappin" target="_blank">Twitter</a>
                                            </li>
                                            <li>
                                                <a href="https://www.instagram.com/ostrichbooks/" target="_blank">Instagram</a>
                                            </li>
                                            <li>
                                                <a href="https://medium.com/@ostrichapp" target="_blank">Medium</a>
                                            </li>
                                        </ul>
                                    </li>
                                    <li key="legal" className="footer-info-li">
                                        <h4></h4>
                                        <ul className="footer-info-subul">
                                        </ul>
                                    </li>


                                </ul>
                            </div>
                            <div className="col-lg-3 col-xs-12">
                                <img className="footer-logo pull-left mt20" src={"https://s3-ap-southeast-1.amazonaws.com/ostrich-catalog/website/logo.png"} alt="Ostrich Logo"/>
                                <div className="pull-left footer-brand-name">Ostrich</div>
                            </div>
                        </div>
                        <div className="row footer-bottom">
                            <div className="col-lg-3">
                                <div className="copy mt20">© 2016 Hassle Free Internet Pvt. Ltd.</div>
                            </div>
                            <div className="col-lg-5">
                            </div>
                            <div className="col-lg-4 col-xs-12">
                                <a className="footer-app-links" target="_blank" href='https://play.google.com/store/apps/details?id=in.hasslefree.ostrichbooks&hl=en&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img id="play-store" alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png' data-source='footer' /></a>

                                <a className="footer-app-links" href="https://slack.com/oauth/authorize?scope=users:read,incoming-webhook,commands&client_id=4256151918.31600537060&redirect_uri=https://ostrich-slack.herokuapp.com/oauth"><img id="slack-app-footer" alt="Add to Slack" src="https://platform.slack-edge.com/img/add_to_slack.png" srcSet="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>
                            </div>
                        </div>
                    </div>
                    <div className="search-links">
                        <section role="group">{search_links}</section>
                    </div>
                </footer>
            );
    }
});

export default Footer;
