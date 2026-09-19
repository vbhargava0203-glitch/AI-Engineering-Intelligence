<div align="center">

# 🧠 AI Engineering Intelligence

**Turn GitHub engineering activity into actionable intelligence.**

A data-driven engineering analytics platform that analyzes GitHub repositories, stores engineering activity in PostgreSQL, and uses machine learning to estimate repository risk — all wrapped in an interactive Streamlit dashboard.

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#-license)

[Overview](#-what-it-does) •
[Features](#-key-features) •
[Architecture](#%EF%B8%8F-architecture) •
[Installation](#%EF%B8%8F-installation) •
[Usage](#-analyze-a-repository) •
[Dashboard](#%EF%B8%8F-dashboard-sections) •
[Roadmap](#-roadmap)

</div>

---

## 📖 Table of Contents

- [What It Does](#-what-it-does)
- [Key Features](#-key-features)
- [Architecture](#%EF%B8%8F-architecture)
- [Tech Stack](#%EF%B8%8F-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#%EF%B8%8F-installation)
- [Environment Variables](#-environment-variables)
- [Database](#%EF%B8%8F-database)
- [Analyze a Repository](#-analyze-a-repository)
- [Train the ML Model](#-train-the-ml-model)
- [Start the Dashboard](#-start-the-dashboard)
- [Dashboard Sections](#%EF%B8%8F-dashboard-sections)
- [End-to-End Workflow](#-end-to-end-workflow)
- [Project Goal](#-project-goal)
- [Roadmap](#-roadmap)
- [Disclaimer](#%EF%B8%8F-disclaimer)
- [Author](#-author)

---

## 🚀 What It Does

AI Engineering Intelligence lets you enter a public GitHub repository URL and automatically collects engineering data such as:

| Metric | Description |
|---|---|
| ⭐ Stars | Community interest signal |
| 🍴 Forks | Reuse and adoption signal |
| 🐛 Open Issues | Outstanding work / bug backlog |
| 👥 Contributors | Size of the engineering footprint |
| 📝 Commits | Development velocity |
| 🔀 Pull Requests | Collaboration and review activity |
| 📌 Issues | Tracked work items |
| 💻 Primary Language | Technology fingerprint |

The collected data is persisted in **PostgreSQL** and exposed through an interactive **Streamlit dashboard**. A machine learning layer then classifies each repository into a risk tier:

<div align="center">

| 🟢 LOW | 🟡 MEDIUM | 🔴 HIGH |
|:---:|:---:|:---:|
| Healthy engineering signals | Some areas worth watching | Elevated attention needed |

</div>

---

## ✨ Key Features

### 🔍 GitHub Repository Analyzer
Enter a repository URL and the analyzer pulls repository metadata, contributors, recent commits, pull requests, and issues straight from the GitHub API.

```text
https://github.com/username/repository
```

### 🗄️ PostgreSQL Data Pipeline
Repository and engineering activity data is persisted in relational tables:

- Repositories
- Contributors
- Commits
- Pull Requests
- Issues
- Daily Metrics
- Risk Predictions

### 📊 Engineering Dashboard
The Streamlit dashboard surfaces:

- Executive overview
- Repository statistics
- Engineering activity
- Code churn
- Risk distribution
- Repository comparison
- Risk scores
- ML prediction details

### 🤖 ML-Powered Risk Analysis
The machine learning component processes engineering metrics and produces a repository risk score and risk category, made easier to interpret through charts and repository-level breakdowns.

### 📈 Interactive Visualizations
Built with Plotly:

- Commit activity
- Risk distribution
- Repository risk scores
- Engineering activity vs. risk
- Code churn

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     GitHub API        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Repository Analyzer   │
                    │       (Python)        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      PostgreSQL       │
                    │       Database        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
      ┌────────────────────┐       ┌────────────────────┐
      │    Engineering      │       │   ML Risk           │
      │      Metrics        │       │   Prediction        │
      └─────────┬──────────┘       └─────────┬──────────┘
                │                            │
                └─────────────┬──────────────┘
                              ▼
                    ┌──────────────────────┐
                    │  Streamlit Dashboard  │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and data pipeline |
| **GitHub REST API** | Repository data collection |
| **PostgreSQL** | Relational data storage |
| **Pandas** | Data processing |
| **Scikit-learn** | Machine learning |
| **Joblib** | ML model persistence |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Dashboard and UI |
| **python-dotenv** | Environment configuration |
| **Requests** | GitHub API requests |

---

## 📁 Project Structure

```text
AI-Engineering-Intelligence/
│
├── backend/
│
├── dashboard/
│   └── app.py
│
├── data_pipeline/
│   ├── github_client.py
│   ├── repository_analyzer.py
│   ├── repository_list.py
│   ├── collect_repositories.py
│   ├── collect_commits.py
│   ├── collect_pull_requests.py
│   ├── collect_issues.py
│   ├── collect_activity.py
│   ├── metrics.py
│   └── etl.py
│
├── database/
│   └── test_connection.py
│
├── ml/
│   ├── prepare_data.py
│   ├── train_model.py
│   ├── predict.py
│   ├── data/
│   │   └── training_data.csv
│   └── models/
│
├── scripts/
├── tests/
│
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/vbhargava0203-glitch/AI-Engineering-Intelligence.git
cd AI-Engineering-Intelligence
```

### 2. Create a virtual environment

**Windows**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

> If PowerShell blocks activation:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> venv\Scripts\Activate.ps1
> ```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pandas requests python-dotenv psycopg2-binary streamlit plotly scikit-learn joblib
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/engineering_intelligence
```

> ⚠️ **Never commit your `.env` file or GitHub token.**
> Make sure `.gitignore` contains:
> ```text
> .env
> venv/
> __pycache__/
> *.pyc
> ```

---

## 🗄️ Database

The project uses a PostgreSQL database named `engineering_intelligence` with the following core tables:

```text
repositories
contributors
commits
pull_requests
issues
daily_metrics
risk_predictions
```

Verify your PostgreSQL connection:

```bash
python database/test_connection.py
```

---

## 🧪 Analyze a Repository

Run the repository analyzer:

```bash
python data_pipeline/repository_analyzer.py
```

When prompted, enter a public repository URL:

```text
Enter GitHub repository URL:
> https://github.com/vbhargava0203-glitch/CartShare
```

or:

```text
> https://github.com/vbhargava0203-glitch/snake-arcade-remastered
```

The analyzer collects the repository's engineering data and saves it to PostgreSQL.

---

## 🤖 Train the ML Model

```bash
# 1. Prepare the training data
python ml/prepare_data.py

# 2. Train the model (saved to ml/models/)
python ml/train_model.py

# 3. Run prediction
python ml/predict.py
```

---

## 📊 Start the Dashboard

From the project root:

```bash
python -m streamlit run dashboard/app.py
```

Then open the local URL shown in the terminal — usually:

```text
http://localhost:8501
```

---

## 🖥️ Dashboard Sections

### Executive Overview
A high-level view of the engineering ecosystem — total repositories, stars, commits, pull requests, issues, contributors, risk distribution, most active repositories, and highest-risk repositories.

### Repository Intelligence
Drill into an individual repository — stars, forks, open issues, language, commits, pull requests, issues, contributors, code churn, ML risk score, and risk level.

### Risk Analysis
Compare repositories side by side — risk scores, risk levels, commit activity, issue activity, and engineering activity vs. risk.

---

## 🔄 End-to-End Workflow

```text
1. Enter GitHub repository URL
            ↓
2. GitHub API retrieves repository data
            ↓
3. Python data pipeline processes the data
            ↓
4. PostgreSQL stores the engineering data
            ↓
5. Metrics are calculated
            ↓
6. ML model generates repository risk
            ↓
7. Streamlit loads the data
            ↓
8. Interactive engineering dashboard
```

---

## 🎯 Project Goal

The goal of AI Engineering Intelligence is to explore how software engineering activity can be transformed into measurable engineering intelligence — turning isolated GitHub numbers into signals that answer questions like:

- Which repositories are most active?
- How much engineering activity is happening?
- How large is the contributor footprint?
- What is the code churn?
- Which repositories may require additional attention?
- Can engineering activity be used to estimate repository risk?

---

## 📌 Roadmap

**Implemented**

- [x] GitHub repository analysis & API integration
- [x] PostgreSQL integration & repository storage
- [x] Contributor, commit, pull request & issue collection
- [x] Engineering metrics pipeline
- [x] ML risk prediction pipeline
- [x] Streamlit dashboard with interactive repository selection
- [x] Risk visualization & repository comparison

**Planned**

- [ ] More historical engineering metrics
- [ ] Improved ML model validation
- [ ] More repository health indicators
- [ ] Automated scheduled data collection
- [ ] Trend analysis over time
- [ ] Authentication and multi-user support
- [ ] Cloud deployment
- [ ] Advanced engineering recommendations

---

## ⚠️ Disclaimer

The repository risk score is an analytical prediction produced by this project's machine learning pipeline. It should be treated as an **engineering intelligence signal**, not as a definitive assessment of software quality or project health.

---

## 👨‍💻 Author

**Bhargava Vagathuri**

Built as a project exploring **Data Engineering + Machine Learning + Software Engineering Analytics + AI**.

---

<div align="center">

### ⭐ If You Find This Interesting

If this project helps or inspires you, consider giving the repository a star and following the development journey.

[![GitHub stars](https://img.shields.io/github/stars/vbhargava0203-glitch/AI-Engineering-Intelligence?style=social)](https://github.com/vbhargava0203-glitch/AI-Engineering-Intelligence)

</div>
