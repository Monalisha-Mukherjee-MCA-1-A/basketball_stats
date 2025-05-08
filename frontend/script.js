// Configuration
const API_BASE_URL = "http://127.0.0.1:8000/api";
const AUTH_TOKEN_KEY = "basketball_stats_auth_token";
const ITEMS_PER_PAGE = 20;

// Enable CORS for all requests
document.addEventListener("DOMContentLoaded", function () {
  // Log configuration
  console.log("API Base URL:", API_BASE_URL);
  console.log("Auth Token Key:", AUTH_TOKEN_KEY);
});

// Authentication state
let isAuthenticated = false;
let currentUser = null;

// DOM Elements
document.addEventListener("DOMContentLoaded", () => {
  // Check authentication status
  checkAuthStatus();

  // Auth tabs
  const authTabs = document.querySelectorAll(".auth-tab");
  authTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const tabName = tab.getAttribute("data-tab");

      // Update active tab
      authTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      // Show corresponding content
      document.querySelectorAll(".auth-tab-content").forEach((content) => {
        content.classList.remove("active");
      });
      document.getElementById(`${tabName}-tab`).classList.add("active");
    });
  });

  // Main login form
  document.getElementById("login-button-main").addEventListener("click", () => {
    const username = document.getElementById("login-username-main").value;
    const password = document.getElementById("login-password-main").value;

    loginAndShowDashboard(username, password);
  });

  // Main register form
  document
    .getElementById("register-button-main")
    .addEventListener("click", () => {
      const username = document.getElementById("register-username-main").value;
      const email = document.getElementById("register-email-main").value;
      const password = document.getElementById("register-password-main").value;
      const confirmPassword = document.getElementById(
        "register-confirm-password-main"
      ).value;

      if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      registerAndShowLogin(username, email, password);
    });

  // Navigation
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const sectionId = link.getAttribute("data-section");
      showSection(sectionId);
    });
  });

  // Filter buttons
  document
    .getElementById("filter-teams")
    .addEventListener("click", () => filterTeams());
  document
    .getElementById("filter-players")
    .addEventListener("click", () => filterPlayers());
  document
    .getElementById("filter-matches")
    .addEventListener("click", () => filterMatches());
  document
    .getElementById("filter-player-stats")
    .addEventListener("click", () => filterPlayerStats());
  document
    .getElementById("filter-team-stats")
    .addEventListener("click", () => filterTeamStats());

  // Search buttons
  document
    .getElementById("search-teams")
    .addEventListener("click", () => searchTeams());
  document
    .getElementById("search-players")
    .addEventListener("click", () => searchPlayers());
  document
    .getElementById("search-matches")
    .addEventListener("click", () => searchMatches());

  // Search input enter key
  document.getElementById("team-search").addEventListener("keyup", (e) => {
    if (e.key === "Enter") searchTeams();
  });
  document.getElementById("player-search").addEventListener("keyup", (e) => {
    if (e.key === "Enter") searchPlayers();
  });
  document.getElementById("match-search").addEventListener("keyup", (e) => {
    if (e.key === "Enter") searchMatches();
  });

  // Prediction buttons
  document
    .getElementById("predict-player")
    .addEventListener("click", () => predictPlayerPerformance());
  document
    .getElementById("predict-match")
    .addEventListener("click", () => predictMatchOutcome());
  document
    .getElementById("compare-players")
    .addEventListener("click", () => comparePlayers());

  // Modal close buttons
  document.querySelectorAll(".close").forEach((closeBtn) => {
    closeBtn.addEventListener("click", () => {
      document.querySelectorAll(".modal").forEach((modal) => {
        modal.style.display = "none";
      });
    });
  });

  // Auth button
  document.getElementById("auth-button").addEventListener("click", () => {
    if (isAuthenticated) {
      logout();
    } else {
      showAuthModal();
    }
  });

  // Login/Register form toggle
  document.getElementById("show-register").addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
    document.getElementById("auth-modal-title").textContent = "Register";
  });

  document.getElementById("show-login").addEventListener("click", (e) => {
    e.preventDefault();
    document.getElementById("register-form").style.display = "none";
    document.getElementById("login-form").style.display = "block";
    document.getElementById("auth-modal-title").textContent = "Login";
  });

  // Login/Register form submission
  document.getElementById("login-button").addEventListener("click", () => {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    // Direct login without using the login function
    fetch(`${API_BASE_URL}/auth/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          return response.text().then((text) => {
            throw new Error(`Login failed: ${text}`);
          });
        }
      })
      .then((data) => {
        localStorage.setItem(AUTH_TOKEN_KEY, data.token);
        isAuthenticated = true;
        document.getElementById("auth-modal").style.display = "none";

        // Update UI
        const userInfo = document.getElementById("user-info");
        const authButton = document.getElementById("auth-button");
        const adminLink = document.getElementById("admin-link");

        userInfo.textContent = `Logged in as ${data.username}`;
        authButton.textContent = "Logout";
        adminLink.style.display = "block";

        alert("Login successful!");
      })
      .catch((error) => {
        console.error("Login error:", error);
        alert(error.message);
      });
  });

  document.getElementById("register-button").addEventListener("click", () => {
    const username = document.getElementById("register-username").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById(
      "register-confirm-password"
    ).value;

    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      return;
    }

    // Direct registration without using the register function
    fetch(`${API_BASE_URL}/auth/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          return response.text().then((text) => {
            throw new Error(`Registration failed: ${text}`);
          });
        }
      })
      .then((data) => {
        alert("Registration successful! You can now login.");
        document.getElementById("register-form").style.display = "none";
        document.getElementById("login-form").style.display = "block";
        document.getElementById("auth-modal-title").textContent = "Login";
        document.getElementById("login-username").value = username;
        document.getElementById("login-password").focus();
      })
      .catch((error) => {
        console.error("Registration error:", error);
        alert(error.message);
      });
  });

  // Admin add buttons
  document.querySelectorAll(".add-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const type = btn.getAttribute("data-type");
      showAddForm(type);
    });
  });

  // Export buttons
  document.querySelectorAll(".export-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const type = btn.getAttribute("data-type");
      exportData(type);
    });
  });

  // Initial data loading
  loadTeams();
  loadTeamDropdowns();
  loadPlayerDropdowns();
  loadMatchDropdowns();
});

