function Dashboard() {
  return (
    <div className="dashboard">

      <div className="dashboard-header">
        <h1>Dashboard</h1>

        <p>
          Welcome back to EduGram. Let's continue learning.
        </p>
      </div>

      <div className="dashboard-grid">

        <div className="dashboard-card">
          <h2>📚 Materials</h2>

          <p>
            Organize and access your study materials
            in one place.
          </p>
        </div>

        <div className="dashboard-card">
          <h2>🗺️ Roadmap</h2>

          <p>
            Follow your personalized learning roadmap.
          </p>
        </div>

        <div className="dashboard-card">
          <h2>📈 Progress</h2>

          <p>
            Track your learning progress and completed topics.
          </p>
        </div>

        <div className="dashboard-card">
          <h2>🤖 AI Assistant</h2>

          <p>
            Get AI-powered help with your learning.
          </p>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;