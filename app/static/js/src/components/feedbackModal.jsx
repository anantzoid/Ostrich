import React from 'react';
import { Modal } from 'react-bootstrap';
import FeedbackUtils from '../utils/feedbackUtils.js';

const FeedbackModal = React.createClass({
    _submit() {
        let email = this.props.user ? this.props.user.email : $(".feedback-email").val(); 
        let subject = $(".feedback-subject").val();
        let description = $(".feedback-description").val();

        if (!email || (email && !FeedbackUtils.validateEmail(email))) {
            this._renderError('email');
        } else if (!subject) {
            this._renderError('subject');
        } else {
            FeedbackUtils.submit({email:email, 
                subject:subject, 
                description:description}).then(() => {
                FeedbackUtils.toggleModal();
            }); 
        }
    },
    render() {
        return (
                <Modal show={this.props.feedback_form} onHide={FeedbackUtils.toggleModal} bsSize="sm">
                    <Modal.Header closeButton>
                        <Modal.Title>Feedback Form</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="feedback-form">
                            {!this.props.user ?
                                <input className="feedback-email" type="text" placeholder="Email" onFocus={this._removeError}/>   
                            : null }
                            <input className="feedback-subject" type="text" placeholder="Subject" onFocus={this._removeError}/>   
                            <textarea className="feedback-description" placeholder="Please tell us about a bug you noticed or a feature that you may like to see..."></textarea>   
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className="btn btn-primary feedback-submit" onClick={this._submit}>Submit</button>
                    </Modal.Footer>
                </Modal>
            );
    },
    _renderError(type) {
        switch(type) {
            case 'email':
                $('.feedback-email').addClass('error');
                break;
            case 'subject':
                $('.feedback-subject').addClass('error');
                break;
        }
    },
    _removeError() {
        $('.error').removeClass('error'); 
    },
});

export default FeedbackModal; 
