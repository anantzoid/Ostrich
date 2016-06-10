import React from 'react';
import SearchBar from './searchbar';

const Banner = React.createClass({
    render() {
        return(<header>
                <div className="header-content">
                    <div className="header-content-inner">
                        <h1>Renting books has never been easier</h1>
                        <p>Search from a myraid of genres and collections, and get
                        the book of your choice delivered to your place.</p>

                        <div className="row">
                            <div className="col-lg-3"></div>
                            <SearchBar />                            
                        </div>
                    </div>
                </div>
            </header>
            );
    }
});

export default Banner;
