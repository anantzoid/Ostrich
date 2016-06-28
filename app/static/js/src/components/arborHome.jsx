import React from 'react';
import Navbar from './navbar';
import Footer from './footer';

const ArborHome = React.createClass({
        render() {
            return  (
                <div id="arborHome">
                    <Navbar {...this.props} />
                    <section className="arbor-login">
                        <div className="container">
                            <div className="row">
                            </div>
                        </div>
                    </section>
                    <Footer {...this.props} />
            </div> 
            );
        }
});

module.exports = ArborHome;
