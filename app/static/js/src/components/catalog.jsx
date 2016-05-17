import React from 'react';
import Navbar from './navbar';
import Footer from './footer';

const Catalog = React.createClass({
    _renderListElements(items) {
        let item_list = null;
        if (items.length) {
            item_list = items.map((book) => {
                let key = 'book-'+book.item_id;
                return (
                    <li className="catalog-book-container text-center" key={key}>
                            <a href={book.item_url}>
                                <img className="catalog-book-image" src={book.img_small} />
                                <div className="catalog-book-info">{book.item_name}</div>
                            </a>
                        </li>
                    );
            }); 
        }
        return item_list;
    },
    render() {
        let categories = this.props.categories.map((category) => {
            let key = 'category-'+category.category_id;
            return(
                <li key={key}>
                    <a className="catalog-sidebar-item" href={category.slug_url}>{category.category_name}</a>    
                </li>
                );
        });

        let catalog = null;
        if(this.props.catalog.length) {
            catalog = this.props.catalog.map((list) => {
            return(
                    <div className="catalog-element clearfix">
                        <h3>{list.name}</h3>
                        <ul>{this._renderListElements(list.items)}</ul>
                    </div>
                  ); 
            });
        }

        let results = null;
        if(this.props.search_results.hasOwnProperty('items') && this.props.search_results.items.length) {
            results = this._renderListElements(this.props.search_results.items);
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
                                <div className="col-lg-9">
                                    {catalog}
                                </div>
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
