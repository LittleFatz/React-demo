import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import HomePage from "./pages/HomePage";
import ProjectsPage from "./pages/ProjectsPage";

function App() {
  return (
    <div className="min-h-screen bg-apple-light text-apple-gray antialiased">
      <NavBar />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/projects" element={<ProjectsPage />} />
        </Routes>
      </main>

      <footer
        id="contact"
        className="border-t border-white/60 bg-apple-light/80 px-6 py-10"
      >
        <div className="mx-auto flex max-w-6xl flex-col gap-4 text-sm text-apple-gray/70 md:flex-row md:items-center md:justify-between">
          <p>© {new Date().getFullYear()} Lin Studio. 灵感来自 Apple。</p>
          <div className="flex gap-4">
            <a href="mailto:hello@linstudio.design">hello@linstudio.design</a>
            <a href="https://www.linkedin.com" target="_blank" rel="noreferrer">
              LinkedIn
            </a>
            <a href="https://www.behance.net" target="_blank" rel="noreferrer">
              Behance
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;

