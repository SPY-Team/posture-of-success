import React, { Component } from "react";
import { Link } from "react-router-dom";


export default class extends Component {
  handleClick = () => {
    console.log(this.email, this.password);
    fetch('/api/login', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
       "email": this.email,
       "password": this.password
      })
    })
    .then(res => res.json())
    .then(json => {
      alert(json.valid?"성공":"실패");
    });
  }

  render() {
    return (
      <div className="signin-container">
        <form name="loginInfo" className="form-signin" autocomplte="off" action="/" method="post">
          <h1>성공의 자세 🪑</h1>
          <h3>Posture of Success</h3>
          <input type="email" className="form-control" placeholder="Email address" required="" autoFocus=""
            onChange={(e) => { this.email = e.target.value}}
          /><br/>
          <input type="password" id="inputPassword" className="form-control" placeholder="Password" required=""
            onChange={(e) => { this.password = e.target.value}}
          /><br/>
          <button className="button sign-in-button" type="button" onClick={this.handleClick}>Sign in</button>
          <Link to="/sign-up">
            <button className="button sign-up-button">Sign up</button>
          </Link>
        </form>
      </div>
    )
  }
}