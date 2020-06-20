import React, { Component } from "react";
import moment from "moment";
import { ScatterChart, XAxis, YAxis, Tooltip, Legend, Scatter, ResponsiveContainer } from "recharts";

export default class extends Component {
  constructor(props) {
    super(props);
    this.state = { 
      email: this.props.email,
      username: "",
      score: 0,
      duration: 0,
      week_score: 0,
      week_duration: 0,
      score_rank: 0,
      graph_data: 0,
      leaderboard: [],
    };
  }

  fetchData(token) {
    fetch('/api/get_data', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email: token })
    })
    .then(res => res.json())
    .then(json => {
      this.setState(prevState => ({ ...prevState, ...json }));
    });
  }

  fetchGraphData(token) {
    fetch('/api/get_graph_data', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email: this.props.token })
    })
    .then(res => res.json())
    .then(json => {
      this.setState(json);
    });
  }

  fetchRivalGraphData(email) {
    fetch('/api/get_graph_data', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email })
    })
    .then(res => res.json())
    .then(json => {
      this.setState(prevState => ({ ...prevState, rival_graph_data: json.graph_data }));
      console.log(this.state);
    });
  };

 fetchLeaderBoard(token) {
    fetch('/api/get_leaderboard', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email: token })
    })
    .then(res => res.json())
    .then(json => {
      json.leaderboard.sort((a, b) => a.score_rank - b.score_rank);
      this.setState(json);
    });
  }

  componentDidMount() {
    this.fetchData(this.props.token);
    this.fetchGraphData(this.props.token);
    this.fetchLeaderBoard(this.props.token);

    setInterval(() => { this.fetchData(this.props.token); }, 1000);
    setInterval(() => { this.fetchGraphData(this.props.token); }, 5000);
    setInterval(() => { this.fetchLeaderBoard(this.props.token); }, 5000);
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
            <div className="score"> {Math.floor(this.state.score)}점 </div>
          </div>
          <div className="card">
            <table>
              <tr>
                <th>순위</th>
                <td>{this.state.score_rank}위</td>
              </tr>
              <tr>
                <th>총 사용시간</th>
                <td>{this.state.duration}</td>
              </tr>
              <tr>
                <th>주간 점수</th>
                <td>{Math.floor(this.state.week_score)}점</td>
              </tr>
            </table>
          </div>
        </div>
        <div className="card">
          <ResponsiveContainer width="100%" height={300}>
            <ScatterChart 
              width={500} 
              height={500}
              margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
            >
              <XAxis
                dataKey = 'receive_time'
                domain = {['auto', 'auto']}
                name = 'Time'
                tickFormatter = {(unixTime) => moment(unixTime).format('HH:mm Do')}
                type = 'number'
              />
              <YAxis dataKey = 'score' name = 'Score' />
              <Tooltip />
              <Legend />
              <Scatter
                data = {this.state.graph_data}
                line = {{ stroke: '#353772' }}
                shape = {() => null}
                fill = "#353772"
                lineJointType = 'monotoneX'
                name = 'Values'
              />
            </ScatterChart>
          </ResponsiveContainer>
        </div>
        <div className="card">
          <h2>리더보드</h2>
          <table className="leaderboard" cellSpacing="0" cellPadding="0"> 
            <thead>
              <tr>
                <th>순위</th>
                <th>이름</th>
                <th>점수</th>
              </tr>
            </thead>
            <tbody>
              { this.state.leaderboard.map((e, i) => 
                <tr key={i} onClick={() => { this.fetchRivalGraphData(e.email); }}>
                  <td id="ranking">{i+1}</td>
                  <td id="nickname">{e.username}</td>
                  <td id="score">{Math.floor(e.score)}</td>
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
