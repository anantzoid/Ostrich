import React from 'react';
import { Modal } from 'react-bootstrap';
import Select from 'react-select';
import OrderUtils from '../utils/orderUtils';

const OrderModal = React.createClass({
    getInitialState() {
        let state = {default_address: {}};
        if (this.props.user) {
            state['user'] = this.props.user;
        } else {
            state['user'] = {};
        }
        return state;
    },
    componentWillUpdate() {
    },
    componentWillReceiveProps() {
    },
    _addressChange(option) {
        if (this.state.user.address) {
            for(let address of this.state.user.address) {
                if (address.address_id == option.value) {
                    this.setState({default_address: address});
                    break;
                }
            }    
        }
    },
    _slotChange(option) {
        this.state.default_address.default_timeslot = option.value;
        this.setState({default_address: this.state.default_address});
    },
    sendOrderData() {
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
        console.log(order_data);
        OrderUtils.placeOrder(order_data, this.props.hide, this.props.appModal);
    }, 
    render() {
        let addresses = [];
        if (this.state.user.address) {
            for(let address of this.state.user.address) {
                addresses.push({
                    value: address.address_id, 
                    label: address.description+', '+address.locality
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
                        <Select
                            name="address-selector"
                            value={ this.state.default_address.hasOwnProperty('address_id') 
                                ? this.state.default_address.address_id : null}
                            options={addresses}
                            onChange={this._addressChange}
                            searchable={false}
                            clearable={false}
                            placeholder="Select Delivery Address..."
                        />
                        <Select
                            name="time-selector"
                            value={ this.state.default_address.hasOwnProperty('default_timeslot') 
                                ? this.state.default_address.default_timeslot : null}
                            options={time_slots}
                            onChange={this._slotChange}
                            searchable={false}
                            clearable={false}
                            placeholder="Select Delivery Time..."
                            disabled={!this.state.default_address.hasOwnProperty('time_slot')}
                        />
                        <div className="payment-section clearfix mt20">
                            <div><strong>Payment Method:</strong></div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_cash" value="cash" defaultChecked/>
                                <label htmlFor="payment_cash">Cash</label>
                            </div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_credits" value="wallet"/>
                                <label htmlFor="payment_credits">Wallet <span className="faded">(₹ {this.state.user.wallet_balance})</span></label>
                            </div>
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className="btn btn-success" onClick={this.sendOrderData}>Place Order Now.</button>
                    </Modal.Footer>
                </Modal>
            );
    }
});

export default OrderModal; 
