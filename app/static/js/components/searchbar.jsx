import React from 'react';
const SearchBar = React.createClass({
    _onClick(event) {
        event.preventDefault();
        //TODO send to flux action
        let query = $('.search-input').val();
        if (query) {
            window.location.href = window.location.origin+'/books?type=free&q='+query;
        }
    },
    render() {
        return(<section className="search-section">
                <div className="container">
                    <div className="row search-row">
                        <div className="col-lg-8 col-lg-offset-2 search-inner-container">
                            <div className="row">
                                <div className="col-lg-9 search-elements">
                                    <form onSubmit={this._onClick}>
                                        <input className="search-input" type="text" />
                                    </form>
                                </div>
                                <div className="col-lg-3 search-elements">
                                    <button className="btn btn-primary search-btn" onClick={this._onClick}>Search</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>);
    }
});

export default SearchBar;
