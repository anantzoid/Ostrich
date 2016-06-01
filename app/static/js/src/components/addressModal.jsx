import React from 'react';
import { Modal } from 'react-bootstrap';
import Select from 'react-select';
import OrderUtils from '../utils/orderUtils';

const AddressModal = React.createClass({
    getInitialState() {
        return { 
            areas: [],
            new_address: {} };
    },
    componentWillMount() {
        OrderUtils.fetchAreas().then((areas) => {
            this.setState({areas: areas});
        });
    },
    _areaChange(option) {
        for(let area in this.state.areas) {
            area = this.state.areas[area];
            if (area.area_id == option.value) {
                this.state.new_address['area_id'] = area.area_id;
                this.state.new_address['locality'] = area.name;
                this.setState({new_address: this.state.new_address});
                break;
            }
        }
    },
    _saveAddress() {
        if(!this.state.new_address.hasOwnProperty('area_id')) {
            this._renderError('area');
        }
        let description = $('.address-description').val();
        if (!description) {
            this._renderError('description');
        }
        let landmark = $('.address-landmark').val();
        
        OrderUtils.addAddress({
            locality: this.state.new_address.locality, 
            description: description, 
            landmark: landmark, 
            is_valid: 1,
            delivery_message: 'Delivery Available'},
            this.props.toggle);
    },
    render() {
        let areas = [];
        for(let area in this.state.areas) {
            areas.push({
                value: this.state.areas[area].area_id,
                label: area
            }); 
        }
        return (
                <Modal show={this.props.show} onHide={this.props.hide}>
                    <Modal.Header closeButton>
                        <Modal.Title>Add New Address</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="address-error-msg collapse"></div>
                        <Select
                            className="area-selector"
                            value={ this.state.new_address.hasOwnProperty('area_id') 
                                ? this.state.new_address.area_id : null}
                            options={areas}
                            onChange={this._areaChange}
                            clearable={false}
                            placeholder="Select Delivery Area..."
                            onFocus={this._removeError}
                        />
                        <div className="mt20">
                            <div><strong>Address:</strong></div>
                            <div><input className="address-description" type="text" placeholder="1st Floor, House 450, 1st Main Rd., Koramangala 8th Block" onFocus={this._removeError}/></div>
                        </div>
                        <div className="mt20">
                            <div><strong>Landmark:</strong></div>
                            <div><input className="address-landmark" type="text" placeholder="Near CCD" onFocus={this._removeError}/></div>
                        </div>
           
 
                    </Modal.Body>
                    <Modal.Footer>
                        <div className="pull-left">
                            <a href="#" onClick={this.props.toggle}>&lt; Back</a>
                        </div>
                        <button className="btn btn-success confirm-address" onClick={this._saveAddress}>Add Address</button>
                    </Modal.Footer>
                </Modal>
            
            );
    },
    _renderError(type) {
        switch(type) {
            case 'area':
                $('.area-selector').first().addClass('error');
                break;
            case 'description':
                $('.address-description').addClass('error');
                break;
        }
    },
    _removeError() {
        $('.error').removeClass('error'); 
        $('.address-error-msg').slideUp('slow');
    },
});

export default AddressModal;

