
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  requestPasswordReset,
  resetPassword,
} from "../services/api";
import "./css/ForgotPassword.css";

export default function ForgotPassword() {
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function handleRequestOtp(event) {
    event.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);

    try {
      await requestPasswordReset(email.trim());
      setStep(2);
      setMessage(
        "If the account is eligible, a verification email will be sent."
      );
    } catch (err) {
      setError(
        err.message || "Unable to request verification code."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleResetPassword(event) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!/^\d{6}$/.test(otp)) {
      setError("Please enter a valid six-digit verification code.");
      return;
    }

    if (newPassword.length < 8 || newPassword.length > 128) {
      setError("Password must contain between 8 and 128 characters.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setError("Your passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await resetPassword(
        email.trim(),
        otp,
        newPassword,
        confirmPassword
      );

      setMessage("Password reset successfully. Redirecting to login...");

      // Clear sensitive form values after success.
      setOtp("");
      setNewPassword("");
      setConfirmPassword("");

      setTimeout(() => {
        navigate("/login", { replace: true });
      }, 1200);
    } catch (err) {
      setError(err.message || "Unable to reset your password.");
    } finally {
      setLoading(false);
    }
  }

  function changeEmail() {
    setStep(1);
    setOtp("");
    setNewPassword("");
    setConfirmPassword("");
    setError("");
    setMessage("");
  }

  return (
    <main className="forgot-page">
      <section className="forgot-shell">
        <aside className="forgot-brand">
          <Link to="/login" className="brand-logo">
            <span className="brand-icon">✦</span>
            <span>
              FullStack<span className="brand-accent">Auth</span>
            </span>
          </Link>

          <div className="brand-content">
            <span className="brand-eyebrow">
              ACCOUNT RECOVERY
            </span>

            <h1>Reset your password.</h1>

            <p>
              Don't worry. We'll help you securely regain access
              to your account in just a few simple steps.
            </p>

            <div className="brand-illustration" aria-hidden="true">
              <div className="illustration-orbit orbit-one" />
              <div className="illustration-orbit orbit-two" />
              <div className="illustration-envelope">
                <span>✉</span>
                <span className="illustration-lock">⌑</span>
              </div>
            </div>

            <div className="brand-benefits">
              <div className="benefit-item">
                <span className="benefit-icon">✓</span>
                <div>
                  <strong>Secure verification</strong>
                  <p>Verify ownership using your email.</p>
                </div>
              </div>

              <div className="benefit-item">
                <span className="benefit-icon">◇</span>
                <div>
                  <strong>Your account stays protected</strong>
                  <p>Use a verification code to reset access.</p>
                </div>
              </div>

              <div className="benefit-item">
                <span className="benefit-icon">↗</span>
                <div>
                  <strong>Back to your account</strong>
                  <p>Return to login when you're finished.</p>
                </div>
              </div>
            </div>
          </div>

          <p className="brand-footer">
            Secure access. Simple recovery.
          </p>
        </aside>

        <section className="forgot-form-panel">
          <div className="form-inner">
            <div className="mobile-brand">
              FullStack<span>Auth</span>
            </div>

            <div className="form-heading">
              <span className="form-kicker">
                {step === 1 ? "STEP 01 OF 02" : "STEP 02 OF 02"}
              </span>

              <h2>
                {step === 1 ? "Forgot password?" : "Create a new password"}
              </h2>

              <p>
                {step === 1
                  ? "Enter your registered email and we'll send you a verification code."
                  : "Enter the code sent to your email and choose a new password."}
              </p>
            </div>

            <div
              className="step-progress"
              aria-label={`Step ${step} of 2`}
            >
              <div className={`progress-step ${step >= 1 ? "active" : ""}`}>
                <span className="step-number">
                  {step === 2 ? "✓" : "1"}
                </span>
                <span>Verify email</span>
              </div>

              <div className={`progress-line ${step === 2 ? "completed" : ""}`} />

              <div className={`progress-step ${step === 2 ? "active" : ""}`}>
                <span className="step-number">2</span>
                <span>Reset password</span>
              </div>
            </div>

            {error && (
              <div className="form-alert alert-error" role="alert">
                <span aria-hidden="true">!</span>
                <p>{error}</p>
              </div>
            )}

            {message && (
              <div
                className="form-alert alert-success"
                role="status"
                aria-live="polite"
              >
                <span aria-hidden="true">✓</span>
                <p>{message}</p>
              </div>
            )}

            {step === 1 ? (
              <form onSubmit={handleRequestOtp} className="auth-form">
                <label htmlFor="email">Email address</label>

                <div className="input-wrap">
                  <span className="input-icon" aria-hidden="true">✉</span>
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="you@example.com"
                    autoComplete="email"
                    maxLength={254}
                    required
                    disabled={loading}
                  />
                </div>

                <p className="field-hint">
                  Use the email address associated with your account.
                </p>

                <button
                  className="primary-button"
                  type="submit"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="button-spinner" />
                      Sending code...
                    </>
                  ) : (
                    <>Send verification code <span>→</span></>
                  )}
                </button>
              </form>
            ) : (
              <form onSubmit={handleResetPassword} className="auth-form">
                <div className="email-summary">
                  <span className="summary-icon">✉</span>
                  <div>
                    <strong>Check your inbox</strong>
                    <p>Enter the verification code for</p>
                    <span className="summary-email">{email.trim()}</span>
                  </div>
                </div>

                <div className="label-row">
                  <label htmlFor="otp">Verification code</label>
                </div>

                <div className="input-wrap">
                  <span className="input-icon" aria-hidden="true">⌑</span>
                  <input
                    id="otp"
                    type="text"
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    value={otp}
                    onChange={(event) =>
                      setOtp(
                        event.target.value.replace(/\D/g, "").slice(0, 6)
                      )
                    }
                    placeholder="Enter 6-digit code"
                    maxLength={6}
                    pattern="[0-9]{6}"
                    required
                    disabled={loading}
                  />
                </div>

                <label htmlFor="newPassword">New password</label>

                <div className="input-wrap">
                  <span className="input-icon" aria-hidden="true">⌑</span>
                  <input
                    id="newPassword"
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={newPassword}
                    onChange={(event) =>
                      setNewPassword(event.target.value)
                    }
                    placeholder="Enter a new password"
                    minLength={8}
                    maxLength={128}
                    required
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <p className="field-hint">
                  Use at least 8 characters.
                </p>

                <label htmlFor="confirmPassword">
                  Confirm new password
                </label>

                <div className="input-wrap">
                  <span className="input-icon" aria-hidden="true">⌑</span>
                  <input
                    id="confirmPassword"
                    type={showConfirmPassword ? "text" : "password"}
                    autoComplete="new-password"
                    value={confirmPassword}
                    onChange={(event) =>
                      setConfirmPassword(event.target.value)
                    }
                    placeholder="Re-enter your new password"
                    minLength={8}
                    maxLength={128}
                    required
                    disabled={loading}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() =>
                      setShowConfirmPassword(!showConfirmPassword)
                    }
                    aria-label={
                      showConfirmPassword
                        ? "Hide confirmation"
                        : "Show confirmation"
                    }
                  >
                    {showConfirmPassword ? "Hide" : "Show"}
                  </button>
                </div>

                <button
                  className="primary-button"
                  type="submit"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="button-spinner" />
                      Resetting password...
                    </>
                  ) : (
                    <>Reset password <span>→</span></>
                  )}
                </button>

                <button
                  className="secondary-button"
                  type="button"
                  onClick={changeEmail}
                  disabled={loading}
                >
                  ← Change email address
                </button>
              </form>
            )}

            <div className="form-footer">
              <span>Remember your password?</span>
              <Link to="/login">Back to login <span>→</span></Link>
            </div>

            <p className="security-note">
              <span aria-hidden="true">✓</span>
              Your account security is our priority.
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}
