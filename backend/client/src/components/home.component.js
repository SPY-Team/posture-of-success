import React, { Component } from "react";
import { LineChart, XAxis, Tooltip, CartesianGrid, Line, ResponsiveContainer } from "recharts";

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
      email: this.props.email,
      username: "",
      score: 0,
      duration: 0,
      week_score: 0,
      week_duration: 0,
      score_rank: 0,
      leaderboard
    };
  }

  componentDidMount() {
    fetch('/api/get_data', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email: this.props.token })
    })
    .then(res => res.json())
    .then(json => {
      this.setState(prevState => ({...prevState, ...json}));
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
            <div className="score"> {this.state.score}점 </div>
          </div>
          <div className="card">
            <table>
              <tr>
                <th>순위</th>
                <td>{this.state.score_rank}위</td>
              </tr>
              <tr>
                <th>총 사용시간</th>
                <td>{this.state.duration}시간</td>
              </tr>
              <tr>
                <th>주간 점수</th>
                <td>{this.state.week_score}점</td>
              </tr>
            </table>
          </div>
        </div>
	<div className="card">
	  <ResponsiveContainer width={700} height="80%">
	    <LineChart width={500} height={500}
              data={[
	        { name: "what", uv: 300 },
	        { name: "what", uv: 300 },
	        { name: "what", uv: 300 },
	        { name: "what", uv: 300 },
	        { name: "what", uv: 300 },
	      ]}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <XAxis dataKey="name" />
              <Tooltip />
              <CartesianGrid stroke="#f5f5f5" />
              <Line type="monotone" dataKey="uv" stroke="#ff7300" yAxisId={0} />
            </LineChart>
	  </ResponsiveContainer>
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
