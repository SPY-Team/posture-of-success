import React, { Component } from "react";
import "../styles/signin.css";

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = { email: "", data: [] };
  }

  componentDidMount() {
    fetch('/api/data', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ token: this.props.token })
    })
    .then(res => res.json())
    .catch((err) => console.error())
    .then(json => {
      this.setState(json);
    });
  }

  render() {
    return (
      <div className="signin-container">
        <div className="form-signin">
          <h1>Hello, {this.state.email}!</h1>
          <p>Your data is {this.state.data}</p>
          <button className="button primary-button" onClick={this.props.signout}> logout </button>
        </div>
      </div>
    )
  }
}
