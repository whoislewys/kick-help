import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./pages/Home";
import Transition from "./pages/Transition";
import Data from "./pages/Data";

class Main extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <div className="content">
            <Route exact path="/" component={Home}/>
            <Route path="/loading" component={Transition}/>
            <Route path="/data" component={Data}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}

export default Main;
