import React from "react";
import { Navbar, Nav, NavDropdown } from "react-bootstrap";
import * as api from "../api";
class Header extends React.Component {
  state = {
    teams: [],
    sprints: [],
    selected_team: this.props.team,
    selected_sprint: this.props.sprint
  };
  componentDidMount() {
    api.fetchTeams().then(teams => {
      this.setState({
        teams: teams.teams
      });
      api.fetchSprint(this.state.selected_team).then(sprints => {
        this.setState({
          sprints: sprints
        });
      });
    });
  }

  changeTeam(team){
    api.fetchSprint(team.team).then(sprints => {
      this.setState({
        sprints: sprints,
        selected_team: team.team,
        selected_sprint: sprints[0]
      });
      this.props.selectedSprint(sprints[0]);
    });
    this.props.selectedTeam(team.team);
  };
  changeSprint(sprint) {
    this.setState({
      selected_sprint: sprint.sprint
    });
    this.props.selectedSprint(sprint.sprint);
  }
  render() {
    return (
      <div>
        <Navbar>
          <Navbar.Brand href="" className="title">
            Retro
          </Navbar.Brand>
          <NavDropdown title={this.state.selected_team} id="basic-nav-dropdown">
            {this.state.teams.map(team => (
              <NavDropdown.Item
                href="#"
                onClick={this.changeTeam.bind(this, { team })}
              >
                {team}
              </NavDropdown.Item>
            ))}
          </NavDropdown>
          <NavDropdown
            title={this.state.selected_sprint}
            id="basic-nav-dropdown"
          >
            {this.state.sprints.map(sprint => (
              <NavDropdown.Item
                href="#"
                onClick={this.changeSprint.bind(this, { sprint })}
              >
                {sprint}
              </NavDropdown.Item>
            ))}
          </NavDropdown>
        </Navbar>
      </div>
    );
  }
}

export default Header;
