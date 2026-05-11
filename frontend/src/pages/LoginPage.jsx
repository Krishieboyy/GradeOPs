import Navbar from "../components/Navbar";
import AuthCard from "../components/AuthCard";
import "../styles/landingpage.css";

export default function LoginPage() {
  return (
    <div className="landing-page">
      <div className="overlay">
        <Navbar />
        <section className="hero-section hero-section--centered">
          <AuthCard mode="login" />
        </section>
      </div>
    </div>
  );
}