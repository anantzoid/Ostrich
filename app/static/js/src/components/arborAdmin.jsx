import React from 'react';
import ArborNavbar from './arborNavbar';
import Footer from './footer';

const ArborAdmin = React.createClass({
    capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    },
    stripTime(ts) {
        return ts.split(' ')[0];
    },
    render() {
        let items = this.props.items.map((item, i) => {
            return (
                    <tr key={'inv-'+i}><td>{item.arbor_id}</td>
                    <td>{item.item_name}</td>
                    <td>{this.capitalizeFirstLetter(item.owner)}</td>
                    <td>{item.date_added}</td>
                    <td>{item.condition}</td>
                    { item.in_stock ?
                        <td>In Stock</td>
                    : <td>{item.name} - {this.stripTime(item.order_placed)}</td>
                    }
                    </tr>
                );

        });
        return (
            <div className="arbor">
                <ArborNavbar {...this.props}/>
                <section className="arbor-section">
                    <div className="container">
                        <div className="row">
                        <table className="table table-striped table-bordered">
                            <thead>
                                <tr>
                                    <th>Book Id</th>
                                    <th>Book Name</th>
                                    <th>Owner</th>
                                    <th>Date Added</th>
                                    <th>Condition</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>{items}</tbody>
                        </table> 
             
                        </div>
                    </div>
                </section>
                <Footer {...this.props} />
           </div> 
            );
    }
});

module.exports = ArborAdmin;
