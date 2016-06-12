import React from 'react';
import Navbar from './navbar';
import Footer from './footer';
import CatalogUtils from '../utils/catalogUtils';

const Catalog = React.createClass({
    _renderListElements(items) {
        let item_list = null;
        if (items.length) {
            item_list = items.map((book) => {
                let key = 'book-'+book.item_id;
                return (
                    <li className="catalog-book-container text-center" key={key}>
                            <a href={book.item_url}>
                                <img className="catalog-book-image" src={book.img_small} alt={book.item_name} />
                                <div className="catalog-book-info">{book.item_name}</div>
                            </a>
                        </li>
                    );
            }); 
        }
        return item_list;
    },
    _loadMore() {
        CatalogUtils.loadMore(this.state.page+1).then((response) => {
            this.setState({
                page: this.state.page + 1,
                items: this.state.items.concat(response.items)});
        }, () => {
            console.log('error');  
        }); 
    },
    getInitialState() {
        let state = {is_search:  this.props.search_results.hasOwnProperty('items')};
        if (state.is_search) {
            state.page =  this.props.page_num;
            state.items = this.props.search_results.items;
        }
        return state; 
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

        let results = null;

        if(!this.state.is_search) {
            results = this.props.catalog.map((list) => {
                let key = 'collection-'+list.collection_id; 
                return(
                        <div className="catalog-element clearfix" key={key}>
                            <h3>{list.name}</h3>
                            <ul>{this._renderListElements(list.items)}</ul>
                        </div>
                        ); 
            });
        } else {
            results = this._renderListElements(this.state.items);
        }

        return(
            <div id="catalog">
                <Navbar {...this.props} />
                <section className="catalog-section">
                    <div className="container-fluid">
                        <div className="row">
                            <div className="col-lg-2 col-sm-3 sidebar-col">
                                <div className="catalog-sidebar">
                                    <div className="catalog-sidebar-title">Popular Categories</div>
                                    <ul>{categories}</ul>
                                </div>  
                            </div>
                            {!this.state.is_search ?
                                <div className="col-lg-10 col-sm-9">
                                    {results}
                                </div>
                                :
                                <div className="col-lg-9 col-sm-9">
                                    <div className="search-result-title mt20">
                                        Showing results for: <span className="query-display">{this.props.query}</span>
                                    </div>
                                    <ul className="clearfix">
                                        {results}
                                    </ul>
                                    { this.state.items.length < this.props.search_results.total ? 
                                        <button className="btn load-more" onClick={this._loadMore}>Load More</button>
                                    : null }
                                </div>
                            }
                        </div>

                         
                    </div>
                </section>
                <Footer {...this.props} />
            </div>
            );
    }
});

module.exports = Catalog;
