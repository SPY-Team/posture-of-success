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

  const login = ({ email, password }) => {
    fetch('/api/login', {
      method: 'post',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .catch((err) => console.error())
    .then(json => {
      setCookie('user', json);
      setToken(json)
    });
  };
  const logout = () => { setToken(null); removeCookie('user') }

  useEffect(() => {
    if (cookies.user && cookies.user !== 'undefined') setToken(cookies.user);
  }, [ cookies ]);

  return (<Router>
    <div className="App">
      <div className="auth-wrapper">
        <div className="auth-inner">
          <Switch>
            <Redirect exact path='/' to='/home'/>
            <Route path='/sign-in' render={() => <SignIn token={token} login={login}/>} />
            <Route path="/sign-up" component={SignUp} />
            <AuthRoute token={token} path='/home' render={() => <Home token={token} logout={logout}/>} />
          </Switch>
        </div>
      </div>
    </div></Router>
  );
}

export default App;