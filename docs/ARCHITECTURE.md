# System Architecture & Design

## 🏗️ Overview
The HSE Management System follows a custom-built **Model-View-Controller (MVC)** architectural pattern. This separation of concerns ensures the application is modular, testable, and easy to maintain.

### 1. The Core Engine (`app/Core/`)
*   **`Database.php`**: A Singleton wrapper for PDO. It ensures only one database connection is active per request and handles connection-level error logging.
*   **`Controller.php`**: The base class for all controllers. It provides methods for rendering views (`view()`) and security utilities like `requireAuth()` and CSRF token management.
*   **`Model.php`**: The base class for all models, providing the shared PDO instance (`$this->db`) for data access.
*   **`ErrorHandler.php`**: A centralized interceptor for all PHP Exceptions and Errors. It logs detailed technical data while displaying a polished UI to the user.

### 2. Controller Layer (`app/Controllers/`)
Controllers handle the orchestration of the request. They:
1. Validate authentication.
2. Interact with one or more Models to fetch data.
3. Pass structured data to the appropriate View.
4. Handle form submissions and redirects.

### 3. Model Layer (`app/Models/`)
Models contain all SQL logic. They utilize strictly parameterized prepared statements (via PDO) to protect against injection attacks. Key models include:
*   `IncidentsModel`: Complex joins for incident reporting and historical logs.
*   `TrainingModel`: Logic for many-to-many relationships between employees and certifications.
*   `DashboardModel`: Aggregation queries for real-time KPI generation.

### 4. View Layer (`app/Views/`)
Views are clean PHP templates focusing on markup and UI presentation.
*   **Framework**: Tailwind CSS 3.0 for responsive design.
*   **Components**: Reusable `header.php` and `footer.php` ensure a consistent "Command Center" layout across all modules.
*   **Visualization**: Chart.js for interactive performance trends.

---

## 🛣️ Routing Logic
The application uses a **Front Controller** pattern.
1. All requests are sent to `public/index.php` via `.htaccess`.
2. The router parses the URL (e.g., `/incidents/create`).
3. It maps the first part to a Controller (`IncidentsController`) and the second to a method (`create()`).
4. If no session exists, the router automatically redirects to the `AuthController`.
