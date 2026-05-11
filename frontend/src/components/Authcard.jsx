import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "../styles/authcard.css";

export default function AuthCard({ mode = "register" }) {
  const isRegister = mode === "register";
  const navigate = useNavigate();
  const { register, login } = useAuth();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    agreed: false,
  });
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const [err, setErr] = useState("");

  const onChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((p) => ({
      ...p,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    setErr("");
    setMsg("");
    setLoading(true);

    try {
      if (isRegister) {
        if (!form.agreed) {
          throw new Error("Please accept the terms.");
        }
        await register(form.name, form.email, form.password);
        setMsg("Registration successful. Please login.");
        setTimeout(() => navigate("/login"), 800);
      } else {
        await login(form.email, form.password);
        navigate("/dashboard");
      }
    } catch (error) {
      setErr(error?.response?.data?.detail || error.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-card">
      <button className="auth-card__close" onClick={() => navigate("/")}>
        ×
      </button>

      <h2 className="auth-card__title">{isRegister ? "Registration" : "Login"}</h2>

      <form className="auth-form" onSubmit={onSubmit}>
        {isRegister && (
          <div className="auth-form__group">
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={form.name}
              onChange={onChange}
              required
            />
            <span className="auth-form__icon">👤</span>
          </div>
        )}

        <div className="auth-form__group">
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={form.email}
            onChange={onChange}
            required
          />
          <span className="auth-form__icon">✉</span>
        </div>

        <div className="auth-form__group">
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={form.password}
            onChange={onChange}
            required
          />
          <span className="auth-form__icon">🔒</span>
        </div>

        {isRegister && (
          <label className="auth-form__checkbox">
            <input
              type="checkbox"
              name="agreed"
              checked={form.agreed}
              onChange={onChange}
            />
            <span>I Agree to the Terms & Conditions</span>
          </label>
        )}

        {err && <p className="auth-form__error">{err}</p>}
        {msg && <p className="auth-form__success">{msg}</p>}

        <button type="submit" className="auth-form__submit" disabled={loading}>
          {loading ? "Please wait..." : isRegister ? "Register" : "Login"}
        </button>

        <p className="auth-form__footer">
          {isRegister ? (
            <>
              Already have an account? <span onClick={() => navigate("/login")}>Login</span>
            </>
          ) : (
            <>
              Don&apos;t have an account? <span onClick={() => navigate("/")}>Register</span>
            </>
          )}
        </p>
      </form>
    </div>
  );
}