# 🧠 AI Engineering Intelligence

> **Turn GitHub engineering activity into actionable intelligence.**

AI Engineering Intelligence is a data-driven engineering analytics platform that analyzes GitHub repositories, stores engineering activity in PostgreSQL, and uses machine learning to estimate repository risk.

The project combines **GitHub API + Python + PostgreSQL + Data Engineering + Machine Learning + Streamlit** into a single interactive dashboard.

---

## 🚀 What It Does

The platform allows you to enter a public GitHub repository URL and automatically collect engineering data such as:

- ⭐ Repository stars
- 🍴 Forks
- 🐛 Open issues
- 👥 Contributors
- 📝 Commits
- 🔀 Pull requests
- 📌 Issues
- 💻 Primary programming language

The collected data is stored in **PostgreSQL** and exposed through an interactive **Streamlit dashboard**.

The ML layer uses engineering activity data to classify repositories into risk levels such as:

- 🟢 **LOW**
- 🟡 **MEDIUM**
- 🔴 **HIGH**

---

## ✨ Key Features

### 🔍 GitHub Repository Analyzer

Enter a GitHub repository URL and automatically analyze the repository through the GitHub API.

Example:

```text
https://github.com/username/repository
```

The analyzer collects repository information, contributors, recent commits, pull requests, and issues.

### 🗄️ PostgreSQL Data Pipeline

Repository and engineering activity data is persisted in PostgreSQL.

The project uses relational tables for:

- Repositories
- Contributors
- Commits
- Pull Requests
- Issues
- Daily Metrics
- Risk Predictions

### 📊 Engineering Dashboard

The Streamlit dashboard provides:

- Executive overview
- Repository statistics
- Engineering activity
- Code churn
- Risk distribution
- Repository comparison
- Risk scores
- ML prediction details

### 🤖 ML-Powered Risk Analysis

The machine learning component processes engineering metrics and produces a repository risk score and risk category.

The dashboard makes the prediction easier to understand through charts and repository-level analysis.

### 📈 Interactive Visualizations

Plotly is used to visualize:

- Commit activity
- Risk distribution
- Repository risk scores
- Engineering activity vs. risk
- Code churn

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │     GitHub API       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Repository Analyzer  │
                    │      Python          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     PostgreSQL       │
                    │      Database        │
                    └──────────┬───────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
      ┌────────────────────┐       ┌────────────────────┐
      │ Engineering        │       │ ML Risk Prediction │
      │ Metrics            │       │                    │
      └─────────┬──────────┘       └─────────┬──────────┘
                │                            │
                └─────────────┬──────────────┘
                              ▼
                    ┌──────────────────────┐
                    │  Streamlit Dashboard │
                    └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and data pipeline |
| GitHub REST API | Repository data collection |
| PostgreSQL | Relational data storage |
| Pandas | Data processing |
| Scikit-learn | Machine learning |
| Joblib | ML model persistence |
| Plotly | Interactive visualizations |
| Streamlit | Dashboard and UI |
| python-dotenv | Environment configuration |
| Requests | GitHub API requests |

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
│
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
git clone https://github.com/YOUR_USERNAME/AI-Engineering-Intelligence.git
cd AI-Engineering-Intelligence
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install pandas requests python-dotenv psycopg2-binary streamlit plotly scikit-learn joblib
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root.

```env
GITHUB_TOKEN=your_github_token
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/engineering_intelligence
```

### Important

Do **not** commit your `.env` file or GitHub token to GitHub.

Make sure `.gitignore` contains:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## 🗄️ Database

The project uses PostgreSQL with a database named:

```text
engineering_intelligence
```

The main data model contains tables such as:

```text
repositories
contributors
commits
pull_requests
issues
daily_metrics
risk_predictions
```

You can verify your PostgreSQL connection using:

```bash
python database/test_connection.py
```

---

## 🧪 Analyze a Repository

Run the repository analyzer:

```bash
python data_pipeline/repository_analyzer.py
```

When prompted:

```text
Enter GitHub repository URL:
```

Enter a public repository URL:

```text
https://github.com/vbhargava0203-glitch/CartShare
```

or:

```text
https://github.com/vbhargava0203-glitch/snake-arcade-remastered
```

The analyzer will collect GitHub engineering information and save the repository data to PostgreSQL.

---

## 🤖 Train the ML Model

Prepare the training data:

```bash
python ml/prepare_data.py
```

Train the model:

```bash
python ml/train_model.py
```

The trained model is stored under:

```text
ml/models/
```

Then run prediction:

```bash
python ml/predict.py
```

---

## 📊 Start the Dashboard

From the project root:

```bash
python -m streamlit run dashboard/app.py
```

Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

---

## 🖥️ Dashboard Sections

### Executive Overview

Provides a high-level view of the engineering ecosystem:

- Total repositories
- GitHub stars
- Commits
- Pull requests
- Issues
- Contributors
- Risk distribution
- Most active repositories
- Highest-risk repositories

### Repository Intelligence

Select an individual repository to inspect:

- Stars
- Forks
- Open issues
- Language
- Commits
- Pull requests
- Issues
- Contributors
- Code churn
- ML risk score
- Risk level

### Risk Analysis

Compare repositories using:

- Risk scores
- Risk levels
- Commit activity
- Issue activity
- Engineering activity vs. risk

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

The goal of AI Engineering Intelligence is to explore how software engineering activity can be transformed into measurable engineering intelligence.

Instead of looking at GitHub activity as isolated numbers, the platform attempts to answer questions such as:

- Which repositories are most active?
- How much engineering activity is happening?
- How large is the contributor footprint?
- What is the code churn?
- Which repositories may require additional attention?
- Can engineering activity be used to estimate repository risk?

---

## 📌 Current Status

### Implemented

- [x] GitHub repository analysis
- [x] GitHub API integration
- [x] PostgreSQL integration
- [x] Repository storage
- [x] Contributor collection
- [x] Commit collection
- [x] Pull request collection
- [x] Issue collection
- [x] Engineering metrics
- [x] ML risk prediction pipeline
- [x] Streamlit dashboard
- [x] Interactive repository selection
- [x] Risk visualization
- [x] Repository comparison

### Planned Improvements

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

The repository risk score is an analytical prediction produced by the project's machine learning pipeline. It should be treated as an engineering intelligence signal, not as a definitive assessment of software quality or project health.

---

## 👨‍💻 Author

**Bhargava Vagathuri**

Built as a project exploring:

**Data Engineering + Machine Learning + Software Engineering Analytics + AI**

---

## ⭐ If You Find This Interesting

If this project helps or inspires you, consider giving the repository a ⭐ and following the development journey.
