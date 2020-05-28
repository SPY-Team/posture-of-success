import React, { Component } from "react";
import { Link, Redirect, useLocation } from "react-router-dom";

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = { email: "", password: "" };
  }
  handleClick = () => {
    this.props.signin(this.state);
  }
  render() {
    const from = useLocation.from || { pathname: "/home" };
    if (this.props.token) return <Redirect to={from} />;

    return (
      <div className="center">
        <div className="card">
          <h1>성공의 자세 🪑</h1>
          <h3>Posture of Success</h3>
          <input type="email" placeholder="Email address" required="" autoFocus=""
            onChange={(e) => { this.setState({ email: e.target.value }); }}
          /><br/>
          <input type="password" placeholder="Password" required=""
            onChange={(e) => { this.setState({ password: e.target.value }); }}
            onKeyDown={ (e) => { if ( e.keyCode ===13 ) this.handleClick(); } }
          /><br/>
          <div className="button-container">
            <button className="button primary-button" type="button" onClick={this.handleClick}>Sign in</button>
            <Link to="/signup">
              <button className="button secondary-button">Sign up</button>
            </Link>
          </div>
        </div>
      </div>
    )
  }
}
