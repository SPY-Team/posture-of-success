import React, { useState, useEffect } from 'react';
import './App.css';

import { BrowserRouter as Router, Switch, Route, Redirect } from "react-router-dom";
import { withCookies, useCookies } from "react-cookie";
import AuthRoute from './AuthRoute';

import SignIn from "./components/signin.component";
import SignUp from "./components/signup.component";
import Home from "./components/home.component";

function App() {

  const [ token, setToken ] = useState(null);
  const [ cookies, setCookie, removeCookie ] = useCookies(['user']);

  const auth = token !== null;

  const signin = ({ email, password }) => {
    fetch('/api/signin', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    })
    .then(res => {
      if (!res.ok) res.text().then(text => alert(text));
      else { 
        res.json()
        .then(json => {
          setCookie('user', json);
          setToken(json)
        });
      }
    });
  }

  const signup = ({ username, email, password }) => {
    fetch('/api/signup', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ username, email, password })
    })
    .then(res => {
      if (!res.ok) res.text().then(text => alert(text));
      else { 
        res.json()
        .then(json => {
          alert("done");
        });
      }
    });
  };

  const signout = () => { setToken(null); removeCookie('user') }

  useEffect(() => {
    if (cookies.user && cookies.user !== 'undefined') setToken(cookies.user);
  }, [ cookies ]);

  return (<Router>
    <div className="App">
      <div className="auth-wrapper">
        <div className="auth-inner">
          <Switch>
            <Redirect exact path='/' to='/home'/>
            <Route path='/sign-in' render={() => <SignIn token={token} signin={signin}/>} />
            <Route path="/sign-up" render={() => <SignUp signup={signup}/>} />
            <AuthRoute token={token} path='/home' render={() => <Home token={token} signout={signout}/>} />
          </Switch>
        </div>
      </div>
    </div></Router>
  );
}

export default App;