// Navigation Functions
function showSection(sectionId) {
  // Hide all sections
  document.querySelectorAll(".content-section").forEach((section) => {
    section.classList.remove("active");
  });

  // Show selected section
  document.getElementById(sectionId).classList.add("active");

  // Update active nav link
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.remove("active");
  });
  document
    .querySelector(`.nav-link[data-section="${sectionId}"]`)
    .classList.add("active");

  // Load data for the section if needed
  switch (sectionId) {
    case "teams":
      loadTeams();
      break;
    case "players":
      loadPlayers();
      break;
    case "matches":
      loadMatches();
      break;
    case "player-stats":
      loadPlayerStats();
      break;
    case "team-stats":
      loadTeamStats();
      break;
    case "predictions":
      // Predictions are loaded on-demand
      break;
  }
}

// API Utility Functions
async function fetchAPI(endpoint, params = {}) {
  const url = new URL(`${API_BASE_URL}/${endpoint}/`);

  // Add query parameters
  Object.keys(params).forEach((key) => {
    if (params[key]) {
      url.searchParams.append(key, params[key]);
    }
  });

  try {
    const headers = {};
    if (isAuthenticated) {
      headers["Authorization"] = `Token ${localStorage.getItem(
        AUTH_TOKEN_KEY
      )}`;
    }

    const response = await fetch(url, { headers });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error("API fetch error:", error);
    return { results: [], count: 0 };
  }
}

async function postAPI(endpoint, data) {
  try {
    const headers = {
      "Content-Type": "application/json",
    };

    if (isAuthenticated) {
      headers["Authorization"] = `Token ${localStorage.getItem(
        AUTH_TOKEN_KEY
      )}`;
    }

    const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API post error:", error);
    return null;
  }
}

async function putAPI(endpoint, data) {
  try {
    const headers = {
      "Content-Type": "application/json",
    };

    if (isAuthenticated) {
      headers["Authorization"] = `Token ${localStorage.getItem(
        AUTH_TOKEN_KEY
      )}`;
    }

    const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
      method: "PUT",
      headers: headers,
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API put error:", error);
    return null;
  }
}

