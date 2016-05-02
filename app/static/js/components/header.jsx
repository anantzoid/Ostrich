import React from 'react';
const Banner = React.createClass({
    render() {
        return(<header>
                <div className="header-content">
                    <div className="header-content-inner">
                        <h1>Ostrich</h1>
                        <h3>Our Books | Your Bookself</h3>
                        <p>Discover and Rent Books in a few taps</p>

                        <div className="row">
                            <div className="col-lg-3"></div>
                            <div className="col-lg-6 search-elements">
                                <form onSubmit={this._onClick}>
                                    <div className="form-group has-feedback">
                                        <input className="search-input form-control" type="text" placeholder="What do you want to read today?"/>
                                        <i className="glyphicon glyphicon-search form-control-feedback"></i>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </header>
            );
    }
});

export default Banner;
