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
                        <img className="navbar-logo pull-left" src={this.props.cdn+"logo.png"} alt="Ostrich Logo" />
                        <div className="pull-left navbar-brand-name">Ostrich</div>
                    </a>
                    <a className="navbar-brand navbar-brand-sec pull-right" href="/">
                        <img className="navbar-logo pull-left" src={this.props.cdn+"arbor/paypal.png"} alt="paypal Logo" />
                    </a>
                </div>
            </div>

            { this.props.user !== null ?
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
                                <input type="text" className="form-control" placeholder="Enter book_id " value={this.state.arbor_id} onChange={this.setArborId}/>
                            </div>
                            <button className="btn btn-success" onClick={this.checkout}>Checkout</button>
                        </form>
                        <ul className="nav navbar-nav navbar-right">
                                { this.props.user.is_admin ?
                                <li><a href="/paypal/admin">Admin</a></li> 
                                : null } 
                            <li><a href="#">My Orders</a></li> 
                            <li><a>{this.props.user.name}</a></li> 
                        </ul>
                    </div>
                </div>
            : null }
        </nav>
        );
    }
});

module.exports = ArborNavbar;
