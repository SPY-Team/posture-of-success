import React from "react"
import { Route, Redirect } from "react-router-dom"

function AuthRoute({ token, component: Component, render, ...rest }) {
  return (
    <Route
      {...rest}
      render={(props) =>
        token ? (
          render ? (
            render(props)
          ) : (
            <Component {...props} />
          )
        ) : (
          <Redirect to={{ pathname: "/signin", state: { from: props.location } }}/>
        )
      }
    />
  )
}

export default AuthRoute
