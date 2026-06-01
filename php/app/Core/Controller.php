<?php
declare(strict_types=1);

namespace App\Core;

/**
 * Base Controller
 * Loads models and views
 */
abstract class Controller {
    /**
     * Redirect to login if not authenticated
     */
    protected function requireAuth(): void {
        if (!isset($_SESSION['user_id'])) {
            header('Location: ' . URL_ROOT . '/auth');
            exit;
        }
    }

    /**
     * Load view template
     */
    protected function view(string $view, array $data = []): void {
        $file = APP_ROOT . "/app/Views/{$view}.php";
        if (file_exists($file)) {
            // Extract data to make variables available in the view
            extract($data);
            require_once $file;
        } else {
            throw new \RuntimeException("View {$view} not found.");
        }
    }

    /**
     * CSRF Protection
     */
    protected function generateCsrfToken(): string {
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    protected function validateCsrfToken(?string $token): bool {
        return !empty($token) && hash_equals($_SESSION['csrf_token'] ?? '', $token);
    }
}
