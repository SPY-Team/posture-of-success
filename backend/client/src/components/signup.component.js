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
      <div className="center">
        <div className="card">
          <h1>성공의 자세 🪑</h1>
          <h3>Posture of Success</h3>
          <input type="text" placeholder="Username" required="" autoFocus=""
            onChange={(e) => { this.setState({ username: e.target.value }); }}
          ></input><br></br>
          <input type="email" placeholder="Email address" required=""
            onChange={(e) => { this.setState({ email: e.target.value }); }}
          ></input><br></br>
          <input type="password" placeholder="Password (평문으로 저장되니 사용하지 않는 비밀번호를 입력해주세요)" required=""
            onChange={(e) => { this.setState({password: e.target.value }); }}
          ></input><br></br>
          <div className="button-container">
            <button className="button primary-button" onClick={this.handleClick}>Submit</button>
            <Link to="signin">
              <button className="button secondary-button" type="submit">Back</button>
            </Link>
          </div>
        </div>
      </div>
    )
  }
}
