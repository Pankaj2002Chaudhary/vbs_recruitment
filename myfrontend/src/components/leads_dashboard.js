import React, { useState, useEffect } from "react";
import axios from "axios";
import { DataGrid } from "@mui/x-data-grid";
import { Box, Button, TextField, Typography, Modal, Select, MenuItem, FormControl, InputLabel } from "@mui/material";

const Dashboard = () => {
  const [programs, setPrograms] = useState([]);
  const [teams, setTeams] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [timesheets, setTimesheets] = useState([]);
  const [openModal, setOpenModal] = useState(false);
  const [newEmployee, setNewEmployee] = useState({
    employee_name: "",
    team: "",
  });

  useEffect(() => {
    // Fetch programs, teams, employees, and timesheets
    axios.get("/api/programs/").then((res) => setPrograms(res.data));
    axios.get("/api/teams/").then((res) => setTeams(res.data));
    axios.get("/api/employees/").then((res) => setEmployees(res.data));
    axios.get("/api/timesheets/").then((res) => setTimesheets(res.data));
  }, []);

  const handleInputChange = (e) => {
    setNewEmployee({ ...newEmployee, [e.target.name]: e.target.value });
  };

  const handleRegister = () => {
    axios
      .post("/api/employees/", newEmployee)
      .then((response) => {
        setEmployees([...employees, response.data]);
        setOpenModal(false);
        setNewEmployee({ employee_name: "", team: "" });
      })
      .catch((error) => console.error(error));
  };


  return (
    <Box p={4}>
      <Typography variant="h4" gutterBottom>
        Employee Dashboard
      </Typography>

      {/* Register New Employee */}
      <Button variant="contained" color="primary" onClick={() => setOpenModal(true)}>
        Register Employee
      </Button>

      {/* Modal */}
      <Modal open={openModal} onClose={() => setOpenModal(false)}>
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            boxShadow: 24,
            p: 4,
            borderRadius: 2,
          }}
        >
          <Typography variant="h6" gutterBottom>
            Register New Employee
          </Typography>
          <TextField
            fullWidth
            margin="normal"
            label="Employee Name"
            name="employee_name"
            value={newEmployee.employee_name}
            onChange={handleInputChange}
          />
          <FormControl fullWidth margin="normal">
            <InputLabel id="team-select-label">Team</InputLabel>
            <Select
              labelId="team-select-label"
              name="team"
              value={newEmployee.team}
              onChange={handleInputChange}
            >
              {teams.map((team) => (
                <MenuItem key={team.team_id} value={team.team_id}>
                  {team.team_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button variant="contained" color="primary" onClick={handleRegister} sx={{ mt: 2 }}>
            Register
          </Button>
        </Box>
      </Modal>

      {/* Timesheets Table */}
      <Box mt={4}>
        <DataGrid
          rows={timesheets}
          columns={[
            { field: "id", headerName: "ID", width: 90 },
            { field: "name", headerName: "Name", width: 150 },
            { field: "ldap", headerName: "LDAP", width: 150 },
            { field: "program", headerName: "Program", width: 150 },
            { field: "team", headerName: "Team", width: 150 },
            { field: "process", headerName: "Process", width: 150 },
            { field: "time_in_mins", headerName: "Time (mins)", width: 100 },
            { field: "comment", headerName: "Comment", width: 300 },
          ]}
          pageSize={5}
        />
      </Box>
    </Box>
  );
};

export default Dashboard;
