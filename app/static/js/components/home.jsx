import React from 'react';
import Navbar from './navbar';
import Header from './header';
import Footer from './footer';

const Homepage = React.createClass({
    componentDidMount() {
        $('.collection-ul').slick({
            infinite: true,
            slidesToShow: 5,
            slidesToScroll: 1
        });
    },
    render() {
        let collections = this.props.collections.map((panel) => {
            let img_link = "https://d3i8lg6krdgeel.cloudfront.net/" + panel.image;
            return (
                <div className="collection-li" key={panel.collection_id}><span className="collections-span">
                    <a>
                        <img className="collection-img" src={img_link} />
                    </a>
                </span></div>
                );
        });
       return (
            <div>
                <section className="header-section">
                    <Navbar user={this.props.user} />
                    <Header />
                </section>
                <section className="collection-section">
                    <div className="container">
                        <div className="row"><div className="col-lg-12 text-center">
                            <h3 className="collection-heading">Don't know what to read?</h3>
                            <h4 className="collection-subheading">Browse through our curated collection</h4>
                        </div></div>
                        <div className="row">
                        <div className="col-lg-12 collection-container">
                            <div className="collection-ul">{collections}</div>
                        </div></div>
                        <div className="row">
                            <div className="col-lg-12">
                                <h3>What's so great about Ostrich?</h3>
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

