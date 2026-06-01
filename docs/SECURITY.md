# Security Implementation Guide

## 🔐 Core Security Principles
The HSE DBMS is built with "Security by Design" to protect sensitive oil and gas operational data.

### 1. SQL Injection Prevention
*   **Mechanism:** PHP Data Objects (PDO) with Prepared Statements.
*   **Implementation:** All user-supplied input is treated as data, never as executable code. Prepared statements ensure that malicious SQL strings cannot alter the intended query structure.
*   **Requirement:** Direct query concatenation is strictly forbidden.

### 2. Cross-Site Scripting (XSS) Mitigation
*   **Mechanism:** Robust Output Escaping.
*   **Implementation:** All data rendered in HTML templates is passed through `htmlspecialchars()`. This converts special characters (like `<` or `>`) into HTML entities, preventing malicious scripts from executing in the user's browser.
*   **Checklist:** Ensure all dynamic variables in `app/Views/` are escaped.

### 3. Cross-Site Request Forgery (CSRF) Protection
*   **Mechanism:** Synchronizer Token Pattern.
*   **Implementation:** 
    *   A unique, cryptographically secure token is generated per session.
    *   This token is embedded in all hidden form fields.
    *   The `Controller::validateCsrfToken()` method verifies the token on the server side before any `POST` or `PUT` request is processed.

### 4. Session & Authentication
*   **Secure Sessions:** Sessions are initialized with `session_start()` at the entry point.
*   **RBAC Placeholder:** The system currently supports roles (Admin, Manager, Officer). Permission checks can be added at the controller level using the `$_SESSION['user_role']` variable.
*   **Forced Logout:** The `logout()` method in `AuthController` explicitly clears and destroys the session to prevent session hijacking on shared workstations.

### 5. Error Masking
*   **Implementation:** Detailed system traces and database errors are intercepted by `ErrorHandler.php`.
*   **Production Behavior:** Users see a generic "Internal Server Error" page, while the specific technical details (including file paths and query fragments) are logged privately to the server.