async function deleteAPI(endpoint) {
  try {
    const headers = {};
    if (isAuthenticated) {
      headers["Authorization"] = `Token ${localStorage.getItem(
        AUTH_TOKEN_KEY
      )}`;
    }

    const response = await fetch(`${API_BASE_URL}/${endpoint}/`, {
      method: "DELETE",
      headers: headers,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    return true;
  } catch (error) {
    console.error("API delete error:", error);
    return false;
  }
}

// Data Loading Functions
async function loadTeams(page = 1, filters = {}) {
  const params = { ...filters, page };
  const data = await fetchAPI("teams", params);
  renderTeams(data);
  renderPagination(data, "teams-pagination", (newPage) =>
    loadTeams(newPage, filters)
  );
}

async function loadPlayers(page = 1, filters = {}) {
  const params = { ...filters, page };
  const data = await fetchAPI("players", params);
  renderPlayers(data);
  renderPagination(data, "players-pagination", (newPage) =>
    loadPlayers(newPage, filters)
  );
}

async function loadMatches(page = 1, filters = {}) {
  const params = { ...filters, page };
  const data = await fetchAPI("matches", params);
  renderMatches(data);
  renderPagination(data, "matches-pagination", (newPage) =>
    loadMatches(newPage, filters)
  );
}

async function loadPlayerStats(page = 1, filters = {}) {
  const params = { ...filters, page };
  const data = await fetchAPI("player-stats", params);
  renderPlayerStats(data);
  renderPagination(data, "player-stats-pagination", (newPage) =>
    loadPlayerStats(newPage, filters)
  );
}

async function loadTeamStats(page = 1, filters = {}) {
  const params = { ...filters, page };
  const data = await fetchAPI("team-stats", params);
  renderTeamStats(data);
  renderPagination(data, "team-stats-pagination", (newPage) =>
    loadTeamStats(newPage, filters)
  );
}

// Dropdown Loading Functions
async function loadTeamDropdowns() {
  const data = await fetchAPI("teams");
  const teams = data.results || [];

  // Populate all team dropdowns
  const dropdowns = [
    document.getElementById("player-team"),
    document.getElementById("match-team"),
    document.getElementById("team-stats-team"),
  ];

  dropdowns.forEach((dropdown) => {
    if (dropdown) {
      // Keep the "All" option
      dropdown.innerHTML = '<option value="">All</option>';

      // Add team options
      teams.forEach((team) => {
        const option = document.createElement("option");
        option.value = team.id;
        option.textContent = team.name;
        dropdown.appendChild(option);
      });
    }
  });
}

async function loadPlayerDropdowns() {
  const data = await fetchAPI("players");
  const players = data.results || [];

  // Populate all player dropdowns
  const dropdowns = [
    document.getElementById("stats-player"),
    document.getElementById("player-prediction-player"),
    document.getElementById("player-comparison-player1"),
    document.getElementById("player-comparison-player2"),
  ];

  dropdowns.forEach((dropdown) => {
    if (dropdown) {
      // Keep the "All" or "Select Player" option
      const firstOption = dropdown.querySelector("option");
      dropdown.innerHTML = "";
      dropdown.appendChild(firstOption);

      // Add player options
      players.forEach((player) => {
        const option = document.createElement("option");
        option.value = player.id;
        option.textContent =
          player.full_name || `${player.first_name} ${player.last_name}`;
        dropdown.appendChild(option);
      });
    }
  });
}

async function loadMatchDropdowns() {
  const data = await fetchAPI("matches");
  const matches = data.results || [];

  // Populate all match dropdowns
  const dropdowns = [
    document.getElementById("stats-match"),
    document.getElementById("team-stats-match"),
    document.getElementById("player-prediction-match"),
    document.getElementById("match-prediction-match"),
  ];

  dropdowns.forEach((dropdown) => {
    if (dropdown) {
      // Keep the "All" or "Select Match" option
      const firstOption = dropdown.querySelector("option");
      dropdown.innerHTML = "";
      dropdown.appendChild(firstOption);

      // Add match options
      matches.forEach((match) => {
        const option = document.createElement("option");
        option.value = match.id;
        option.textContent = `${match.home_team_name} vs ${
          match.away_team_name
        } (${new Date(match.date).toLocaleDateString()})`;
        dropdown.appendChild(option);
      });
    }
  });
}

// Rendering Functions
function renderTeams(data) {
  const tableBody = document.querySelector("#teams-table tbody");
  tableBody.innerHTML = "";

  const teams = data.results || [];

  teams.forEach((team) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${team.name}</td>
            <td>${team.city}</td>
            <td>${team.abbreviation}</td>
            <td>${team.conference}</td>
            <td>${team.division}</td>
            <td>
                <button class="action-btn view" data-id="${team.id}" data-type="team">View</button>
            </td>
        `;
    tableBody.appendChild(row);
  });

  // Add event listeners to view buttons
  document.querySelectorAll("#teams-table .view").forEach((button) => {
    button.addEventListener("click", () =>
      showTeamDetails(button.getAttribute("data-id"))
    );
  });
}

function renderPlayers(data) {
  const tableBody = document.querySelector("#players-table tbody");
  tableBody.innerHTML = "";

  const players = data.results || [];

  players.forEach((player) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${player.first_name} ${player.last_name}</td>
            <td>${player.team_name}</td>
            <td>${player.position}</td>
            <td>${player.jersey_number}</td>
            <td>${player.height}</td>
            <td>${player.weight}</td>
            <td>${player.age}</td>
            <td>
                <button class="action-btn view" data-id="${player.id}" data-type="player">View</button>
                <button class="action-btn predict" data-id="${player.id}">Predict</button>
            </td>
        `;
    tableBody.appendChild(row);
  });

  // Add event listeners to buttons
  document.querySelectorAll("#players-table .view").forEach((button) => {
    button.addEventListener("click", () =>
      showPlayerDetails(button.getAttribute("data-id"))
    );
  });

  document.querySelectorAll("#players-table .predict").forEach((button) => {
    button.addEventListener("click", () => {
      const playerId = button.getAttribute("data-id");
      document.getElementById("player-prediction-player").value = playerId;
      showSection("predictions");
      document
        .getElementById("predict-player")
        .scrollIntoView({ behavior: "smooth" });
    });
  });
}

function renderMatches(data) {
  const tableBody = document.querySelector("#matches-table tbody");
  tableBody.innerHTML = "";

  const matches = data.results || [];

  matches.forEach((match) => {
    const score = match.is_completed
      ? `${match.home_team_score} - ${match.away_team_score}`
      : "TBD";
    const status = match.is_completed ? "Completed" : "Upcoming";

    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${new Date(match.date).toLocaleDateString()}</td>
            <td>${match.home_team_name}</td>
            <td>${match.away_team_name}</td>
            <td>${score}</td>
            <td>${match.season}</td>
            <td>${status}</td>
            <td>
                <button class="action-btn view" data-id="${
                  match.id
                }" data-type="match">View</button>
                ${
                  match.is_completed
                    ? ""
                    : '<button class="action-btn predict" data-id="' +
                      match.id +
                      '">Predict</button>'
                }
            </td>
        `;
    tableBody.appendChild(row);
  });

  // Add event listeners to buttons
  document.querySelectorAll("#matches-table .view").forEach((button) => {
    button.addEventListener("click", () =>
      showMatchDetails(button.getAttribute("data-id"))
    );
  });

  document.querySelectorAll("#matches-table .predict").forEach((button) => {
    button.addEventListener("click", () => {
      const matchId = button.getAttribute("data-id");
      document.getElementById("match-prediction-match").value = matchId;
      showSection("predictions");
      document
        .getElementById("predict-match")
        .scrollIntoView({ behavior: "smooth" });
    });
  });
}

function renderPlayerStats(data) {
  const tableBody = document.querySelector("#player-stats-table tbody");
  tableBody.innerHTML = "";

  const stats = data.results || [];

  stats.forEach((stat) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${stat.player_name}</td>
            <td>${stat.match_description}</td>
            <td>${stat.points}</td>
            <td>${stat.rebounds}</td>
            <td>${stat.assists}</td>
            <td>${stat.steals}</td>
            <td>${stat.blocks}</td>
            <td>${(stat.field_goal_percentage * 100).toFixed(1)}%</td>
            <td>${(stat.three_point_percentage * 100).toFixed(1)}%</td>
            <td>${(stat.free_throw_percentage * 100).toFixed(1)}%</td>
        `;
    tableBody.appendChild(row);
  });
}

