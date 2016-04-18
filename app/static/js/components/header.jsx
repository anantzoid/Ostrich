import React from 'react';
const Banner = React.createClass({
    render() {
        return(<header>
                <div className="header-content">
                    <div className="header-content-inner">
                        <h1>Ostrich</h1>
                        <hr className="light" />
                        <h3>Our Books | Your Bookself</h3>
                        <hr className="light" />
                        <p>Discover and Rent Books in a few taps</p>
                    </div>
                </div>
            </header>
            );
    }
});

export default Banner;
