import React, { useState, useEffect } from 'react';
import './App.css';

import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import { useCookies } from "react-cookie";
import AuthRoute from './AuthRoute';
import { Helmet } from "react-helmet";

import SignIn from "./components/signin.component";
import SignUp from "./components/signup.component";
import Home from "./components/home.component";

function App() {

  const [ token, setToken ] = useState(null);
  const [ cookies, setCookie, removeCookie ] = useCookies(['token']);

  const signin = ({ email, password }) => {
    fetch('/api/signin', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    })
    .then(res => {
      res.json()
      .then(json => {
	if ( json.success ) {
	  setCookie('token', email);
          setToken(email)
	} else alert("아이디와 비밀번호를 확인해주세요.");
      });
    });
  }

  const signup = ({ username, email, password }) => {
    fetch('/api/signup', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ username, email, password })
    })
    .then(res => {
      res.json().then(json => {
	if ( json.success ) {
          if (alert("성공적으로 회원가입 되었습니다.")) return <Redirect to='/signin'/>;
        } else {
	  alert("이미 가입된 이메일입니다.");
	}
      });
    });
  };

  const signout = () => { setToken(null); removeCookie('token') }

  useEffect(() => {
    if (cookies.token && cookies.token !== 'undefined') setToken(cookies.token);
  }, [ cookies ]);

  return (<Router>
    <div className="App">
      <Helmet>
	<title>Posture of Success</title>
      </Helmet>
      <Switch>
        <Redirect exact path='/' to='/home'/>
        <Route path='/signin' render={() => <SignIn token={token} signin={signin}/>} />
        <Route path='/signup' render={() => <SignUp signup={signup}/>} />
        <AuthRoute token={token} path='/home' render={() => <Home token={token} signout={signout}/>} />
      </Switch>
    </div></Router>
  );
}

export default App;