function renderTeamStats(data) {
  const tableBody = document.querySelector("#team-stats-table tbody");
  tableBody.innerHTML = "";

  const stats = data.results || [];

  stats.forEach((stat) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td>${stat.team_name}</td>
            <td>${stat.match_description}</td>
            <td>${stat.points}</td>
            <td>${stat.rebounds}</td>
            <td>${stat.assists}</td>
            <td>${stat.steals}</td>
            <td>${stat.blocks}</td>
            <td>${(stat.field_goal_percentage * 100).toFixed(1)}%</td>
            <td>${(stat.three_point_percentage * 100).toFixed(1)}%</td>
            <td>${(stat.free_throw_percentage * 100).toFixed(1)}%</td>
        `;
    tableBody.appendChild(row);
  });
}

function renderPagination(data, containerId, callback) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";

  if (!data.count) return;

  const totalPages = Math.ceil(data.count / ITEMS_PER_PAGE);
  const currentPage = data.next
    ? parseInt(new URL(data.next).searchParams.get("page")) - 1
    : data.previous
    ? parseInt(new URL(data.previous).searchParams.get("page")) + 1
    : 1;

  // Previous button
  if (data.previous) {
    const prevButton = document.createElement("button");
    prevButton.textContent = "«";
    prevButton.addEventListener("click", () => callback(currentPage - 1));
    container.appendChild(prevButton);
  }

  // Page buttons
  for (let i = 1; i <= totalPages; i++) {
    const pageButton = document.createElement("button");
    pageButton.textContent = i;
    if (i === currentPage) {
      pageButton.classList.add("active");
    }
    pageButton.addEventListener("click", () => callback(i));
    container.appendChild(pageButton);
  }

  // Next button
  if (data.next) {
    const nextButton = document.createElement("button");
    nextButton.textContent = "»";
    nextButton.addEventListener("click", () => callback(currentPage + 1));
    container.appendChild(nextButton);
  }
}

// Filter Functions
function filterTeams() {
  const conference = document.getElementById("team-conference").value;
  const division = document.getElementById("team-division").value;

  const filters = {
    conference: conference,
    division: division,
  };

  loadTeams(1, filters);
}

function filterPlayers() {
  const team = document.getElementById("player-team").value;
  const position = document.getElementById("player-position").value;

  const filters = {
    team: team,
    position: position,
  };

  loadPlayers(1, filters);
}

function filterMatches() {
  const season = document.getElementById("match-season").value;
  const team = document.getElementById("match-team").value;
  const completed = document.getElementById("match-completed").value;

  const filters = {
    season: season,
    is_completed: completed,
  };

  // Handle team filter differently since we need to check both home and away teams
  if (team) {
    filters.home_team = team;
    // We'll handle this in the API call by using OR logic
  }

  loadMatches(1, filters);
}

function filterPlayerStats() {
  const player = document.getElementById("stats-player").value;
  const match = document.getElementById("stats-match").value;

  const filters = {
    player: player,
    match: match,
  };

  loadPlayerStats(1, filters);
}

function filterTeamStats() {
  const team = document.getElementById("team-stats-team").value;
  const match = document.getElementById("team-stats-match").value;

  const filters = {
    team: team,
    match: match,
  };

  loadTeamStats(1, filters);
}

// Detail View Functions
async function showTeamDetails(teamId) {
  try {
    const team = await fetchAPI(`teams/${teamId}`);
    const players = await fetchAPI(`teams/${teamId}/players`);
    const matches = await fetchAPI(`teams/${teamId}/matches`);
    // Fetch team stats for potential future use
    // const stats = await fetchAPI(`teams/${teamId}/stats`);

    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");

    modalTitle.textContent = `${team.city} ${team.name}`;

    let content = `
      <div class="detail-section">
        <h3>Team Information</h3>
        <p><strong>Abbreviation:</strong> ${team.abbreviation}</p>
        <p><strong>Conference:</strong> ${team.conference}</p>
        <p><strong>Division:</strong> ${team.division}</p>
      </div>

      <div class="detail-section">
        <h3>Players</h3>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Position</th>
              <th>Jersey #</th>
            </tr>
          </thead>
          <tbody>
    `;

    players.forEach((player) => {
      content += `
        <tr>
          <td>${player.first_name} ${player.last_name}</td>
          <td>${player.position}</td>
          <td>${player.jersey_number}</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>

      <div class="detail-section">
        <h3>Recent Matches</h3>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Opponent</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
    `;

    matches.slice(0, 5).forEach((match) => {
      const isHomeTeam = match.home_team === parseInt(teamId);
      const opponent = isHomeTeam ? match.away_team_name : match.home_team_name;
      let result = "Upcoming";

      if (match.is_completed) {
        const teamScore = isHomeTeam
          ? match.home_team_score
          : match.away_team_score;
        const opponentScore = isHomeTeam
          ? match.away_team_score
          : match.home_team_score;
        result =
          teamScore > opponentScore
            ? "Win"
            : teamScore < opponentScore
            ? "Loss"
            : "Tie";
        result += ` (${teamScore}-${opponentScore})`;
      }

      content += `
        <tr>
          <td>${new Date(match.date).toLocaleDateString()}</td>
          <td>${opponent}</td>
          <td>${result}</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>
    `;

    modalBody.innerHTML = content;
    document.getElementById("modal").style.display = "block";
  } catch (error) {
    console.error("Error fetching team details:", error);
  }
}

async function showPlayerDetails(playerId) {
  try {
    const player = await fetchAPI(`players/${playerId}`);
    const stats = await fetchAPI(`players/${playerId}/stats`);

    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");

    modalTitle.textContent = `${player.first_name} ${player.last_name}`;

    let content = `
      <div class="detail-section">
        <h3>Player Information</h3>
        <p><strong>Team:</strong> ${player.team_name}</p>
        <p><strong>Position:</strong> ${player.position}</p>
        <p><strong>Jersey Number:</strong> ${player.jersey_number}</p>
        <p><strong>Height:</strong> ${player.height}</p>
        <p><strong>Weight:</strong> ${player.weight}</p>
        <p><strong>Age:</strong> ${player.age}</p>
        <p><strong>Birth Date:</strong> ${new Date(
          player.birth_date
        ).toLocaleDateString()}</p>
      </div>

      <div class="detail-section">
        <h3>Recent Statistics</h3>
        <table>
          <thead>
            <tr>
              <th>Match</th>
              <th>PTS</th>
              <th>REB</th>
              <th>AST</th>
              <th>STL</th>
              <th>BLK</th>
            </tr>
          </thead>
          <tbody>
    `;

    stats.slice(0, 5).forEach((stat) => {
      content += `
        <tr>
          <td>${stat.match_description}</td>
          <td>${stat.points}</td>
          <td>${stat.rebounds}</td>
          <td>${stat.assists}</td>
          <td>${stat.steals}</td>
          <td>${stat.blocks}</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>
    `;

    modalBody.innerHTML = content;
    document.getElementById("modal").style.display = "block";
  } catch (error) {
    console.error("Error fetching player details:", error);
  }
}

async function showMatchDetails(matchId) {
  try {
    const match = await fetchAPI(`matches/${matchId}`);
    const playerStats = await fetchAPI(`matches/${matchId}/player_stats`);
    const teamStats = await fetchAPI(`matches/${matchId}/team_stats`);

    const modalTitle = document.getElementById("modal-title");
    const modalBody = document.getElementById("modal-body");

    modalTitle.textContent = `${match.home_team_name} vs ${match.away_team_name}`;

    let content = `
      <div class="detail-section">
        <h3>Match Information</h3>
        <p><strong>Date:</strong> ${new Date(
          match.date
        ).toLocaleDateString()}</p>
        <p><strong>Season:</strong> ${match.season}</p>
        <p><strong>Status:</strong> ${
          match.is_completed ? "Completed" : "Upcoming"
        }</p>
        ${
          match.is_completed
            ? `<p><strong>Final Score:</strong> ${match.home_team_name} ${match.home_team_score} - ${match.away_team_score} ${match.away_team_name}</p>`
            : ""
        }
      </div>

      <div class="detail-section">
        <h3>Team Statistics</h3>
        <table>
          <thead>
            <tr>
              <th>Team</th>
              <th>PTS</th>
              <th>REB</th>
              <th>AST</th>
              <th>STL</th>
              <th>BLK</th>
              <th>FG%</th>
              <th>3P%</th>
              <th>FT%</th>
            </tr>
          </thead>
          <tbody>
    `;

    teamStats.forEach((stat) => {
      content += `
        <tr>
          <td>${stat.team_name}</td>
          <td>${stat.points}</td>
          <td>${stat.rebounds}</td>
          <td>${stat.assists}</td>
          <td>${stat.steals}</td>
          <td>${stat.blocks}</td>
          <td>${(stat.field_goal_percentage * 100).toFixed(1)}%</td>
          <td>${(stat.three_point_percentage * 100).toFixed(1)}%</td>
          <td>${(stat.free_throw_percentage * 100).toFixed(1)}%</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>

      <div class="detail-section">
        <h3>Player Statistics</h3>
        <table>
          <thead>
            <tr>
              <th>Player</th>
              <th>Team</th>
              <th>PTS</th>
              <th>REB</th>
              <th>AST</th>
              <th>STL</th>
              <th>BLK</th>
            </tr>
          </thead>
          <tbody>
    `;

    playerStats.forEach((stat) => {
      content += `
        <tr>
          <td>${stat.player_name}</td>
          <td>${stat.team_name}</td>
          <td>${stat.points}</td>
          <td>${stat.rebounds}</td>
          <td>${stat.assists}</td>
          <td>${stat.steals}</td>
          <td>${stat.blocks}</td>
        </tr>
      `;
    });

    content += `
          </tbody>
        </table>
      </div>
    `;

    modalBody.innerHTML = content;
    document.getElementById("modal").style.display = "block";
  } catch (error) {
    console.error("Error fetching match details:", error);
  }
}

// Prediction Functions
async function predictPlayerPerformance() {
  const playerId = document.getElementById("player-prediction-player").value;
  const matchId = document.getElementById("player-prediction-match").value;

  if (!playerId || !matchId) {
    alert("Please select both a player and a match for prediction.");
    return;
  }

  try {
    const response = await postAPI(`players/${playerId}/predict_performance`, {
      match_id: matchId,
    });

    if (response) {
      const resultContainer = document.getElementById(
        "player-prediction-result"
      );
      resultContainer.classList.add("active");

      // Format the prediction data
      const predictionData = JSON.parse(response.prediction_data);
      let resultHTML = `
        <h4>Prediction Results</h4>
        <p><strong>Confidence:</strong> ${(response.confidence * 100).toFixed(
          1
        )}%</p>
        <div class="prediction-stats">
          <p><strong>Points:</strong> ${predictionData.points.toFixed(1)}</p>
          <p><strong>Rebounds:</strong> ${predictionData.rebounds.toFixed(
            1
          )}</p>
          <p><strong>Assists:</strong> ${predictionData.assists.toFixed(1)}</p>
          <p><strong>Steals:</strong> ${predictionData.steals.toFixed(1)}</p>
          <p><strong>Blocks:</strong> ${predictionData.blocks.toFixed(1)}</p>
          <p><strong>Field Goal %:</strong> ${(
            predictionData.field_goal_percentage * 100
          ).toFixed(1)}%</p>
          <p><strong>Three Point %:</strong> ${(
            predictionData.three_point_percentage * 100
          ).toFixed(1)}%</p>
          <p><strong>Free Throw %:</strong> ${(
            predictionData.free_throw_percentage * 100
          ).toFixed(1)}%</p>
        </div>
      `;

      resultContainer.innerHTML = resultHTML;
    }
  } catch (error) {
    console.error("Error predicting player performance:", error);
    alert("Failed to predict player performance. Please try again.");
  }
}

async function predictMatchOutcome() {
  const matchId = document.getElementById("match-prediction-match").value;

  if (!matchId) {
    alert("Please select a match for prediction.");
    return;
  }

  try {
    const response = await postAPI(`matches/${matchId}/predict_outcome`, {});

    if (response) {
      const resultContainer = document.getElementById(
        "match-prediction-result"
      );
      resultContainer.classList.add("active");

      // Format the prediction data
      const predictionData = JSON.parse(response.prediction_data);
      let resultHTML = `
        <h4>Prediction Results</h4>
        <p><strong>Confidence:</strong> ${(response.confidence * 100).toFixed(
          1
        )}%</p>
        <div class="prediction-stats">
          <p><strong>Predicted Winner:</strong> ${
            predictionData.winner_name
          }</p>
          <p><strong>Predicted Score:</strong> ${
            predictionData.home_team_name
          } ${predictionData.home_team_score.toFixed(
        0
      )} - ${predictionData.away_team_score.toFixed(0)} ${
        predictionData.away_team_name
      }</p>
          <p><strong>Predicted Point Difference:</strong> ${Math.abs(
            predictionData.point_difference
          ).toFixed(1)}</p>
        </div>
      `;

      resultContainer.innerHTML = resultHTML;
    }
  } catch (error) {
    console.error("Error predicting match outcome:", error);
    alert("Failed to predict match outcome. Please try again.");
  }
}

async function comparePlayers() {
  const player1Id = document.getElementById("player-comparison-player1").value;
  const player2Id = document.getElementById("player-comparison-player2").value;

  if (!player1Id || !player2Id) {
    alert("Please select two players to compare.");
    return;
  }

  if (player1Id === player2Id) {
    alert("Please select two different players to compare.");
    return;
  }

  try {
    const response = await postAPI("predictions/compare_players", {
      player1_id: player1Id,
      player2_id: player2Id,
    });

    if (response) {
      const resultContainer = document.getElementById(
        "player-comparison-result"
      );
      resultContainer.classList.add("active");

      // Format the comparison data
      const comparisonData = JSON.parse(response.prediction_data);
      let resultHTML = `
        <h4>Player Comparison Results</h4>
        <table class="comparison-table">
          <thead>
            <tr>
              <th>Statistic</th>
              <th>${comparisonData.player1_name}</th>
              <th>${comparisonData.player2_name}</th>
              <th>Difference</th>
            </tr>
          </thead>
          <tbody>
      `;

      // Add rows for each statistic
      const stats = [
        { key: "points", label: "Points" },
        { key: "rebounds", label: "Rebounds" },
        { key: "assists", label: "Assists" },
        { key: "steals", label: "Steals" },
        { key: "blocks", label: "Blocks" },
        { key: "field_goal_percentage", label: "FG%", isPercentage: true },
        { key: "three_point_percentage", label: "3P%", isPercentage: true },
        { key: "free_throw_percentage", label: "FT%", isPercentage: true },
      ];

      stats.forEach((stat) => {
        const player1Value = stat.isPercentage
          ? (comparisonData.player1_stats[stat.key] * 100).toFixed(1) + "%"
          : comparisonData.player1_stats[stat.key].toFixed(1);

        const player2Value = stat.isPercentage
          ? (comparisonData.player2_stats[stat.key] * 100).toFixed(1) + "%"
          : comparisonData.player2_stats[stat.key].toFixed(1);

        const difference = stat.isPercentage
          ? (
              (comparisonData.player1_stats[stat.key] -
                comparisonData.player2_stats[stat.key]) *
              100
            ).toFixed(1) + "%"
          : (
              comparisonData.player1_stats[stat.key] -
              comparisonData.player2_stats[stat.key]
            ).toFixed(1);

        resultHTML += `
          <tr>
            <td>${stat.label}</td>
            <td>${player1Value}</td>
            <td>${player2Value}</td>
            <td>${difference}</td>
          </tr>
        `;
      });

      resultHTML += `
          </tbody>
        </table>
        <p class="comparison-summary"><strong>Summary:</strong> ${comparisonData.summary}</p>
      `;

      resultContainer.innerHTML = resultHTML;
    }
  } catch (error) {
    console.error("Error comparing players:", error);
    alert("Failed to compare players. Please try again.");
  }
}

// Authentication Functions
function checkAuthStatus() {
  const token = localStorage.getItem(AUTH_TOKEN_KEY);
  if (token) {
    isAuthenticated = true;
    fetchUserInfo();
    showDashboard();
  } else {
    isAuthenticated = false;
    updateAuthUI();
    showAuthView();
  }
}

function showAuthView() {
  document.getElementById("auth-view").style.display = "flex";
  document.getElementById("dashboard-view").style.display = "none";
}

function showDashboard() {
  document.getElementById("auth-view").style.display = "none";
  document.getElementById("dashboard-view").style.display = "block";

  // Load initial data
  loadTeams();
  loadTeamDropdowns();
  loadPlayerDropdowns();
  loadMatchDropdowns();
}

async function loginAndShowDashboard(username, password) {
  try {
    console.log("Attempting to login user:", username);

    const response = await fetch(`${API_BASE_URL}/auth/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    console.log("Login response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Login error response:", errorText);
      throw new Error(`Login failed: ${errorText}`);
    }

    const data = await response.json();
    console.log("Login successful:", data);

    if (data && data.token) {
      localStorage.setItem(AUTH_TOKEN_KEY, data.token);
      isAuthenticated = true;

      // Set current user
      currentUser = {
        id: data.user_id,
        username: data.username,
        email: data.email,
      };

      // Update UI
      updateAuthUI();

      // Show dashboard
      showDashboard();

      // No need for alert in the main flow
      // alert("Login successful!");
    } else {
      alert("Login failed. Please check your credentials.");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert(error.message);
  }
}

