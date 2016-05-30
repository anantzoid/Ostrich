import React from 'react';
import Navbar from './navbar';
import OrderModal from './orderModal';
//TODO use appModal included in navbar itself
import AppModal from './appModal';
import Footer from './footer';
import gAuth from '../google_auth.js'; 

const Item = React.createClass({
    getInitialState() {
        return {
            'show_order_modal': false,
            'show_app_modal': false
        };
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
    _toggleAppModal(title) {
        this.setState({
            'show_app_modal': !this.state.show_app_modal
        });
    },
    render() {
        let categories = this.props.item_data.categories.map((category, i) => {
            let key = 'category-'+category.category_id;
            let last_el = this.props.item_data.categories.length-1 !== i ? ', ': ''; 
            return <span className="category-tag" key={key}><a href={category.slug_url}>{category.category_name}</a>{last_el}</span>;
        });
      
        let ratings = null;
        if(this.props.item_data.ratings) { 
            ratings = Array.apply(null, Array(parseInt(this.props.item_data.ratings))).map((_, i) => {
                return <span className="glyphicon glyphicon-star" aria-hidden="true"></span>;
            });
            if (ratings.length < this.props.item_data.ratings) {
                ratings.push(<span className="glyphicon glyphicon-star star-half" aria-hidden="true"></span>);
            }
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

                                        <div className="itemmeta-container clearfix mt20">
                                            <div className="col-lg-5">
                                                <div className="item-ratings">
                                                    {ratings}
                                                </div>
                                                { ratings ? 
                                                <div className="item-num-ratings">
                                                    <i>{this.props.item_data.num_ratings} ratings</i>
                                                </div> : null }
                                            </div>
                                            { categories.length ? 
                                                <div className="col-lg-7">
                                                    <div className="category-container clearfix pull-right">
                                                        {categories}
                                                    </div>
                                                </div>
                                            : null }
                                        </div>
                                        
                                        <div className="summary mt20">
                                        { this.props.item_data.summary ?
                                            this.props.item_data.summary
                                        : <i className="summary-placeholder">
                                            No description given.    
                                        </i> }
                                        </div>
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
                                        <button className="btn btn-success order-now" onClick={this._toggleOrderModal}>Rent Now</button>
                                        : <a href="#" onClick={this.startAuth}><img className="order-gauth mt20" src="/static/img/sign-in-with-google.png" /></a> }
                                    </div>
                                </div>
                                
                            </div>
                        </div>
                   </div> 
                   <OrderModal show={this.state.show_order_modal} {...this.props} hide={this._toggleOrderModal} appModal={this._toggleAppModal}/>
                   <AppModal show={this.state.show_app_modal} hide={this._toggleAppModal} title="Order Placed Successfully" />
                </section>
                <Footer />
            </div>
            );
    }
});

module.exports = Item;

