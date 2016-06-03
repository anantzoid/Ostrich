import React from 'react';
const SearchBar = React.createClass({
    getInitialState() {
        return {xs: false};
    },
    componentDidMount() {
        this.setState({xs:Math.max(document.documentElement.clientWidth, window.innerWidth || 0) <= 768});
    },
    _onClick(event) {
        event.preventDefault();
        let query = $('.search-input').val();
        window.location.href = window.location.origin+'/books?type=free&q='+query;
    },
    _showFilters() {
        $('.sidebar-col').show();
    },
    render() {
        return(<div className="col-lg-6 search-elements">
                <form className="search-form" onSubmit={this._onClick}>
                    <div className="form-group has-feedback">
                        <input type="text" className="search-input form-control" placeholder="What do you want to read today?" defaultValue={this.props.query} />
                        <i className="glyphicon glyphicon-search form-control-feedback" onClick={this._onClick}></i>
                    </div>
                </form>
                { this.state.xs && this.props.hasOwnProperty('page') && this.props.page == 'catalog' ?
                <a href="#" onClick={this._showFilters}><span className="glyphicon glyphicon-filter" aria-hidden="true"></span></a>
                : null }
            </div>);
    }
});

export default SearchBar;
