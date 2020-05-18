import React, { Component } from "react";
import { Link, Redirect, useLocation } from "react-router-dom";
import "../styles/signin.css";


export default class extends Component {
  constructor(props) {
    super(props);
    this.state = { email: "", password: "" };
  }
  handleClick = () => {
    this.props.login(this.state);
  }
  render() {
    const from = useLocation.from || { pathname: "/home" };
    if (this.props.token) return <Redirect to={from} />

    return (
      <div className="signin-container">
        <div className="form-signin">
          <h1>성공의 자세 🪑</h1>
          <h3>Posture of Success</h3>
          <input type="email" className="form-control" placeholder="Email address" required="" autoFocus=""
            onChange={(e) => { this.state.email = e.target.value }}
          /><br/>
          <input type="password" id="inputPassword" className="form-control" placeholder="Password" required=""
            onChange={ (e) => { this.state.password = e.target.value; } }
            onKeyDown={ (e) => { if ( e.keyCode ===13 ) this.handleClick(); } }
          /><br/>
          <button className="button primary-button" type="button" onClick={this.handleClick}>Sign in</button>
          <Link to="/sign-up">
            <button className="button secondary-button">Sign up</button>
          </Link>
        </div>
      </div>
    )
  }
}