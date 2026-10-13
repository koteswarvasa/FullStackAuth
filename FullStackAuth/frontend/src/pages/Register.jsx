
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";
import "./css/Register.css";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    first_nm: "",
    last_nm: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

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
    setSuccess("");

    if (formData.password.length < 8 ||
        formData.password.length > 128) {
      setError("Password must contain between 8 and 128 characters.");
      return;
    }

    setLoading(true);

    try {
      await apiRequest("/api/v1/auth/register", {
        method: "POST",
        body: JSON.stringify(formData),
      });

      setSuccess(
        "Account created successfully! Check your email for the welcome message."
      );

      setFormData({
        username: "",
        email: "",
        password: "",
        first_nm: "",
        last_nm: "",
      });

      // Redirect after showing the success message.
      setTimeout(() => {
        navigate("/login", { replace: true });
      }, 1800);
    } catch (err) {
      setError(err.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="register-page">
      <section className="register-shell">
        <aside className="register-brand">
          <Link to="/login" className="register-brand-logo">
            <span className="register-brand-mark">✦</span>
            <span>
              FullStack<span className="register-brand-accent">Auth</span>
            </span>
          </Link>

          <div className="register-brand-content">
            <span className="register-eyebrow">
              CREATE YOUR ACCOUNT
            </span>

            <h1>Start your secure journey.</h1>

            <p>
              Create your account to access your workspace with
              secure authentication and reliable session management.
            </p>

            <div className="register-illustration" aria-hidden="true">
              <div className="register-orbit register-orbit-one" />
              <div className="register-orbit register-orbit-two" />

              <div className="register-card-art">
                <div className="register-card-top">
                  <span>●</span>
                  <span>●</span>
                  <span>●</span>
                </div>
                <div className="register-avatar">+</div>
                <div className="register-art-line line-long" />
                <div className="register-art-line line-short" />
                <div className="register-art-check">✓</div>
              </div>
            </div>

            <div className="register-benefits">
              <div className="register-benefit">
                <span className="register-benefit-icon">✓</span>
                <div>
                  <strong>Quick registration</strong>
                  <p>Create your account in a few steps.</p>
                </div>
              </div>

              <div className="register-benefit">
                <span className="register-benefit-icon">◇</span>
                <div>
                  <strong>Email notifications</strong>
                  <p>Receive a confirmation after registration.</p>
                </div>
              </div>

              <div className="register-benefit">
                <span className="register-benefit-icon">⌑</span>
                <div>
                  <strong>Account security</strong>
                  <p>Your password is securely hashed by the backend.</p>
                </div>
              </div>
            </div>
          </div>

          <p className="register-brand-footer">
            Secure access. Simple experience.
          </p>
        </aside>

        <section className="register-form-panel">
          <div className="register-form-inner">
            <div className="register-mobile-brand">
              FullStack<span>Auth</span>
            </div>

            <div className="register-heading">
              <span className="register-form-eyebrow">
                GET STARTED
              </span>
              <h2>Create your account</h2>
              <p>
                Enter your details below to join FullStackAuth.
              </p>
            </div>

            {error && (
              <div className="register-alert register-alert-error"
                   role="alert">
                <span>!</span>
                <p>{error}</p>
              </div>
            )}

            {success && (
              <div className="register-alert register-alert-success"
                   role="status">
                <span>✓</span>
                <p>{success}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="register-form">
              <div className="register-name-grid">
                <div className="register-field">
                  <label htmlFor="first_nm">First name</label>
                  <input
                    id="first_nm"
                    name="first_nm"
                    type="text"
                    value={formData.first_nm}
                    onChange={handleChange}
                    placeholder="First name"
                    autoComplete="given-name"
                    maxLength={100}
                    disabled={loading}
                  />
                </div>

                <div className="register-field">
                  <label htmlFor="last_nm">Last name</label>
                  <input
                    id="last_nm"
                    name="last_nm"
                    type="text"
                    value={formData.last_nm}
                    onChange={handleChange}
                    placeholder="Last name"
                    autoComplete="family-name"
                    maxLength={100}
                    disabled={loading}
                  />
                </div>
              </div>

              <div className="register-field">
                <label htmlFor="username">Username <span>*</span></label>
                <input
                  id="username"
                  name="username"
                  type="text"
                  value={formData.username}
                  onChange={handleChange}
                  placeholder="Choose a username"
                  minLength={3}
                  maxLength={100}
                  autoComplete="username"
                  required
                  disabled={loading}
                />
                <small>Use at least 3 characters.</small>
              </div>

              <div className="register-field">
                <label htmlFor="email">Email address <span>*</span></label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="example@gmail.com"
                  maxLength={254}
                  autoComplete="email"
                  required
                  disabled={loading}
                />
              </div>

              <div className="register-field">
                <label htmlFor="password">Password <span>*</span></label>

                <div className="register-password-wrap">
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Create a strong password"
                    minLength={8}
                    maxLength={128}
                    autoComplete="new-password"
                    required
                    disabled={loading}
                  />

                  <button
                    type="button"
                    className="register-password-toggle"
                    onClick={() =>
                      setShowPassword((previous) => !previous)
                    }
                    aria-label={
                      showPassword ? "Hide password" : "Show password"
                    }
                    aria-pressed={showPassword}
                    disabled={loading}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <small>Password must contain 8–128 characters.</small>
              </div>

              <button
                type="submit"
                className="register-submit"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="register-spinner" />
                    Creating account...
                  </>
                ) : (
                  <>
                    Create account <span>→</span>
                  </>
                )}
              </button>
            </form>

            <div className="register-login-link">
              <span>Already have an account?</span>
              <Link to="/login">Sign in</Link>
            </div>

            <p className="register-security-note">
              <span>✓</span>
              Your password is never stored as plain text.
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}

export default Register;
