# HSE Management System — Uganda Oil & Gas Sector

<p align='left'>
  <img src='https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge' alt='Version'>
  <img src='https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python' alt='Python'>
  <img src='https://img.shields.io/badge/MySQL-8.0+-00758F?style=for-the-badge&logo=mysql&logoColor=white' alt='MySQL'>
  <img src='https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white' alt='Streamlit'>
  <img src='https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge' alt='License'>
</p>

---

## 📄 Executive Summary
The **Health, Safety, and Environment (HSE) DBMS** is a production-grade database management system engineered to oversee HSE operations within Uganda's burgeoning oil and gas sector. Specifically designed for the **Albertine Graben** (Tilenga, Kingfisher, and EACOP projects), the system provides a centralized platform for real-time monitoring of safety metrics, incident management, and regulatory compliance.

## 🎯 Project Role: Problem & Solution

### The Problem
Managing HSE data in multi-site, high-risk oil and gas operations often suffers from fragmented tracking, delayed incident reporting, and certification lapses. These inefficiencies increase the risk of workplace accidents and lead to non-compliance with stringent regulatory standards (NEMA, PAU, OPITO), potentially resulting in heavy fines and operational shutdowns.

### The Solution
This DBMS provides an integrated digital solution that automates the tracking of personnel, incidents, and training certifications. By centralizing data into a high-performance, interactive dashboard, it empowers safety officers with real-time insights, automated expiry alerts, and comprehensive audit trails, ensuring that all operations meet both local and international safety benchmarks.

## 🛠 Tech Stack & Implementation

### Core Technologies
- **Frontend:** [Streamlit](https://streamlit.io/) — Interactive UI with a custom production-grade CSS design system.
- **Backend:** [Python 3](https://www.python.org/) — Business logic and data processing.
- **Database:** [MySQL 8.0+](https://www.mysql.com/) — Relational storage with optimized indexing and referential integrity.
- **Data Analysis:** [Pandas](https://pandas.pydata.org/) & [Plotly](https://plotly.com/) — Real-time KPI visualization and trend analysis.

### Implementation Highlights
- **Normalized Schema:** 7+ tables with M:N relationships for robust data integrity.
- **Performance Optimized:** 20+ database indexes ensuring sub-50ms query response times.
- **Responsive Design:** Mobile-first architecture with semantic CSS variables.
- **Secure Integration:** Environment-based configuration for sensitive database credentials.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher
- MySQL Server 8.0+
- Git

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/asiimwe-dev/HEALTH-SAFETY-AND-ENVIRONMENT-DBMS.git
cd HEALTH-SAFETY-AND-ENVIRONMENT-DBMS

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r files/requirements.txt
```

### 3. Database Setup
1. Create a MySQL database (e.g., `hse_db`).
2. Import the production schema:
   ```bash
   mysql -u [username] -p hse_db < files/hse_db.sql
   ```
3. Configure your credentials in a `.env` file or export them:
   ```bash
   export HSE_DB_HOST='localhost'
   export HSE_DB_USER='your_user'
   export HSE_DB_PASS='your_password'
   export HSE_DB_NAME='hse_db'
   ```

### 4. Execution
```bash
streamlit run files/app.py
```

## 📂 Project Layout
```text
├── docs/                # Technical documentation and deployment guides
├── files/               # Core application source code
│   ├── app.py           # Main Streamlit application entry point
│   ├── hse_db.sql       # Relational database schema with sample data
│   └── requirements.txt # Python dependency list
├── .gitignore           # Version control exclusion rules
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

## 📜 License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software for both commercial and non-commercial purposes. See the `LICENSE` file for full details.

## 🤝 Contributing
Contributions are welcome and greatly appreciated! To contribute:
1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`).
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4. **Push** to the branch (`git push origin feature/AmazingFeature`).
5. **Open** a Pull Request.

Please ensure your code adheres to the project's coding standards and includes appropriate documentation or tests.

---
**Maintained by:** [Gilbert Asiimwe](https://github.com/asiimwe-dev) | Mbarara University of Science and Technology

