# Developer & In-Code Navigation Guide

## 🛠️ Code Standards
*   **PHP Version:** 8.2+
*   **Strict Typing:** Every core file must start with `declare(strict_types=1);`.
*   **Naming Conventions:** 
    *   Classes: `PascalCase`
    *   Methods/Properties: `camelCase`
    *   Filenames: Match Class names (PSR-4 compliant).

## 📂 Navigation Path

### Adding a New HSE Module
To add a new feature (e.g., "Equipment Inspection"):
1.  **Model:** Create `app/Models/InspectionModel.php` to handle SQL queries.
2.  **Controller:** Create `app/Controllers/InspectionsController.php`. Ensure the constructor calls `$this->requireAuth()`.
3.  **View:** Create `app/Views/inspections/index.php`.
4.  **Sidebar:** Add the new link to `app/Views/inc/header.php`.

### Working with the Database
Never use `mysqli_*` functions. Always use the `Database` singleton:
```php
$db = \App\Core\Database::getInstance();
$stmt = $db->prepare("SELECT * FROM table WHERE id = :id");
$stmt->execute(['id' => $val]);
```

### Form Security (CSRF)
All forms must include a CSRF token:
```html
<input type="hidden" name="csrf_token" value="<?= $csrf_token ?>">
```
And the controller must validate it:
```php
if (!$this->validateCsrfToken($_POST['csrf_token'])) { 
    throw new \RuntimeException("Security Error"); 
}
```

## 🔍 Debugging
*   **Local Logs:** Check `php/logs/` or the system error log for PHP fatal errors.
*   **Dev Mode:** Set `define('DEBUG', true);` in `config/config.php` to see full stack traces in the browser.
*   **SQL Errors:** Database exceptions are caught by `ErrorHandler.php` and masked in production to prevent data leakage.