async function registerAndShowLogin(username, email, password) {
  try {
    console.log("Attempting to register user:", username, email);

    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    console.log("Registration response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Registration error response:", errorText);
      throw new Error(`Registration failed: ${errorText}`);
    }

    const data = await response.json();
    console.log("Registration successful:", data);

    if (data && data.id) {
      alert("Registration successful! You can now login.");

      // Switch to login tab
      document
        .querySelectorAll(".auth-tab")
        .forEach((t) => t.classList.remove("active"));
      document
        .querySelector(".auth-tab[data-tab='login']")
        .classList.add("active");

      document.querySelectorAll(".auth-tab-content").forEach((content) => {
        content.classList.remove("active");
      });
      document.getElementById("login-tab").classList.add("active");

      // Pre-fill username
      document.getElementById("login-username-main").value = username;
      document.getElementById("login-password-main").focus();
    } else {
      alert("Registration failed. Please try again.");
    }
  } catch (error) {
    console.error("Registration error:", error);
    alert(error.message);
  }
}

async function fetchUserInfo() {
  try {
    console.log("Fetching user info");

    // Use fetch directly for debugging
    const response = await fetch(`${API_BASE_URL}/auth/user/`, {
      headers: {
        Authorization: `Token ${localStorage.getItem(AUTH_TOKEN_KEY)}`,
      },
    });

    console.log("User info response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("User info error response:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const user = await response.json();
    console.log("User info:", user);

    currentUser = user;
    updateAuthUI();
  } catch (error) {
    console.error("Error fetching user info:", error);
    logout();
  }
}

function updateAuthUI() {
  const userInfo = document.getElementById("user-info");
  const authButton = document.getElementById("auth-button");
  const adminLink = document.getElementById("admin-link");

  if (isAuthenticated && currentUser) {
    userInfo.textContent = `Logged in as ${currentUser.username}`;
    authButton.textContent = "Logout";
    adminLink.style.display = "block";
  } else {
    userInfo.textContent = "Not logged in";
    authButton.textContent = "Login";
    adminLink.style.display = "none";
  }
}

function showAuthModal() {
  document.getElementById("auth-modal").style.display = "block";
  document.getElementById("login-form").style.display = "block";
  document.getElementById("register-form").style.display = "none";
  document.getElementById("auth-modal-title").textContent = "Login";
  document.getElementById("login-username").focus();
}

async function login(username, password) {
  try {
    console.log("Attempting to login user:", username);

    // Use fetch directly for debugging
    const response = await fetch(`${API_BASE_URL}/auth/token/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    });

    console.log("Login response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Login error response:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Login successful:", data);

    if (data && data.token) {
      localStorage.setItem(AUTH_TOKEN_KEY, data.token);
      isAuthenticated = true;
      document.getElementById("auth-modal").style.display = "none";
      await fetchUserInfo();
      alert("Login successful!");
    } else {
      alert("Login failed. Please check your credentials.");
    }
  } catch (error) {
    console.error("Login error:", error);
    alert("Login failed. Please try again: " + error.message);
  }
}

async function register(username, email, password) {
  try {
    console.log("Attempting to register user:", username, email);

    // Use fetch directly for debugging
    const response = await fetch(`${API_BASE_URL}/auth/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    });

    console.log("Registration response status:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Registration error response:", errorText);
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log("Registration successful:", data);

    if (data && data.id) {
      alert("Registration successful! You can now login.");
      document.getElementById("register-form").style.display = "none";
      document.getElementById("login-form").style.display = "block";
      document.getElementById("auth-modal-title").textContent = "Login";
      document.getElementById("login-username").value = username;
      document.getElementById("login-password").focus();
    } else {
      alert("Registration failed. Please try again.");
    }
  } catch (error) {
    console.error("Registration error:", error);
    alert("Registration failed. Please try again: " + error.message);
  }
}

