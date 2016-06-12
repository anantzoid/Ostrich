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
        /*
        OrderUtils.fetchAreas().then((areas) => {
            this.setState({areas: areas});
        });
        */
    },
    componentDidMount() {
        let _ = this;
        $('.map-picker').locationpicker({
            location: {latitude: 12.933074, longitude: 77.6221414},
            radius: 0,
            enableAutocomplete: true,
            inputBinding: {
                locationNameInput: $('.area-picker')
            },
            onchanged: function() {
                _._setLocationDetails();
            }
        }); 
    },
    _setLocationDetails() {
        //NOTE Know bug: Need to move the marker before checking availability
        let location_details = $('.map-picker').locationpicker('map').location;
        this.state.new_address.latitude = location_details.latitude;
        this.state.new_address.longitude = location_details.longitude;
        this.state.new_address.description = location_details.addressComponents.addressLine1+', '+location_details.addressComponents.district;
        this.state.new_address.district = location_details.addressComponents.district;
        this.state.new_address.locality = location_details.formattedAddress;
        this.setState({new_address: this.state.new_address});
        this._checkAreaValidity();

    },
    _descriptionChange(event) {
        this.state.new_address.description = event.target.value;
        this.setState({new_address: this.state.new_address}); 
    },
    _checkAreaValidity() {
        if (this.state.new_address.locality.indexOf('Bengaluru') > -1) {
            OrderUtils.validateLocality(this.state.new_address.locality).then((response) => {
                this.state.new_address.is_valid = response.is_valid;
                this.state.new_address.delivery_msg = response.delivery_message;
                if (this.state.new_address.is_valid) {
                    // Formatting: capitalize initials
                    this.state.new_address.locality = response.validated_locality.replace(/\w\S*/g, ((txt) => {
                        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                    }));
                } else {
                    let local = this.state.new_address.locality;
                    let dis = this.state.new_address.district;
                    this.state.new_address.locality = local.slice(local.lastIndexOf(dis) + dis.length, local.indexOf('Bengaluru')).trim();
                    // Formatting: Removing trash chars
                    this.state.new_address.locality = this.state.new_address.locality.replace(/^\,+|\,+$/g, '').trim();
                }
                this.setState({new_address: this.state.new_address});
            }); 
        } else {
            let local = this.state.new_address.locality;
            let dis = this.state.new_address.district;
            this.state.new_address.locality = local.slice(local.lastIndexOf(dis) + dis.length);
            this.state.new_address.is_valid = 0;
            this.state.new_address.delivery_msg = 'Out of Delivery Area';
            this.setState({new_address: this.state.new_address});
        }
        console.log(this.state);
    },
    _areaChange(option) {
        /*
        for(let area in this.state.areas) {
            area = this.state.areas[area];
            if (area.area_id == option.value) {
                this.state.new_address['area_id'] = area.area_id;
                this.state.new_address['locality'] = area.name;
                this.setState({new_address: this.state.new_address});
                break;
            }
        }
        */
    },
    _saveAddress() {
        /* 
        if(!this.state.new_address.hasOwnProperty('area_id')) {
            this._renderError('area');
        }
        let description = $('.address-description').val();
        if (!description) {
            this._renderError('description');
        }
        let landmark = $('.address-landmark').val();
        */
        if(!this.state.new_address.description) {
            this._renderError('description');
        } else {
            OrderUtils.addAddress(this.state.new_address, this.props.user.user_id, this.props.toggle)
        }
    },
    render() {
        /*
        let areas = [];
        for(let area in this.state.areas) {
            areas.push({
                value: this.state.areas[area].area_id,
                label: area
            }); 
        }
        */
        return (
                <Modal show={this.props.show} onHide={this.props.hide}>
                    <Modal.Header closeButton>
                        <Modal.Title>Add New Address</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className="address-error-msg collapse"></div>
                        <div className="map-container">
                            <div><strong>Select Area:</strong></div>
                            <input type="text" className="area-picker"/>
                            <div className="map-picker"></div>
                        </div>
                        
                        {this.state.new_address.hasOwnProperty('is_valid') ?
                            <div>
                            <div className="mt20">
                                <div><input className="address-description" type="text" placeholder="Address Description..." value={this.state.new_address.description} onChange={this._descriptionChange} onFocus={this._removeError}/></div>
                            <div><input className="address-landmark" type="text" placeholder="Landmark..." onFocus={this._removeError}/></div>
                            </div>
                            <div className="mt20 locality clearfix">
                                <div className="pull-left locality-name">{this.state.new_address.locality}</div>
                                <div className="pull-right locality-valid">
                                {this.state.new_address.is_valid ? 
                                    <span className="glyphicon glyphicon-ok" aria-hidden="true"></span>
                                  : <span className="glyphicon glyphicon-ban-circle" aria-hidden="true"></span>
                                }
                                {this.state.new_address.delivery_msg}
                                </div>
                            </div>
                            {this.state.new_address.is_valid ? null : 
                                <div className="invalid-address-msg">
                                    Ostrich currently delivers in Central & South Bangalore. We'll inform you when we start serving your area.
                                </div>
                            }
                            </div>
                        : null }
           
 
                    </Modal.Body>
                    <Modal.Footer>
                        {this.props.user.address.length ?
                            <div className="pull-left">
                                <a href="#" onClick={this.props.toggle}>&lt; Back</a>
                            </div>
                        : null }
                        {this.state.new_address.hasOwnProperty('is_valid') ?
                            <button className="btn btn-success confirm-address" onClick={this._saveAddress}>Add Address</button>
                            : null }
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
/*
 *<Select
                            className="area-selector"
                            value={ this.state.new_address.hasOwnProperty('area_id') 
                                ? this.state.new_address.area_id : null}
                            options={areas}
                            onChange={this._areaChange}
                            clearable={false}
                            placeholder="Select Delivery Area..."
                            onFocus={this._removeError}
                        />
                        */
