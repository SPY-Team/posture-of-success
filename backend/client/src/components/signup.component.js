import React, { Component } from "react";
import { Link } from "react-router-dom";

export default class extends Component {
  constructor(props) {
    super(props);
    this.setState({ username: "", email: "", password: "" });
  }
  handleClick = () => {
    this.props.signup(this.state);
  }
  render() {
    return (
      <div className="signin-container">
        <div className="form-signin">
          <h1>성공의 자세 🪑</h1>
          <h3>Posture of Success</h3>
          <input type="text" id="inputUsername" className="form-control" placeholder="Username" required="" autoFocus=""
            onChange={(e) => { this.setState({ username: e.target.value }); }}
	  ></input><br></br>
          <input type="email" id="inputEmail" className="form-control" placeholder="Email address" required=""
            onChange={(e) => { this.state.email = e.target.value }}
          ></input><br></br>
          <input type="password" id="inputPassword" className="form-control" placeholder="Password" required=""
            onChange={(e) => { this.state.password = e.target.value }}
	  ></input><br></br>
          <button className="button primary-button" onClick={this.handleClick}>Submit</button>
          <Link to="sign-in">
            <button className="button secondary-button" type="submit">Back</button>
          </Link>
        </div>
      </div>
    )
  }
}
