import React, { Component } from "react";

class Home extends Component {
  constructor() {
    super();
    this.state = {
      url: ''
    }

    this.handleURLChange = this.handleURLChange.bind(this);
    this.submitForm = this.submitForm.bind(this);
    this.validURL = this.validURL.bind(this);
  }

  handleURLChange(e) {
     this.setState({url: e.target.value});
  }

  validURL() {
    return true;
  }

  submitForm() {
    if(this.validURL()) {

    }
  }

  render() {
    return (
      <div className="form-parent">
        <form>
          <input type="url" name="name" className="question" id="nme" value={this.state.url} onChange={this.handleURLChange} required autoComplete="off" />
          <label htmlFor="url"><span>Project URL</span></label>
          <input type="button" value="Submit!" onClick={this.submitForm} />
        </form>
      </div>
    );
  }
}

export default Home;
