import React, { useState, useEffect } from "react";
import "./TimesheetForm.css";

const TimesheetForm = () => {
  const [programs, setPrograms] = useState([]);
  const [teams, setTeams] = useState([]);
  const [formData, setFormData] = useState({
    name: "",
    ldap: "",
    lead: "",
    program: "",
    team: "",
    process: "",
    activity: "",
    time_in_mins: "",
    comment: "",
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/programs/")
      .then((response) => response.json())
      .then((data) => setPrograms(data))
      .catch((error) => console.error("Error fetching programs:", error));
  }, []);

  useEffect(() => {
    if (formData.program) {
      fetch(`http://127.0.0.1:8000/api/teams/${formData.program}/`)
        .then((response) => response.json())
        .then((data) => setTeams(data))
        .catch((error) => console.error("Error fetching teams:", error));
    } else {
      setTeams([]);
    }
  }, [formData.program]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://127.0.0.1:8000/api/timesheet/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to save timesheet data");
        }
        return response.json();
      })
      .then((data) => {
        alert("Timesheet data saved successfully!");
        console.log(data);
        setFormData({
          name: "",
          ldap: "",
          lead: "",
          program: "",
          team: "",
          process: "",
          activity: "",
          time_in_mins: "",
          comment: "",
        });
      })
      .catch((error) => {
        console.error("Error saving timesheet data:", error);
        alert("Failed to save data. Please try again.");
      });
  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Name:</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Enter your name"
          required
        />
      </div>
      <div className="form-group">
        <label>LDAP:</label>
        <input
          type="text"
          name="ldap"
          value={formData.ldap}
          onChange={handleChange}
          placeholder="Enter LDAP"
          required
        />
      </div>
      <div className="form-group">
        <label>Lead:</label>
        <input
          type="text"
          name="lead"
          value={formData.lead}
          onChange={handleChange}
          placeholder="Enter lead name"
          required
        />
      </div>
      <div className="form-group">
        <label>Program:</label>
        <select
          name="program"
          value={formData.program}
          onChange={handleChange}
          required
        >
          <option value="">Select a Program</option>
          {programs.map((program) => (
            <option key={program.program_id} value={program.program_id}>
              {program.program_name}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>Team:</label>
        <select
          name="team"
          value={formData.team}
          onChange={handleChange}
          required
          disabled={!formData.program || teams.length === 0}
        >
          <option value="">Select a Team</option>
          {teams.map((team) => (
            <option key={team.team_id} value={team.team_id}>
              {team.team_name}
            </option>
          ))}
        </select>
      </div>
      <div className="form-group">
        <label>Process:</label>
        <input
          type="text"
          name="process"
          value={formData.process}
          onChange={handleChange}
          placeholder="Enter process"
          required
        />
      </div>
      <div className="form-group">
        <label>Activity:</label>
        <input
          type="text"
          name="activity"
          value={formData.activity}
          onChange={handleChange}
          placeholder="Enter activity"
          required
        />
      </div>
      <div className="form-group">
        <label>Time (in minutes):</label>
        <input
          type="number"
          name="time_in_mins"
          value={formData.time_in_mins}
          onChange={handleChange}
          placeholder="Enter time in minutes"
          required
        />
      </div>
      <div className="form-group">
        <label>Comment:</label>
        <textarea
          name="comment"
          value={formData.comment}
          onChange={handleChange}
          placeholder="Enter comments"
          required
        ></textarea>
      </div>
      <button className="submit-button" type="submit">
        Submit
      </button>
    </form>
  );
};

export default TimesheetForm;
