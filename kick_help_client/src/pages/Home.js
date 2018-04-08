import React, { Component } from "react";

class Home extends Component {
  constructor(props) {
    super(props);
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
      this.props.submit('https://www.kickstarter.com/projects/' + this.state.url);
      // this.props.submit(Math.random());
      this.props.history.push('/data')
    }
  }

  render() {
    return (
      <div className="form-parent">
        <form onSubmit={this.submitForm}>
          <div className="url-input">
            <input
              className="url-input"
              name="url-input"
              id="url-input"
              type="text"
              value={this.state.url}
              onChange={this.handleURLChange}
              required
              autoComplete="off"
              autoCorrect="off"
              autoCapitalize="off"
              spellCheck="false" />
            <label htmlFor="url-input"><span className="url-text">https://kickstarter.com/projects/</span></label>
            <input type="submit" style={{display: 'none'}}/>
          </div>
        </form>
      </div>
    );
  }
}

export default Home;
