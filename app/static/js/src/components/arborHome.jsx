import React from 'react';
import ArborNavbar from './arborNavbar';
import Footer from './footer';
import ItemUtils from '../utils/itemUtils.js';

const ArborHome = React.createClass({
        getInitialState() {
            let books = this.props.books;
            for (let _ in books) {
                books[_]['options'] = false;
            }
            return {books: books, checkout_id: ""};
        },
        showOptions(flag, event) {
            if (!flag) {
                for (let _ in this.state.books) {
                    this.state.books[_]['options'] = false;
                }
            } else {
                if (event.target.id == "") { return; }
                for (let _ in this.state.books) {
                    if (this.state.books[_]['arbor_id'] == event.target.id ) {
                        this.state.books[_]['options'] = flag;
                    }
                }
            }
            this.setState({books: this.state.books});
        },
        selectBook(arbor_id) {
            this.setState({checkout_id: arbor_id}); 
        },
        render() {
            let books = this.state.books.map((book) => {
                let categories = ItemUtils.getCategories(book.item.categories);
                let ratings = ItemUtils.getRatings(book.item.ratings);

                return (
                       <li className="arbor-book-li" key={book.arbor_id} id={book.arbor_id} onMouseEnter={this.showOptions.bind(this, true)} onMouseLeave={this.showOptions.bind(this, false)} >
                        <div className="arbor-book-container clearfix">
                            <div className="arbor-book-image-container pull-left">
                                <img src={book.item.img_small} alt={book.item.item_name} />
                            </div>
                            <div>
                                <div className="arbor-book-name">{book.item.item_name}</div>
                                <div>{book.item.author}</div>
                            </div>
                            <div className="arbor-book-meta">
                                <div>{ratings}</div>
                                <div>{categories}</div>
                            </div>
                        </div>
                        { book.options ?
                            <div className="arbor-book-options-container">
                                <div className="arbor-book-options">
                                    <button className="btn btn-success" onClick={this.selectBook.bind(this, book.arbor_id)}>Checkout</button>
                                </div>
                            </div>  
                        : null }
                      </li>
                    );
            });
            return  (
                <div className="arbor">
                    <ArborNavbar {...this.props} checkout_id={this.state.checkout_id}/>
                    <section className="arbor-section">
                        <div className="container-fluid">
                            <div className="row">
                                <ul>{books}</ul>
                            </div>
                        </div>
                    </section>
                    <Footer {...this.props} />
            </div> 
            );
        }
});

module.exports = ArborHome;
