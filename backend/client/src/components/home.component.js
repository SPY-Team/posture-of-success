import React, { Component } from "react";

export default class extends Component {
  constructor(props) {
    super(props);
    const leaderboard = [
      {
        nickname: "성시철",
        score: 3000,
      },
      {
        nickname: "박건",
        score: 2000,
      },
      {
        nickname: "이희준",
        score: 1000,
      },
    ]
    const my_data = { score: 100, total_duration: 10, weekly_score: 10, ranking: 30 };
    this.state = { 
      email: "guest@posture.success", 
      username: "guest", 
      leaderboard: leaderboard ,
      my_data: my_data
    };
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
      <div className="home-container">
        <h1>성공의 자세 🪑</h1>
        <div className="card">
          <h3>안녕하세요, {this.state.username}님</h3>
        </div>
        <div className="score-container">
          <div className="card">
            <h2>나의 점수</h2>
            <div className="score"> {this.state.my_data.score}점 </div>
          </div>
          <div className="card">
            <table>
              <tr>
                <th>순위</th>
                <td>{this.state.my_data.ranking}위</td>
              </tr>
              <tr>
                <th>총 사용시간</th>
                <td>{this.state.my_data.total_duration}시간</td>
              </tr>
              <tr>
                <th>주간 점수</th>
                <td>{this.state.my_data.weekly_score}점</td>
              </tr>
            </table>
          </div>
        </div>
        <div className="card">
          <h2>리더보드</h2>
          <table cellSpacing="0" cellPadding="0"> 
            <thead>
              <tr>
                <th>순위</th>
                <th>이름</th>
                <th>점수</th>
              </tr>
            </thead>
            <tbody>
              { this.state.leaderboard.map((e, i) => 
                <tr key={i}>
                  <td id="ranking">{i+1}</td>
                  <td id="nickname">{e.nickname}</td>
                  <td id="score">{e.score}</td>
                </tr>
              ) }
            </tbody>
          </table>
        </div>
        <div className="button-container">
          <button className="button secondary-button" onClick={this.props.signout}> logout </button>
        </div>
      </div>
    )
  }
}
