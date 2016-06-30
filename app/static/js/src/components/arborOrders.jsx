import React from 'react';
import ArborNavbar from './arborNavbar';
import Footer from './footer';

const ArborOrders = React.createClass({

    getItemList(orders) {
        let elements = orders.map((book) => {
            return (
            <li className="arbor-book-li" key={book.arbor_id} id={book.arbor_id}>
                <div className="arbor-book-container clearfix">
                    <div className="arbor-book-image-container pull-left">
                        <img src={book.item.img_small} alt={book.item.item_name} />
                    </div>
                    <div>
                        <div className="arbor-book-name">{book.item.item_name}</div>
                        <div>{book.item.author}</div>
                    </div>
                    <div className="arbor-book-meta">
                    </div>
                </div>
            </li>
            );
        });
        return elements;
    },
    render() {
        let reading = this.getItemList(this.props.orders.reading);
        let history = this.getItemList(this.props.orders.history);

        return(
            <div className="arbor">
                <ArborNavbar {...this.props} />
                <section className="arbor-section">
                    <div className="container arbor-orders">
                        <div className="row">
                            <div className="clearfix">
                                <h3>Reading</h3>
                                <ul>{reading}</ul>
                            </div>
                            <div className="clearfix arbor-order-history">
                                <h3>Already Issued</h3>
                                <ul>{history}</ul>
                            </div>
                        </div>
                    </div>
                </section>
                <Footer {...this.props} />
            </div> 
 
            );
    }

});

module.exports = ArborOrders;
