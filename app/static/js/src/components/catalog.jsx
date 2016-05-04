import React from 'react';
import Navbar from './navbar';
import Footer from './footer';

const Catalog = React.createClass({
    render() {
        return(
            <div>
                <Navbar user={this.props.user} />
                <Footer />
            </div>
            );
    }
});

module.exports = Catalog;