function logout() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  isAuthenticated = false;
  currentUser = null;
  updateAuthUI();
  showAuthView();
  alert("You have been logged out.");
}

// Search Functions
function searchTeams() {
  const searchTerm = document.getElementById("team-search").value.trim();
  if (!searchTerm) {
    loadTeams();
    return;
  }

  const filters = {
    search: searchTerm,
  };
  loadTeams(1, filters);
}

function searchPlayers() {
  const searchTerm = document.getElementById("player-search").value.trim();
  if (!searchTerm) {
    loadPlayers();
    return;
  }

  const filters = {
    search: searchTerm,
  };
  loadPlayers(1, filters);
}

function searchMatches() {
  const searchTerm = document.getElementById("match-search").value.trim();
  if (!searchTerm) {
    loadMatches();
    return;
  }

  const filters = {
    search: searchTerm,
  };
  loadMatches(1, filters);
}

// Data Management Functions
function showAddForm(type) {
  if (!isAuthenticated) {
    alert("You must be logged in to add new data.");
    showAuthModal();
    return;
  }

  const formModal = document.getElementById("form-modal");
  const formTitle = document.getElementById("form-modal-title");
  const formBody = document.getElementById("form-modal-body");

  formTitle.textContent = `Add New ${
    type.charAt(0).toUpperCase() + type.slice(1).replace("-", " ")
  }`;

  let formHTML = "";

  switch (type) {
    case "team":
      formHTML = `
        <form id="team-form">
          <div class="form-group">
            <label for="team-name">Name:</label>
            <input type="text" id="team-name" required>
          </div>
          <div class="form-group">
            <label for="team-city">City:</label>
            <input type="text" id="team-city" required>
          </div>
          <div class="form-group">
            <label for="team-abbreviation">Abbreviation:</label>
            <input type="text" id="team-abbreviation" required>
          </div>
          <div class="form-group">
            <label for="team-conference">Conference:</label>
            <select id="team-conference-form" required>
              <option value="Eastern">Eastern</option>
              <option value="Western">Western</option>
            </select>
          </div>
          <div class="form-group">
            <label for="team-division">Division:</label>
            <select id="team-division-form" required>
              <option value="Atlantic">Atlantic</option>
              <option value="Central">Central</option>
              <option value="Southeast">Southeast</option>
              <option value="Northwest">Northwest</option>
              <option value="Pacific">Pacific</option>
              <option value="Southwest">Southwest</option>
            </select>
          </div>
          <div class="form-group">
            <label for="team-logo">Logo URL:</label>
            <input type="url" id="team-logo">
          </div>
          <div class="form-actions">
            <button type="button" id="save-team" class="btn">Save</button>
            <button type="button" class="btn form-cancel">Cancel</button>
          </div>
        </form>
      `;
      break;
    case "player":
      formHTML = `
        <form id="player-form">
          <div class="form-group">
            <label for="player-first-name">First Name:</label>
            <input type="text" id="player-first-name" required>
          </div>
          <div class="form-group">
            <label for="player-last-name">Last Name:</label>
            <input type="text" id="player-last-name" required>
          </div>
          <div class="form-group">
            <label for="player-team-form">Team:</label>
            <select id="player-team-form" required>
              <!-- Teams will be loaded here -->
            </select>
          </div>
          <div class="form-group">
            <label for="player-position-form">Position:</label>
            <select id="player-position-form" required>
              <option value="PG">Point Guard</option>
              <option value="SG">Shooting Guard</option>
              <option value="SF">Small Forward</option>
              <option value="PF">Power Forward</option>
              <option value="C">Center</option>
            </select>
          </div>
          <div class="form-group">
            <label for="player-jersey">Jersey Number:</label>
            <input type="number" id="player-jersey" required>
          </div>
          <div class="form-group">
            <label for="player-height">Height (cm):</label>
            <input type="number" id="player-height" required>
          </div>
          <div class="form-group">
            <label for="player-weight">Weight (kg):</label>
            <input type="number" id="player-weight" required>
          </div>
          <div class="form-group">
            <label for="player-birth-date">Birth Date:</label>
            <input type="date" id="player-birth-date" required>
          </div>
          <div class="form-actions">
            <button type="button" id="save-player" class="btn">Save</button>
            <button type="button" class="btn form-cancel">Cancel</button>
          </div>
        </form>
      `;
      break;
    // Add other form types here
  }

  formBody.innerHTML = formHTML;

  // Add event listeners for form buttons
  if (type === "team") {
    document.getElementById("save-team").addEventListener("click", saveTeam);
  } else if (type === "player") {
    loadTeamDropdownForForm();
    document
      .getElementById("save-player")
      .addEventListener("click", savePlayer);
  }

  document.querySelectorAll(".form-cancel").forEach((btn) => {
    btn.addEventListener("click", () => {
      formModal.style.display = "none";
    });
  });

  formModal.style.display = "block";
}

