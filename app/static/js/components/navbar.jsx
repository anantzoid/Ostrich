import React from 'react';
const Navbar = React.createClass({
    render() {
        return(
        <nav className="navbar navbar-default">
        <div className="container-fluid">
            <div className="navbar-header">
                <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span className="sr-only">Toggle navigation</span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                    <span className="icon-bar"></span>
                </button>
                <a className="navbar-brand page-scroll" href="#page-top">Ostrich</a>
            </div>

            <div className="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul className="nav navbar-nav navbar-right">
                    <li className="">
                        <a className="page-scroll" href="#about">About</a>
                    </li>
                    <li className="">
                        { this.props.user === null ?
                            <div>
                                <button id="googleAuth">Sign in with Google</button>
                            </div>:<div>
                                <div>{this.props.user_data.name}</div>
                            </div>
                        }
                    </li>
               </ul>
            </div>
        </div>
        </nav>
        );
    }
});

export default Navbar;
