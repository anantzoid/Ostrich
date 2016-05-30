import React from 'react';

const SearchResults = React.createClass({
    getInitialState() {
        return { page: 1 };
    },
    render() {
        console.log(this.state.page*this.props.search_results.items.length, this.props.search_results.count);
        let results = this.props.search_results.items.map((book) => {
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
        let categories = this.props.categories.map((category) => {
            let key = 'category-'+category.category_id;
            return(
                <li className="catalog-sidebar-item" key={key}>
                    <a href="#">{category.category_name}</a>    
                </li>
                );
        });

        // TODO collections below items list
        // similar categories list
        return(
            <div className="row">
                <div className="col-lg-2">
                    <div>
                        <div className="catalog-sidebar-title">Popular Categories</div>
                        <ul>{categories}</ul>
                    </div>  
                    <div>
                        <div className="catalog-sidebar-title">Recent Searches</div>
                    </div>
                </div>
                <div className="col-lg-9 clearfix">
                    <ul className="clearfix">
                        {results}
                    </ul>
                    { this.state.page*this.props.search_results.items.length < this.props.search_results.count ? 
                        <button className="" onClick={this._}>Load More</button>
                    : null }
                </div>
            </div>
            );
    }
});

export default SearchResults;
