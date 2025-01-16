import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import TimesheetForm from "./components/TimesheetForm";
import LoginForm from "./components/LoginForm"; // Import the existing LoginForm

const App = () => {
  const [accessToken, setAccessToken] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginForm, setShowLoginForm] = useState(false); // Track login form visibility
  const [showForm, setShowForm] = useState(false);

  // Handle login success
  const handleLoginSuccess = (token) => {
    setAccessToken(token);
    setIsLoggedIn(true);
    setShowLoginForm(false); // Close the login form after successful login
  };

  // Handle login failure
  const handleLoginFail = (errorMessage) => {
    alert(errorMessage);  // Show login failure message
  };

  // Handle logout functionality
  const handleLogout = () => {
    axios
      .post(
        "http://localhost:8000/api/logout/",
        {},
        {
          headers: {
            Authorization: `Bearer ${accessToken}`, // Send token as Bearer in headers
          },
        }
      )
      .then(() => {
        setAccessToken("");
        setIsLoggedIn(false);
        alert("Logged out successfully!");
      })
      .catch((error) => {
        alert("Logout failed: " + error.response.data.detail);
      });
  };

  // Toggle timesheet form visibility
  const handleFormToggle = () => {
    setShowForm((prev) => !prev);
  };

  // Toggle login form visibility
  const handleLoginFormToggle = () => {
    setShowLoginForm((prev) => !prev);
  };

  return (
    <div className="app-container">
      <nav className="navbar">
        <div className="navbar-logo">
          <img
            src="https://media.licdn.com/dms/image/v2/D5616AQH5c846_5rePQ/profile-displaybackgroundimage-shrink_200_800/profile-displaybackgroundimage-shrink_200_800/0/1708943021537?e=2147483647&v=beta&t=0NWv8L7Or4RkH3XBDLas4uKv8x__qM-m5OcJwlUk30o"
            alt="Logo"
          />
        </div>

        <div className="navbar-buttons">
          {!isLoggedIn ? (
            <button className="navbar-button" onClick={handleLoginFormToggle}>
              Login
            </button>
          ) : (
            <>
              <button className="navbar-button" onClick={handleLogout}>
                Logout
              </button>
              <button className="navbar-button" onClick={handleFormToggle}>
                {showForm ? "Close Form" : "Fill Timesheet"}
              </button>
            </>
          )}
        </div>
      </nav>

      <div className="content-container">
        {!isLoggedIn ? (
          <header className="landing-header">
            <h1>Welcome to the Timesheet Management Portal</h1>
            <p>Track your work efficiently and submit your timesheets seamlessly.</p>
          </header>
        ) : (
          <div className="form-container">
            {showForm && <TimesheetForm />}
          </div>
        )}
      </div>

      {/* Show login form in the center of the page */}
      {showLoginForm && (
        <div className="login-form-container">
          <LoginForm
            onLoginSuccess={handleLoginSuccess}   // Pass success callback
            onLoginFail={handleLoginFail}           // Pass fail callback
          />
        </div>
      )}
    </div>
  );
};

export default App;
