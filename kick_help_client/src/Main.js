import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./pages/Home";
import Data from "./pages/Data";

class Main extends Component {
  constructor() {
    super();
    this.state = {
      data: {}
    }
  }

  queryAPI(url) {
    fetch('https://kick-help-api.herokuapp.com/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url
      })
    }).then(results => {
      return results.json();
    }).then(data => {
      this.setState({data});
    })
  }

  render() {
    return (
      <HashRouter>
        <div className="content">
          <Route exact path="/" component={Home} submit={this.queryAPI}/>
          <Route path="/data" component={Data} data={this.state.data}/>
        </div>
      </HashRouter>
    );
  }
}

export default Main;
