import React from 'react';
import { Modal } from 'react-bootstrap';

const AppModal = React.createClass({
    
    render() {
        return (
            <Modal show={this.props.show} onHide={this.props.hide}>
                <Modal.Header closeButton>
                    <Modal.Title>{this.props.title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Order Placed Successfully! Download our app to track your order status.
                </Modal.Body>
            </Modal>
        );
    }
});

export default AppModal;
