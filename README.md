# HSE Management System — Uganda Oil & Gas Sector

<p align='left'>
  <img src='https://img.shields.io/badge/Version-2.1-blue?style=for-the-badge' alt='Version'>
  <img src='https://img.shields.io/badge/PHP-8.2+-777BB4?style=for-the-badge&logo=php&logoColor=white' alt='PHP'>
  <img src='https://img.shields.io/badge/MySQL-8.0+-00758F?style=for-the-badge&logo=mysql&logoColor=white' alt='MySQL'>
  <img src='https://img.shields.io/badge/Tailwind_CSS-3.0+-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white' alt='Tailwind'>
  <img src='https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge' alt='License'>
</p>

---

## 📄 Executive Summary
The **Health, Safety, and Environment (HSE) DBMS** is an enterprise-grade platform engineered to oversee HSE operations within Uganda's oil and gas sector (Tilenga, Kingfisher, and EACOP). Migrated from a Python prototype to a high-performance **PHP 8.2+ MVC architecture**, the system provides secure, real-time monitoring of safety metrics, incident management, and regulatory compliance.

## 🎯 Project Role: Problem & Solution

### The Problem
High-risk oil and gas operations require precise tracking of personnel, incidents, and certifications. Legacy systems often suffer from data fragmentation and slow reporting, increasing operational risk and regulatory non-compliance.

### The Solution
This digital command center automates HSE workflows. It features a high-density dashboard, a many-to-many training matrix, and a production-ready incident reporting system, all protected by modern web security standards.

## 🛠 Tech Stack (v2.1)

-   **Backend:** PHP 8.2+ (Strictly Typed)
-   **Architecture:** Custom MVC (Model-View-Controller)
-   **Frontend:** Tailwind CSS 3.0 & Chart.js
-   **Database:** MySQL 8.0+ (PDO with Prepared Statements)
-   **Security:** CSRF Protection, XSS Mitigation, and Session Management.

## 🚀 Getting Started

### 1. Prerequisites
-   PHP 8.2 or higher
-   MySQL Server 8.0+
-   Apache/Nginx (or use PHP built-in server for dev)

### 2. Installation
```bash
git clone https://github.com/asiimwe-dev/HEALTH-SAFETY-AND-ENVIRONMENT-DBMS.git
cd HEALTH-SAFETY-AND-ENVIRONMENT-DBMS/php
```

### 3. Database Setup
1. Create a MySQL database (e.g., `hse_db`).
2. Import the schema and sample data:
   ```bash
   mysql -u root -p hse_db < ../files/hse_db.sql
   ```
3. Update `php/config/config.php` with your database credentials.

### 4. Local Execution
```bash
php -S localhost:8000 -t public
```
Access the system at `http://localhost:8000`.

## 🔐 Access & Security
| Role | Username | Password |
| :--- | :--- | :--- |
| **HSE Administrator** | `admin` | `admin123` |
| **HSE Manager** | `gilbert` | `hse2025` |

## 📂 Project Layout
```text
php/
├── app/
│   ├── Controllers/    # Routing & Business Logic
│   ├── Models/         # Data Access Layer (PDO)
│   ├── Core/           # Framework Engine (Database, Base classes)
│   └── Views/          # UI Templates (Tailwind CSS)
├── config/             # App Configuration
├── public/             # Entry point & Assets
└── docs/               # Detailed Technical Documentation
```

## 📜 Documentation
Comprehensive guides are available in the [docs/](docs/) directory:
- [Architecture & Design](docs/ARCHITECTURE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Security Implementation](docs/SECURITY.md)
- [User Manual](docs/USER_MANUAL.md)

---
**Maintained by:** [Gilbert Asiimwe](https://github.com/asiimwe-dev)