async function loadTeamDropdownForForm() {
  const data = await fetchAPI("teams");
  const teams = data.results || [];
  const dropdown = document.getElementById("player-team-form");

  dropdown.innerHTML = "";

  teams.forEach((team) => {
    const option = document.createElement("option");
    option.value = team.id;
    option.textContent = team.name;
    dropdown.appendChild(option);
  });
}

async function saveTeam() {
  const name = document.getElementById("team-name").value;
  const city = document.getElementById("team-city").value;
  const abbreviation = document.getElementById("team-abbreviation").value;
  const conference = document.getElementById("team-conference-form").value;
  const division = document.getElementById("team-division-form").value;
  const logo = document.getElementById("team-logo").value;

  const teamData = {
    name,
    city,
    abbreviation,
    conference,
    division,
    logo,
  };

  try {
    const response = await postAPI("teams", teamData);

    if (response && response.id) {
      alert("Team added successfully!");
      document.getElementById("form-modal").style.display = "none";
      loadTeams();
    } else {
      alert("Failed to add team. Please try again.");
    }
  } catch (error) {
    console.error("Error saving team:", error);
    alert("Failed to add team. Please try again.");
  }
}

async function savePlayer() {
  const firstName = document.getElementById("player-first-name").value;
  const lastName = document.getElementById("player-last-name").value;
  const teamId = document.getElementById("player-team-form").value;
  const position = document.getElementById("player-position-form").value;
  const jerseyNumber = document.getElementById("player-jersey").value;
  const height = document.getElementById("player-height").value;
  const weight = document.getElementById("player-weight").value;
  const birthDate = document.getElementById("player-birth-date").value;

  const playerData = {
    first_name: firstName,
    last_name: lastName,
    team: teamId,
    position,
    jersey_number: jerseyNumber,
    height,
    weight,
    birth_date: birthDate,
    is_active: true,
  };

  try {
    const response = await postAPI("players", playerData);

    if (response && response.id) {
      alert("Player added successfully!");
      document.getElementById("form-modal").style.display = "none";
      loadPlayers();
    } else {
      alert("Failed to add player. Please try again.");
    }
  } catch (error) {
    console.error("Error saving player:", error);
    alert("Failed to add player. Please try again.");
  }
}

// Export Functions
async function exportData(type) {
  if (!isAuthenticated) {
    alert("You must be logged in to export data.");
    showAuthModal();
    return;
  }

  try {
    const data = await fetchAPI(type);
    const results = data.results || [];

    if (results.length === 0) {
      alert("No data to export.");
      return;
    }

    // Convert data to CSV
    const headers = Object.keys(results[0]).join(",");
    const rows = results.map((item) =>
      Object.values(item)
        .map((value) => {
          // Handle strings with commas by wrapping in quotes
          if (typeof value === "string" && value.includes(",")) {
            return `"${value}"`;
          }
          return value;
        })
        .join(",")
    );

    const csv = [headers, ...rows].join("\n");

    // Create download link
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${type}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  } catch (error) {
    console.error(`Error exporting ${type}:`, error);
    alert(`Failed to export ${type}. Please try again.`);
  }
}
