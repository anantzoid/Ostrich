import React from 'react';
import Navbar from './navbar';
import Header from './banner';
import Footer from './footer';

const Homepage = React.createClass({
    componentDidMount() {
        $('.collection-ul').slick({
            infinite: false,
            slidesToShow: 5,
            slidesToScroll: 1,
            prevArrow: '<a href="#" class="slick-left" onClick="event.preventDefault()"><span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span></a>',
            nextArrow: '<a href="#" class="slick-right" onClick="event.preventDefault()"><span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span></a>'
        })
        .on('afterChange', () => {
            let currentSlide = $('.collection-ul').slick('slickCurrentSlide');

            if (currentSlide == 0){
                $('.slick-left').hide();
                $('.slick-right').show();
            }
            else if (currentSlide == this.props.collections.length - 5){
                $('.slick-left').show();
                $('.slick-right').hide();
            } else {
                $('.slick-left').show();
                $('.slick-right').show();
            }

        });
        $('.slick-left').hide();

    },
    render() {
        let collections = this.props.collections.map((panel) => {
            return (
                <div className="collection-li" key={panel.collection_id}><span className="collections-span">
                    <a>
                        {panel.name}
                    </a>
                </span></div>
                );
        });
       return (
            <div id="home">
                <section className="header-section">
                    <Navbar {...this.props} />
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
                    </div>
                </section>
                <section className="howto-section">
                    <div className="container">
                        <div className="row howto-heading">
                            <div className="col-lg-12 text-center">
                                <h3>What's so great about Ostrich?</h3>
                            </div>
                        </div>
                        <div className="row">
                            <div className="col-lg-4">
                                <img src="/static/img/tmp/click_120.png" />
                            </div>
                            <div className="col-lg-4">
                                <img src="/static/img/tmp/door_120.png" />
                            </div>
                            <div className="col-lg-4">
                                <img src="/static/img/tmp/pay_r_120.png" />
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

