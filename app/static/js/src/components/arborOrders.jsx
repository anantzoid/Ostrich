import React from 'react';
import ArborNavbar from './arborNavbar';
import Footer from './footer';
import ItemUtils from '../utils/itemUtils';

const ArborOrders = React.createClass({

    returnBook(arbor_id, event) {
        event.preventDefault();
        $.ajax({
            url: this.props.host + 'arbor/return',
            type: 'POST',
            data: {
                arbor_id: arbor_id,
                user_id: this.props.user.user_id
            },
            success:((response) => {
                alert(response.message);
                location.reload();
            })
        });
    },
    getItemList(orders) {
        let elements = null;
        elements = orders.map((book, i) => {
            return (
            <li className="arbor-book-li" key={book.arbor_id+"-"+i} id={book.arbor_id}>
                <div className="arbor-book-container clearfix">
                    <div className="arbor-book-image-container pull-left">
                        <img src={book.item.img_small} alt={book.item.item_name} />
                    </div>
                    <div>
                        <div className="arbor-book-name">{book.item.item_name}</div>
                        <div>{book.item.author}</div>
                    </div>
                    <div className="arbor-book-meta">
                        <div>Issued on: {ItemUtils.stripTime(book.order_placed)}</div>
                        { book.order_returned ?
                          <div>Returned on: {ItemUtils.stripTime(book.order_returned)}</div>   
                        : <div> <a href="#" className="arbor-return" onClick={this.returnBook.bind(this, book.arbor_id)}>Return Now</a></div>
                        }
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
                        { !reading.length && !history.length ?
                            <div className="row"><h3>Nothing Ordered yet :(</h3></div>  
                            : 
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
                        }
                    </div>
                </section>
                <Footer {...this.props} />
            </div> 
 
            );
    }

});

module.exports = ArborOrders;
