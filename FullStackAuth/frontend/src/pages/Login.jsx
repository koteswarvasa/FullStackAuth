
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";
import { useAuth } from "../context/AuthContext";
import "./css/Login.css";

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((previousData) => ({
      ...previousData,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (loading) return;

    setError("");
    setLoading(true);

    try {
      const response = await apiRequest("/api/v1/auth/login", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      if (!response?.access_token) {
        throw new Error("Access token was not returned.");
      }

      login(response.access_token);
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="login-page">
      <section className="login-shell">
        <aside className="login-brand">
          <Link to="/login" className="login-brand-logo">
            <span className="login-brand-mark">✦</span>
            <span>
              FullStack<span className="login-brand-accent">Auth</span>
            </span>
          </Link>

          <div className="login-brand-content">
            <span className="login-eyebrow">SECURE ACCESS</span>

            <h1>Your workspace. Your security.</h1>

            <p>
              Sign in to access your account, manage your profile,
              and continue where you left off.
            </p>

            <div className="login-illustration" aria-hidden="true">
              <div className="login-orbit login-orbit-one" />
              <div className="login-orbit login-orbit-two" />

              <div className="login-shield">
                <svg viewBox="0 0 100 100" fill="none">
                  <path
                    d="M50 8 82 21v25c0 22-13 37-32 46C31 83 18 68 18 46V21L50 8Z"
                    stroke="currentColor"
                    strokeWidth="5"
                    strokeLinejoin="round"
                  />
                  <rect
                    x="36"
                    y="43"
                    width="28"
                    height="23"
                    rx="5"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    d="M42 43v-7a8 8 0 0 1 16 0v7"
                    stroke="currentColor"
                    strokeWidth="4"
                    strokeLinecap="round"
                  />
                  <circle cx="50" cy="53" r="3" fill="currentColor" />
                </svg>
              </div>

              <span className="login-floating-dot dot-one" />
              <span className="login-floating-dot dot-two" />
            </div>

            <div className="login-benefits">
              <div className="login-benefit">
                <span className="login-benefit-icon">✓</span>
                <div>
                  <strong>Secure authentication</strong>
                  <p>Your account is protected by secure sign-in.</p>
                </div>
              </div>

              <div className="login-benefit">
                <span className="login-benefit-icon">◇</span>
                <div>
                  <strong>Session management</strong>
                  <p>Access your account with managed sessions.</p>
                </div>
              </div>

              <div className="login-benefit">
                <span className="login-benefit-icon">↗</span>
                <div>
                  <strong>Easy account recovery</strong>
                  <p>Reset your password if you lose access.</p>
                </div>
              </div>
            </div>
          </div>

          <p className="login-brand-footer">
            Secure access. Simple experience.
          </p>
        </aside>

        <section className="login-form-panel">
          <div className="login-form-inner">
            <div className="login-mobile-brand">
              FullStack<span>Auth</span>
            </div>

            <div className="login-heading">
              <span className="login-form-eyebrow">WELCOME BACK</span>
              <h2>Sign in to your account</h2>
              <p>Enter your credentials to continue.</p>
            </div>

            {error && (
              <div className="login-alert" role="alert">
                <span className="login-alert-icon">!</span>
                <p>{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="login-form">
              <label htmlFor="username">Username</label>

              <div className="login-input-wrap">
                <span className="login-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="8" r="4" />
                    <path d="M4 21v-2a8 8 0 0 1 16 0v2" />
                  </svg>
                </span>

                <input
                  id="username"
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Enter your username"
                  autoComplete="username"
                  maxLength={100}
                  required
                  disabled={loading}
                />
              </div>

              <div className="login-label-row">
                <label htmlFor="password">Password</label>
                <Link to="/forgot-password">
                  Forgot password?
                </Link>
              </div>

              <div className="login-input-wrap">
                <span className="login-input-icon" aria-hidden="true">
                  <svg viewBox="0 0 24 24" fill="none">
                    <rect
                      x="4"
                      y="10"
                      width="16"
                      height="11"
                      rx="2"
                    />
                    <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                    <path d="M12 14v3" />
                  </svg>
                </span>

                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  maxLength={128}
                  required
                  disabled={loading}
                />

                <button
                  type="button"
                  className="login-password-toggle"
                  onClick={() =>
                    setShowPassword((previous) => !previous)
                  }
                  aria-label={
                    showPassword ? "Hide password" : "Show password"
                  }
                  aria-pressed={showPassword}
                  disabled={loading}
                >
                  {showPassword ? (
                    <svg viewBox="0 0 24 24" fill="none">
                      <path d="M3 3l18 18" />
                      <path d="M10.6 10.6a2 2 0 0 0 2.8 2.8" />
                      <path d="M9.9 5.2A11 11 0 0 1 12 5c5 0 9 5 9 7a11 11 0 0 1-2.1 3.1" />
                      <path d="M6.2 6.2C3.7 7.7 2 10 2 12c0 2 4 7 10 7a10 10 0 0 0 4-.8" />
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" fill="none">
                      <path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z" />
                      <circle cx="12" cy="12" r="3" />
                    </svg>
                  )}
                </button>
              </div>

              <button
                className="login-submit"
                type="submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="login-spinner" />
                    Signing in...
                  </>
                ) : (
                  <>
                    Sign in to your account
                    <span aria-hidden="true">→</span>
                  </>
                )}
              </button>
            </form>

            <div className="login-register">
              <span>Don't have an account?</span>
              <Link to="/register">Create an account</Link>
            </div>

            <div className="login-security-note">
              <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
                <path d="M12 3 20 6v5c0 5-3 8-8 10-5-2-8-5-8-10V6l8-3Z" />
                <path d="m9 12 2 2 4-4" />
              </svg>
              <span>Your connection is protected.</span>
            </div>
          </div>
        </section>
      </section>
    </main>
  );
}

export default Login;
