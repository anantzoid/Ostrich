import React from 'react';
import Navbar from './navbar';
import Header from './header';
const homepage = React.createClass({
    render() {
        return (
            <div>
                <Navbar />
                <Header />
            </div>
            );
    }
});

export default homepage;

