import React from 'react';
import { Modal } from 'react-bootstrap';

const OrderModal = React.createClass({
    getInitialState() {
        if (this.props.user) {
            return {'user': this.props.user};
        } else {
            return {'user': {}};
        }
    },
    render() {
        return (
                <Modal show={this.props.show} onHide={this.props.hide}>
                    <Modal.Header closeButton>
                        <Modal.Title>Placing order</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                      <div>
                            <div>
                                Select Address: 
                            </div>
                            <select id="category_id" className="category-picker" multiple onChange={this._onChange}>
                                <option id="default" disabled="disabled" value="default">Select address</option>
                            </select>
                            <div className="payment-section clearfix mt20">
                                <div><strong>Payment Method:</strong></div>
                                <div className="payment-options">
                                    <input type="radio" name="payment-option" id="payment_cash" value="cash"/>
                                    <label htmlFor="payment_cash">Cash</label>
                                </div>
                                <div className="payment-options">
                                    <input type="radio" name="payment-option" id="payment_credits" value="credits"/>
                                    <label htmlFor="payment_credits">Credits: ₹ {this.state.user.wallet_balance}</label>
                                </div>
                            </div>
                    </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className="btn btn-success">Place Order Now.</button>
                    </Modal.Footer>
                </Modal>
            );
    }
});

export default OrderModal; 
