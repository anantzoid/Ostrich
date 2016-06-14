import React from 'react';
import { Modal } from 'react-bootstrap';

const AppModal = React.createClass({
    
    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.hide} bsSize="sm">
                <Modal.Body closeButton bsClass="app-modal">
                    <div className="app-image-container">
                        <img className="app-image" src={this.props.cdn + 'tmp/showcase.png'} />
                    </div>
                    <div className="app-features">
                        <h3>Download our app to be a part of the easy reading experience</h3>
                        <ul>
                            <li><span className="glyphicon glyphicon-star riptide" aria-hidden="true"></span>Rent any book in a few taps</li>
                            <li><span className="glyphicon glyphicon-star riptide" aria-hidden="true"></span>Keep track and extend your orders</li>
                            <li><span className="glyphicon glyphicon-star riptide" aria-hidden="true"></span>Offer used books and get free credits</li>
                            <li><span className="glyphicon glyphicon-star riptide" aria-hidden="true"></span>Order Collection Sets</li>
                            <li><span className="glyphicon glyphicon-star riptide" aria-hidden="true"></span>Share with your friends</li>
                        </ul> 
                    </div>
                    <div className="app-link-container">
                        <a target="_blank" href='https://play.google.com/store/apps/details?id=in.hasslefree.ostrichbooks&hl=en&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'><img id="play-store" alt='Get it on Google Play' src='https://play.google.com/intl/en_us/badges/images/generic/en_badge_web_generic.png' data-source='modal' /></a>
                        </div>
                </Modal.Body>
            </Modal>
            
        );
    }
});

export default AppModal;

