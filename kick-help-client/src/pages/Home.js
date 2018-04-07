import React, { Component } from "react";

class Home extends Component {
  render() {
    return (
      <div className="form-parent">
        <form>
          <input type="url" name="name" className="question" id="nme" required autoComplete="off" />
          <label htmlFor="url"><span>Project URL</span></label>
          <input type="submit" value="Submit!" />
        </form>
      </div>
    );
  }
}

export default Home;
