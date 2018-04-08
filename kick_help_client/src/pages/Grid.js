import React, { Component } from 'react';

export default class Grid extends Component {
  constructor(props) {
    super(props);

    let arr = [];
    for(let i = 0; i < 100; i++) {
      arr.push(0);
    }

    this.state = {
      activations: arr.slice(),
      counter: 0
    }

    this.nullArray = arr.slice();
    this.animationStep = this.animationStep.bind(this);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.success != 0) {
      console.log("WILLRECIEVEPROPS!!!" + nextProps.success);
      this.setState({counter: nextProps.success}, this.animationStep);
    }
  }

  animationStep() {
    if(this.state.counter > 0) {
      setTimeout(() => {
        let arr = this.state.activations.slice();
        arr[(this.props.success - this.state.counter)] = 1;

        this.setState({activations: arr, counter: this.state.counter - 1}, this.animationStep);
      }, 2500/this.props.success);
    }
  }

  render() {
    let arr = [], n = Math.round(Math.sqrt(this.state.activations.length));
    let activs = this.state.activations.slice().reverse();

    for(let i = 0; i < n; i++) {
      arr.push(
        <Row activations={activs.splice(0, 10).reverse()} n={n} key={i}/>
      );
    }

    return arr;
  }
}

class Row extends Component {
  render() {
    let arr = [];

    for(let i = 0; i < this.props.n; i++) {
      arr.push(<Box active={this.props.activations[i]} key={i}/>);
    }

    return (
      <div className="row">
        { arr }
      </div>
    );
  }
}

const Box = ({ active }) => (
  <div className={active == 1 ? "element bounce active" : "element bounce"}></div>
);
