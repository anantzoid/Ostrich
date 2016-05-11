import React from 'react';
import Navbar from './navbar';
import Footer from './footer';

const Catalog = React.createClass({
    render() {

        let categories = this.props.categories.map((category) => {
            let key = 'category-'+category.category_id;
            return(
                <li className="catalog-sidebar-item" key={key}>
                    <a href={category.slug_url}>{category.category_name}</a>    
                </li>
                );
        });

        let results = [];
        if(this.props.search_results.items.length) {
            results = this.props.search_results.items.map((book) => {
                let key = 'book-'+book.item_id;
                return(
                    <li className="catalog-book-container text-center" key={key}>
                        <a href={book.item_url}>
                            <img className="catalog-book-image" src={book.img_small} />
                            <div className="catalog-book-info">{book.item_name}</div>
                        </a>
                    </li>
                    );
            });
        }
        return(
            <div id="catalog">
                <Navbar {...this.props} />
                <section className="catalog-section">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-lg-2">
                                <div className="catalog-sidebar">
                                    <div className="catalog-sidebar-title">Popular Categories</div>
                                    <ul>{categories}</ul>
                                </div>  
                            </div>
                            {this.props.catalog.length ?
                                null
                                :
                                <div className="col-lg-9">
                                    <div className="search-result-title">
                                        Showing results for: <span>{this.props.query}</span>
                                    </div>
                                    <ul>
                                        {results}
                                    </ul>
                                </div>
                            }
                        </div>

                         
                    </div>
                </section>
                <Footer />
            </div>
            );
    }
});

module.exports = Catalog;
