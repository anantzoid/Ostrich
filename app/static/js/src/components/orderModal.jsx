import React from 'react';
import { Modal } from 'react-bootstrap';
import Select from 'react-select';
import OrderUtils from '../utils/orderUtils';

const OrderModal = React.createClass({
    getInitialState() {
        let state = {
            show: this.props.show,
            default_address: {},
            total_amount: this.props.item_data.custom_price
        };
        if (this.props.user) {
            state['user'] = this.props.user;
        } else {
            state['user'] = {};
        }
        return state;
    },
    _addressChange(option) {
        if (this.state.user.address) {
            for(let address of this.state.user.address) {
                if (address.address_id == option.value) {
                    this.setState({default_address: address});
                    break;
                }
            }    
            if (this.state.default_address.hasOwnProperty('delivery_charge')) {
                this.setState({total_amount: this.props.item_data.custom_price + this.state.default_address.delivery_charge});
            }
        }
    },
    _slotChange(option) {
        this.state.default_address.default_timeslot = option.value;
        this.setState({default_address: this.state.default_address});
    },
    sendOrderData() {
        if($.isEmptyObject(this.state.default_address)) {
            this._renderError('address');
        } else if(!this.state.default_address.hasOwnProperty('default_timeslot')) {
            this._renderError('time');
        } else {
            let delivery_info = this.state.default_address.default_timeslot.split(":");
            let pay_option = $('input[name=payment-option]:checked').val();
            let order_data = {
                item_id: this.props.item_data.item_id,
                user_id: this.props.user.user_id,
                address_id: this.state.default_address.address_id,
                payment_mode: pay_option,
                delivery_slot: delivery_info[0],
                delivery_date: delivery_info[1]
            };
            OrderUtils.placeOrder(order_data, this.props.hide, this.props.appModal);
        }
    }, 
    render() {
        let addresses = [];
        if (this.state.user.hasOwnProperty('address')) {
            for(let address in this.state.user.address) {
                address = this.state.user.address[address];
                addresses.push({
                    value: address.address_id, 
                    label: address.description+', '+address.locality,
                    disabled: address.is_valid ? false : true
                }); 
            }
        }
        let time_slots = [];
        if (this.state.default_address.hasOwnProperty('time_slot')) {
            for(let slot of this.state.default_address.time_slot) {
                time_slots.push({
                    value: slot.slot_id + ":" + slot.delivery_date, 
                    label: slot.formatted
                });
            }
        }
        return (
                <Modal show={this.props.show} onHide={this.props.hide}>
                    <Modal.Header closeButton>
                        <Modal.Title>Placing order</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="order-error-msg collapse"></div>
                        <Select
                            className="address-selector"
                            value={ this.state.default_address.hasOwnProperty('address_id') 
                                ? this.state.default_address.address_id : null}
                            options={addresses}
                            onChange={this._addressChange}
                            searchable={false}
                            clearable={false}
                            placeholder="Select Delivery Address..."
                            onFocus={this._removeError}
                        />
                        <Select
                            className="time-selector"
                            value={ this.state.default_address.hasOwnProperty('default_timeslot') 
                                ? this.state.default_address.default_timeslot : null}
                            options={time_slots}
                            onChange={this._slotChange}
                            searchable={false}
                            clearable={false}
                            placeholder="Select Delivery Time..."
                            disabled={!this.state.default_address.hasOwnProperty('time_slot')}
                            onFocus={this._removeError}
                        />
                        <div className="payment-section clearfix mt20">
                            <div><strong>Payment Method:</strong></div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_cash" value="cash" defaultChecked/>
                                <label htmlFor="payment_cash">Cash</label>
                            </div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_credits" value="wallet" disabled={!this.state.user.wallet_balance}/>
                                <label htmlFor="payment_credits">Wallet {this.state.user.wallet_balance ? <span className="faded">(₹ {this.state.user.wallet_balance})</span> : null }</label>
                            </div>
                        </div>
                        <div className="bill-section">
                            <div className="bill-entity clearfix">
                                <div className="bill-label">Rental Amount:</div>
                                <div className="bill-amount">₹ {this.props.item_data.custom_price}</div>
                            </div>
                            {this.state.default_address.hasOwnProperty('delivery_charge') ?

                                <div className="bill-entity clearfix">
                                    <div className="bill-label">Delivery Charge:</div>
                                    <div className="bill-amount">₹ {this.state.default_address.delivery_charge}</div>
                                </div> 
                                : null }

                            <div className="bill-entity bill-total clearfix">
                                <div className="bill-label">Total Amount:</div>
                                <div className="bill-amount">₹ {this.state.total_amount}</div>
                            </div>
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className="btn add-address pull-left" onClick={this.props._toggleAddressModal}>+ Add New Address</button>
                        <button className="btn btn-success place-order" onClick={this.sendOrderData}>Place the Order</button>
                    </Modal.Footer>
                </Modal>
            );
    },
    _renderError(type) {
        switch(type) {
            case 'address':
                $('.address-selector').addClass('error');
                break;
            case 'time':
                $('.time-selector').addClass('error');
                break;
        }
    },
    _removeError() {
        $('.error').removeClass('error'); 
        $('.order-error-msg').slideUp('slow');
    },
});

export default OrderModal; 
