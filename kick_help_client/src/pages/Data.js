import React, { Component } from "react";
<<<<<<< HEAD
import CountUp from 'countup.js';
import Grid from './Grid';

class Data extends Component {
  constructor(props) {
    super(props);
    this.state = {
      countUp: null
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.success === 0 && nextProps.success !== 0) {
      this.state.countUp.update(nextProps.success);
    }
  }

  componentDidMount() {
    var options = {
      useEasing: true,
      useGrouping: true,
      separator: ',',
      decimal: '.',
      suffix: '%'
    };

    this.setState({countUp: new CountUp('perc', 0, this.props.success, 0, 4, options)});
  }

  map(num) {
    if(num <= 10) {
      return 1;
    } else if(num <= 50) {
      return 8.5;
    } else if(num <= 80) {
      return 9.5;
    } else {
      return 10;
    }
  }

  render() {
    return (
      <div>
        <h1 id="perc" className=""></h1>
        <div className="grid">
          <Grid success={this.props.success} />
        </div>
=======

class Data extends Component {
  render() {
    return (
      <div>
        
>>>>>>> 414037edfc163cc48fabd66e6fb287044411f842
      </div>
    );
  }
}

export default Data;
