import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/useAuth";

function Navbar() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const getNavClass = ({ isActive }) =>
    isActive ? "nav-link active" : "nav-link";

  return (
    <nav className="navbar">

      <div
        className="navbar-brand"
        onClick={() => navigate("/dashboard")}
      >
        EduGram
      </div>

      <div className="navbar-links">

        <NavLink
          to="/dashboard"
          className={getNavClass}
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/materials"
          className={getNavClass}
        >
          Materials
        </NavLink>

        <NavLink
          to="/roadmap"
          className={getNavClass}
        >
          Roadmap
        </NavLink>

        <NavLink
          to="/progress"
          className={getNavClass}
        >
          Progress
        </NavLink>

      </div>

      <div className="navbar-user">

        <span>
          {user?.name || "Student"}
        </span>

        <button
          type="button"
          onClick={handleLogout}
        >
          Logout
        </button>

      </div>

    </nav>
  );
}

export default Navbar;