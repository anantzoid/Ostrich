import React from 'react';
const Banner = React.createClass({
    render() {
        return(<section className="search-section">
                <div className="container">
                    <div className="row search-row">
                        <div className="col-lg-8 col-lg-offset-2 search-inner-container">
                            <div className="row search-action-row">
                                <div className="col-lg-9">
                                    <input className="search-input" type="text" />
                                </div>
                                <div className="col-lg-3">
                                    <button className="btn btn-primary search-btn">Search</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>);
    }
});

export default Banner;
