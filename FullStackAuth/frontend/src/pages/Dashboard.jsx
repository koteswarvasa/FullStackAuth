
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import { apiRequest } from "../services/api";

function Dashboard() {
  const { accessToken, logout, updateAccessToken } = useAuth();
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [loggingOut, setLoggingOut] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadProfile() {
      setLoading(true);
      setError("");

      try {
        const profile = await apiRequest(
          "/api/v1/users/me",
          { accessToken },
          { updateAccessToken, logout }
        );

        if (!cancelled) {
          setUser(profile);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message || "Unable to load profile.");
          logout();
          navigate("/login", { replace: true });
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (!accessToken) {
      navigate("/login", { replace: true });
      return;
    }

    loadProfile();

    return () => {
      cancelled = true;
    };
  }, [accessToken, updateAccessToken, logout, navigate]);

  async function handleLogout() {
    if (loggingOut) return;

    setLoggingOut(true);
    setError("");

    try {
      await apiRequest("/api/v1/auth/logout", {
        method: "POST",
        accessToken,
      });

      logout();
      navigate("/login", { replace: true });
    } catch (err) {
      setError(`Logout failed: ${err.message}. Please retry.`);
    } finally {
      setLoggingOut(false);
    }
  }

  if (loading) {
    return <p>Loading your profile...</p>;
  }

  if (!user) {
    return (
      <div style={{ padding: "30px" }}>
        <p className="error-message">
          {error || "User profile is unavailable."}
        </p>

        <button
          onClick={() => navigate("/login", { replace: true })}
        >
          Back to Login
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Welcome, {user.first_nm || user.username}!</h1>

      <h2>Your Profile</h2>

      <p>
        <strong>User ID:</strong> {user.user_id}
      </p>

      <p>
        <strong>Username:</strong> {user.username}
      </p>

      <p>
        <strong>Email:</strong> {user.email}
      </p>

      <p>
        <strong>Account active:</strong>{" "}
        {user.is_active ? "Yes" : "No"}
      </p>

      {error && <p className="error-message">{error}</p>}

      <button onClick={handleLogout} disabled={loggingOut}>
        {loggingOut ? "Logging out..." : "Logout"}
      </button>
    </div>
  );
}

export default Dashboard;
