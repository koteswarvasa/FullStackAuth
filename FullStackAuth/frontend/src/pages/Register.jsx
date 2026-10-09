
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";

function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_nm: "",
    last_nm: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();
  

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const response = await apiRequest("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify(formData),
      });

    setError("");
    setSuccess("Registration successful! Redirecting to login...");

    setTimeout(() => {
    navigate("/login", { replace: true });
    }, 1500);

      setFormData({
        username: "",
        email: "",
        password: "",
        first_nm: "",
        last_nm: "",
      });
    } catch (err) {
      setError(err.message || "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h1>Create Account</h1>
        <p>Register for FullStackAuth</p>

        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}

        <label htmlFor="username">Username</label>
        <input
          id="username"
          name="username"
          type="text"
          value={formData.username}
          onChange={handleChange}
          minLength={3}
          maxLength={100}
          autoComplete="username"
          required
        />

        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          maxLength={255}
          autoComplete="email"
          required
        />

        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          value={formData.password}
          onChange={handleChange}
          minLength={8}
          maxLength={128}
          autoComplete="new-password"
          required
        />

        <label htmlFor="first_nm">First Name</label>
        <input
          id="first_nm"
          name="first_nm"
          type="text"
          value={formData.first_nm}
          onChange={handleChange}
          maxLength={100}
        />

        <label htmlFor="last_nm">Last Name</label>
        <input
          id="last_nm"
          name="last_nm"
          type="text"
          value={formData.last_nm}
          onChange={handleChange}
          maxLength={100}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Creating Account..." : "Register"}
        </button>

        <p>
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}

export default Register;
