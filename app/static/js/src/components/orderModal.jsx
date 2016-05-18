import React from 'react';
import { Modal } from 'react-bootstrap';

const OrderModal = React.createClass({
    getInitialState() {
        let state = {'default_address': {}};
        if (this.props.user) {
            state['user'] = this.props.user;
            // TODO set defautlt_address
            if (this.props.user.address.length) {
                state['default_address'] = this.props.user.address[0];
            }
        } else {
            state['user'] = {};
        }
        return state;
    },
    componentDidMount() {
        /*
        $(".address-selector").selectpicker({
            width: 500
        });
        */
        $(document).ready(function() {
            $(".time-selector").selectpicker();
        });
    },
    componentDidUpdate() {
        $(".time-selector").selectpicker('refresh'); 
    },
    _addressChange(event) {
        for(let address of this.state.user.address) {
            if (address.address_id == event.target.value) {
                this.setState({'default_address': address});
                break;
            }
        }    
    },
    _placeOrder() {
        let time_slot = $(".time-selector").val();
        let pay_option = $('input[name=payment-option]:checked').val();
        let order_data = {
            item_id: this.props.item_data.item_id,
            user_id: this.props.user.user_id,
            address_id: this.state.default_address.address_id,
            payment_mode: pay_option,
            delivery_slot: time_slot
        };
        $.ajax({
            type: 'POST',
            url: '/order',
            data: order_data,
            success:((response) => {
                if (response.hasOwnProperty('order_id')) {
                    //TODO render app download banner
                }
            })
        });
    },
    render() {
        let addresses = this.state.user.address.map((address) => {
            let key = "address-"+address.address_id;
            return (<option key={key} value={address.address_id}>
                        {address.locality}
                    </option>);
        });

        let time_slots = this.state.default_address.time_slot.map((slot) => {
                let key = "slot-"+slot.slot_id;
                return <option key={key} value={slot.slot_id}>{slot.formatted}</option>;    
        });

        return (
                <Modal show={this.props.show} onHide={this.props.hide}>
                    <Modal.Header closeButton>
                        <Modal.Title>Placing order</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div>
                            Select Address: 
                            <select className="address-selector" onChange={this._addressChange} value={this.state.default_address.address_id}>
                                <option id="default" disabled="disabled" value="default">Select a category</option>
                                {addresses}
                            </select>
                        </div>
                        <div>
                            Select Time:
                            <select className="time-selector" >
                                {time_slots}
                            </select>
                        </div>
                        <div className="payment-section clearfix mt20">
                            <div><strong>Payment Method:</strong></div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_cash" value="cash" defaultChecked/>
                                <label htmlFor="payment_cash">Cash</label>
                            </div>
                            <div className="payment-options">
                                <input type="radio" name="payment-option" id="payment_credits" value="wallet"/>
                                <label htmlFor="payment_credits">Credits: ₹ {this.state.user.wallet_balance}</label>
                            </div>
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className="btn btn-success" onClick={this._placeOrder}>Place Order Now.</button>
                    </Modal.Footer>
                </Modal>
            );
    }
});

export default OrderModal; 
