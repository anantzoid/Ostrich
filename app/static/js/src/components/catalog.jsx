import React from 'react';
import Navbar from './navbar';
import SearchResults from './searchresults';
import Footer from './footer';

const Catalog = React.createClass({
    render() {
        return(
            <div id="catalog">
                <Navbar {...this.props} />
                <section className="catalog-section">
                    <div className="container-fluid">
                        {this.props.catalog.length ?
                            null
                            :
                            <SearchResults {...this.props}/>
                        } 
                    </div>
                </section>
                <Footer />
            </div>
            );
    }
});

module.exports = Catalog;
