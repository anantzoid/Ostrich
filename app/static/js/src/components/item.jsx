import React from 'react';
import Navbar from './navbar';
import OrderModal from './orderModal';
import Footer from './footer';
import gAuth from '../google_auth.js'; 

const Item = React.createClass({
    getInitialState() {
        return {'show_order_modal': false};
    },
    componentDidMount() {
        //fetch collection object
        //fetch similar items
    },
    startAuth() {
        gAuth().then(function(response) {});
    },
    _toggleOrderModal() {
        this.setState({'show_order_modal': !this.state.show_order_modal});
    },
    render() {
        let categories = this.props.item_data.categories.map((category, i) => {
            let key = 'category-'+category.category_id;
            let last_el = this.props.item_data.categories.length-1 !== i ? ', ': ''; 
            return <span className="category-tag" key={key}><a href={category.slug_url}>{category.category_name}</a>{last_el}</span>;
        });
       
        let ratings = Array.apply(null, Array(parseInt(this.props.item_data.ratings))).map((_, i) => {
            return <span className="glyphicon glyphicon-star" aria-hidden="true"></span>;
        });
        if (ratings.length < this.props.item_data.ratings) {
            ratings.push(<span className="glyphicon glyphicon-star star-half" aria-hidden="true"></span>);
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
                                        {this.props.item_data.author ? 
                                        <h4>by {this.props.item_data.author}</h4>
                                        : null}

                                        <div className="itemmeta-container mt20">
                                            <div className="item-ratings">
                                                {ratings}
                                            </div>
                                            <div className="item-num-ratings">
                                                <i>{this.props.item_data.num_ratings} ratings</i>
                                            </div>
                                            { categories.length ? 
                                                <div className="category-container clearfix pull-right">
                                                    {categories}
                                                </div>
                                            : null }
                                        </div>
                                        
                                        { this.props.item_data.summary ?
                                            <div className="summary mt20">
                                                {this.props.item_data.summary}
                                            </div>
                                        : null }
                                    </div>
                                </div>
                            </div>
                            <div className="col-lg-3">
                                <div className="order-info-container">
                                    <div className="clearfix">
                                        <div className="price-label">M.R.P:</div> 
                                        <div className="price-value">₹ {this.props.item_data.price}</div>
                                    </div>
                                    <div className="clearfix">
                                        <div className="price-label">Rental Amount:</div> 
                                        <div className="price-value">₹ {this.props.item_data.custom_price}</div>
                                    </div>
                                    <div className="clearfix">
                                        <div className="price-label">Rental Period:</div> 
                                        <div className="price-value">{this.props.item_data.custom_return_days ? this.props.item_data.custom_return_days: 21} days</div>
                                    </div>
                                    <div className="action-container">
                                        { this.props.user ? 
                                        <button className="btn btn-success order-now" onClick={this._toggleOrderModal}>Order Now</button>
                                        : <a href="#" onClick={this.startAuth}><img className="order-gauth mt20" src="/static/img/sign-in-with-google.png" /></a> }
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                   </div> 
                   <OrderModal show={this.state.show_order_modal} {...this.props} hide={this._toggleOrderModal}/>
                </section>
                <Footer />
            </div>
            );
    }
});

module.exports = Item;
/*
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
*/
