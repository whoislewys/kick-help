import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./pages/Home";
import Data from "./pages/Data";

class Main extends Component {
<<<<<<< HEAD
  constructor(props) {
    super(props);
    this.state = {
      success: 0
    }

    this.queryAPI = this.queryAPI.bind(this);
    this.setData = this.setData.bind(this);
  }

  queryAPI(url) {
    fetch('https://kick-help-api.herokuapp.com/predict?url=' + url)
    .then(results => {
      return results.json();
    }).then(data => {
      this.setData(Math.round(data['success'] * 100));
    })
  }

  setData(success) {
    this.setState({success});
  }

  render() {
    const HomePage = (props) => {
      return (
        <Home
          submit={this.queryAPI}
          {...props}
        />
      );
    }

    const DataPage = (props) => {
      return (
        <Data
          success={this.state.success}
          {...props}
        />
      );
    }

    return (
      <HashRouter>
        <div className="content">
          <Route exact path="/" render={HomePage}/>
          <Route path="/data" render={DataPage}/>
=======
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
>>>>>>> 414037edfc163cc48fabd66e6fb287044411f842
        </div>
      </HashRouter>
    );
  }
}

export default Main;
