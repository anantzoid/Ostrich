import React from 'react';
import Navbar from './navbar';
import Header from './header';
import Searchbar from './searchbar';
import Footer from './footer';

const Homepage = React.createClass({
    render() {
        let collections = this.props.collections.map((panel) => {
            let img_link = "https://d3i8lg6krdgeel.cloudfront.net/" + panel.image;
            return (
                <li className="collection-li"><span className="collections-span">
                    <a>
                        <img className="collection-img" src={img_link} />
                    </a>
                </span></li>
                );
        });
       return (
            <div>
                <section className="header-section">
                    <Navbar user={this.props.user} />
                    <Header />
                </section>
                <Searchbar />
                <section className="collection-section">
                    <div className="container">
                        <div className="row">
                            <div className="collection-section">
                                <ul className="collection-ul">{collections}</ul>
                            </div>
                        </div>
                    </div>
                </section>
                <Footer />
           </div>
            );
    }
});

// not compatible with React.createFactory
//export default homepage;
module.exports = Homepage;

