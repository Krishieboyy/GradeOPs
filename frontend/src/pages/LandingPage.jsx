import Navbar from "../components/Navbar";
import AuthCard from "../components/AuthCard";
import "../styles/landingpage.css";

export default function LandingPage() {
  return (
    <div className="landing-page">
      <div className="overlay">
        <Navbar />

        <section className="hero-section">
          <div className="hero-left">
            <h1 className="hero-title">
              <span className="hero-title--white">GradeOps</span>
              <span className="hero-title--blue">Evaluate</span>
              <span className="hero-title--blue">With AI</span>
            </h1>

            <p className="hero-subtext">
              Transforming handwritten answer sheets into structured,
              explainable evaluation with OCR-powered grading workflows.
            </p>
          </div>

          <div className="hero-right">
            <AuthCard mode="register" />
          </div>
        </section>
      </div>
    </div>
  );
}