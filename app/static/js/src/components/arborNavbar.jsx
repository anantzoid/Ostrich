import React from 'react';

const ArborNavbar = React.createClass({
    getInitialState() {
        return {arbor_id: this.props.checkout_id};
    },
    componentWillReceiveProps(nextProps) {
        this.setState({arbor_id: nextProps.checkout_id});
    },
    setArborId(event) {
        this.setState({arbor_id: event.target.value});
    },
    checkout() {
        let arbor_id = $(".form-control").val();
        if (!arbor_id) {
            return;
        }
        
        $.ajax({
            url: this.props.host + 'arbor/checkout',
            type: 'POST',
            data: {
                user_id: this.props.user.user_id,
                arbor_id:  arbor_id
            },
            success: ((response) => {
                alert(response['message']);
                if (response['status'] == true) {
                    location.reload();
                } 
            })
        });
    },
    render() {
        return(
            <nav className="navbar navbar-default">
            <div className="container-fluid">
                <div className="navbar-header">
                    <a className="navbar-brand page-scroll" href="/">
                        <img className="navbar-logo pull-left" src={"https://s3-ap-southeast-1.amazonaws.com/ostrich-catalog/website/logo.png"} alt="Ostrich Logo" />
                        <div className="pull-left navbar-brand-name">Ostrich</div>
                    </a>
                </div>

                <div className="navbar-collapse text-left" id="bs-example-navbar-collapse-1">
                    <ul className="nav navbar-nav navbar-right">
                    </ul>
                 </div>
            </div>

            <div className="container-fluid sec-nav">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false" aria-controls="navbar">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                </div>

                <div className="navbar-collapse collapse text-left" id="bs-example-navbar-collapse-1">
                    <form className="navbar-form navbar-left" role="search">
                        <div className="form-group">
                            <input type="text" className="form-control" placeholder="Search" value={this.state.arbor_id} onChange={this.setArborId}/>
                        </div>
                        <button className="btn btn-default" onClick={this.checkout}>Submit</button>
                    </form>
                    <ul className="nav navbar-nav navbar-right">
                       { this.props.user !== null ?
                            <li><a href="#">{this.props.user.name}</a></li> 
                        : null }
                    </ul>
                 </div>
            </div>
        </nav>
        );
    }
});

module.exports = ArborNavbar;
