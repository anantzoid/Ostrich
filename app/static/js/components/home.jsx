import React from 'react';
import Navbar from './navbar';
import Header from './header';
import Searchbar from './searchbar';
const homepage = React.createClass({
    render() {
        let panels = this.props.panel_data.map((panel) => {
            let books = panel.items.map((item) => {
                let img_link  = "https://d3i8lg6krdgeel.cloudfront.net/" + item.img_small;
                return (
                    <li className="book-li"><span className="book-span">
                        <a>
                            <img className="book-img" src={img_link} />
                        </a>
                    </span></li>
                    );
            });

            return ( <div>
                        <h4>{panel.name}</h4>
                        <div className="book-section">
                            <ul className="book-ul">{books}</ul>
                        </div>
                    </div>);
        }); 
        return (
            <div>
                <section className="header-section">
                    <Navbar user={this.props.user} />
                    <Header />
                </section>
                <Searchbar />
                <div className="container">
                <div className="row">
                {panels}
                </div>
                </div>
            </div>
            );
    }
});

export default homepage;

