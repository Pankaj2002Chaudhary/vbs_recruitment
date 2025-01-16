// src/components/LoginForm.js

import React, { useState } from "react";
import axios from "axios";

const LoginForm = ({ onLoginSuccess, onLoginFail }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = () => {
    axios
      .post("http://localhost:8000/api/login/", { username, password })
      .then((response) => {
        // Trigger parent callback on success
        onLoginSuccess(response.data.access_token);
      })
      .catch((error) => {
        // Trigger parent callback on failure
        onLoginFail(error.response.data.detail);
      });
  };

  return (
    <div className="login-form">
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default LoginForm;
