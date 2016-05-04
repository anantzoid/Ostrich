import React from 'react';
import Navbar from './navbar';
import SearchResults from './searchresults';
import Footer from './footer';

const Catalog = React.createClass({
    render() {
        console.log(this.props);
        return(
            <div id="catalog">
                <Navbar {...this.props} />
                <section className="catalog-section">
                    <div className="container">
                        <div className="row">
                            {this.props.catalog.length ?
                                null
                                :
                                <SearchResults search_results={this.props.search_results}/>
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
