import React from 'react';

const SearchResults = React.createClass({
    render() {
        let results = this.props.search_results.items.map((book) => {
            return(
                <div className="catalog-book-container pull-left" key={book.item_id}>
                    <a href="#">
                        <div className="catalog-book-image-container">
                            <img className="catalog-book-image" src={book.img_small} />
                        </div>
                        <div>{book.item_name}</div>
                    </a>
                </div>
                );
        });
        // TODO collections below items list
        // similar categories list
        return(
            <div className="col-lg-9">
                {results}
            </div>
            );
    }
});

export default SearchResults;
