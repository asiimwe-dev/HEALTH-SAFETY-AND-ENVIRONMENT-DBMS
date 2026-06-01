<?php
declare(strict_types=1);

namespace App\Core;

/**
 * Centralized Error and Exception Handler
 */
class ErrorHandler {
    public static function handleException(\Throwable $exception): void {
        $code = $exception->getCode() ?: 500;
        
        // Log the detailed error
        error_log(sprintf(
            "[%s] %s in %s on line %d",
            get_class($exception),
            $exception->getMessage(),
            $exception->getFile(),
            $exception->getLine()
        ));

        // Set HTTP response code
        if (!headers_sent()) {
            http_response_code((int)$code);
        }

        // Display user-friendly view
        if (defined('DEBUG') && DEBUG) {
            echo "<h1>Fatal Error</h1>";
            echo "<p>Message: " . htmlspecialchars($exception->getMessage()) . "</p>";
            echo "<pre>" . htmlspecialchars($exception->getTraceAsString()) . "</pre>";
        } else {
            // Production view
            $errorFile = APP_ROOT . '/app/Views/errors/500.php';
            if (file_exists($errorFile)) {
                include $errorFile;
            } else {
                echo "<h1>500 Internal Server Error</h1><p>A technical error occurred. Please try again later.</p>";
            }
        }
        exit;
    }

    public static function handleError(int $level, string $message, string $file, int $line): void {
        if (error_reporting() !== 0) {
            throw new \ErrorException($message, 0, $level, $file, $line);
        }
    }
}
