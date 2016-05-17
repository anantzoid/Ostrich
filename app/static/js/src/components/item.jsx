import React from 'react';
import Navbar from './navbar';
import Footer from './footer';
import gAuth from '../google_auth.js'; 

const Item = React.createClass({
    startAuth() {
        gAuth().then(function(response) {
            //TODO Fetching user action box - add address, credits etc.
        });
    },
    _placeOrder() {
        let pay_option = $('input[name=payment-option]:checked').val();
        if (typeof pay_option == "undefined") {
            alert("Please select payment option");
        }
        let order_data = {
        
        };
        $.ajax({
            type: 'POST',
            url: '/order',
            data: order_data
        });
    },
    render() {
        let categories = this.props.item_data.categories.map((genre) => {
            return <span>{genre}</span>;
        });

        let addresses = null;
        if (this.props.user) {
            addresses = this.props.user.addresses.map((address) => {
                  
            });
        }

        return(
            <div id="itempage">
                <Navbar {...this.props} />
                <section className="itempage-section">
                    <div className="container">
                        <div className="row">
                            <div className="col-lg-9 item-container">
                                <div className="row">
                                    <div className="col-lg-3 img-container">
                                        <img src={this.props.item_data.img_small} />
                                    </div> 
                                    <div className="col-lg-9 iteminfo-container">
                                        <h2>{this.props.item_data.item_name}</h2>
                                        <h4>{this.props.item_data.author}</h4>

                                        <div className="itemmeta-container">
                                            <div className="item-ratings">
                                                Ratings: {this.props.item_data.ratings}
                                            </div>
                                            <div className="item-num-ratings">
                                                No. Ratings: {this.props.item_data.num_ratings}
                                            </div>
                                            <div className="item-num-reviews">
                                                No. Reviews: {this.props.item_data.num_reviews}
                                            </div>
                                        </div>
                                        { categories.length ? 
                                            <div className="category-container">
                                                Categories: {categories}
                                            </div>
                                        : null }
                                        { this.props.item_data.summary ?
                                            <div className="summary">
                                                {this.props.item_data.summary}
                                            </div>
                                        : null }
                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-3">
                                <div className="order-info-container">
                                    <div>
                                        M.R.P: ₹ {this.props.item_data.price}
                                    </div>
                                    <div>
                                        Rental At: ₹ {this.props.item_data.custom_price} 
                                    </div>
                                    <div>
                                        for: {this.props.item_data.custom_return_days} days 
                                    </div>
                                </div>
                                <div className="order-confirm-container">
                                    {this.props.user ? 
                                        <div>
                                            <div>
                                               Select Address: 
                                            </div>
                                            <select id="category_id" className="category-picker" multiple onChange={this._onChange}>
                                                <option id="default" disabled="disabled" value="default">Select address</option>
                                                {addresses}
                                            </select>
                                            <div>Payment Method:</div>
                                            <div className="payment-options">
                                                <input type="radio" name="payment-option" id="payment_cash" value="cash"/>
                                                <label htmlFor="payment_cash">Cash</label>
                                            </div>
                                            <div className="payment-options">
                                                <input type="radio" name="payment-option" id="payment_credits" value="credits"/>
                                                <label htmlFor="payment_credits">Credits: ₹ {this.props.user.wallet_balance}</label>
                                            </div>

                                            <button className="btn btn-success order-now" onClick={this._placeOrder}>Order Now</button>
                                        </div>
                                    : <a href="#" onClick={this.startAuth}>Sign in with Google</a> }
            
                                </div>
                            </div>
                        </div>
                   </div> 
                </section>
                <Footer />
            </div>
            );
    }
});

module.exports = Item;

