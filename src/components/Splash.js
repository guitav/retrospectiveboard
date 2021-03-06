import React from "react";
import Header from "./Header";
import TeamBoard from "./TeamBoard";
import Popup from "./Popup";
import * as api from "../api";
import { Form, Row, Col, Button, Collapse, Dropdown, Card, Jumbotron } from "react-bootstrap";

class Splash extends React.Component {
  state = {
    teams: this.props.teams,
    sprints: ["0"],
    team: "Select a Team",
    sprint: "Select a Sprint",
    open: false
  };


  changeTeam(team) {
    fetch("/fetch/sprint/values/"+team.team)
    .then(res => res.json()) //returning a promise To extract the JSON body content from the response
    .then(resJson => {
      this.setState({
        sprints: resJson,
        team: team.team,
        sprint: resJson[0]
      });
    })
    .catch(error => {
      console.error(error);
    });
  }
  changeSprint(sprint) {
    this.setState({
      sprint: sprint.sprint
    });
  }
  handleSubmit(event) {
    api
      .createTeam(this.state.team, this.state.sprint)
      .then(resp => this.props.selectedSprint(this.state.team, this.state.sprint));
      this.props.selectedSprint(this.state.team, this.state.sprint);
  }
  handleChange(event) {
    this.setState({ [event.target.name]: event.target.value });
  }
  handleChoose() {
    this.props.selectedSprint(this.state.team, this.state.sprint);
  }
  goTo() {
    if (!isNaN(this.state.sprint)) {
      return (
        <Col md={{ span: 6, offset: 3 }}>
          <Button onClick={this.handleChoose.bind(this)} className="splashbutton">
            Go To {this.state.team} Board for Sprint {this.state.sprint}
          </Button>
        </Col>
      );
    }
  }
  render() {
    return (
      <div className="Splash">
        <div className="backgroundImage">
          <Jumbotron className="jumbo">
            <h1>Retro</h1>
          </Jumbotron>
          <Row>
            <Col md={{ span: 6, offset: 3 }}>
              <Dropdown>
                <Dropdown.Toggle  id="dropdown-basic">
                  Select a Team
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {this.state.teams.map(team => (
                    <Dropdown.Item
                      onClick={this.changeTeam.bind(this, { team })}
                    className="splashbutton">
                      {team}
                    </Dropdown.Item>
                  ))}
                </Dropdown.Menu>
              </Dropdown>
              <Dropdown>
                <Dropdown.Toggle  id="dropdown-basic">
                  Select a Sprint
                </Dropdown.Toggle>
                <Dropdown.Menu>
                  {this.state.sprints.map(sprint => (
                    <Dropdown.Item
                      onClick={this.changeSprint.bind(this, { sprint })}
                    >
                      {sprint}
                    </Dropdown.Item>
                  ))}
                </Dropdown.Menu>
              </Dropdown>
            </Col>
          </Row>
          <Row>
            <Col md={{ span: 6, offset: 3 }} className="splashbutton">
              <Button
                onClick={() => this.setState({ open: !this.state.open })}
                aria-controls="example-collapse-text"
                aria-expanded={this.state.open}
                className="splashbutton"
              >
                Create a New Board
              </Button>
              <Collapse in={this.state.open}>
                <div id="example-collapse-text">
                  <Form onSubmit={this.handleSubmit.bind(this)}>
                    <Form.Control
                      type="text"
                      name="team"
                      placeholder="Enter Team Name"
                      onChange={this.handleChange.bind(this)}
                    />

                    <Form.Control
                      type="number"
                      name="sprint"
                      placeholder="Enter Sprint Number"
                      onChange={this.handleChange.bind(this)}
                    />
                    <Form.Control
                      type="submit"
                      sprintvalue="sprint"
                      value="Submit"
                    />
                  </Form>
                </div>
              </Collapse>
              <Jumbotron className="goto">
                <Row>{this.goTo()}</Row>
              </Jumbotron>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default Splash;
