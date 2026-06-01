<?php
declare(strict_types=1);

require_once __DIR__ . '/../config/config.php';

// Autoloader (Simple PSR-4 implementation)
spl_autoload_register(function ($class) {
    $prefix = 'App\\';
    $base_dir = APP_ROOT . '/app/';
    
    $len = strlen($prefix);
    if (strncmp($prefix, $class, $len) !== 0) {
        return;
    }

    $relative_class = substr($class, $len);
    $file = $base_dir . str_replace('\\', '/', $relative_class) . '.php';

    if (file_exists($file)) {
        require $file;
    }
});

use App\Core\ErrorHandler;

// Set error handlers
set_exception_handler([ErrorHandler::class, 'handleException']);
set_error_handler([ErrorHandler::class, 'handleError']);

// Ensure session starts before any routing logic
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Simple Router
// If running via 'php -S', we need to handle the REQUEST_URI manually
$url = $_GET['url'] ?? '';
if (empty($url)) {
    $requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
    $url = trim($requestUri, '/');
}

$parts = explode('/', $url);

// Check if we are at the root or explicitly at 'auth'
if (empty($url) || $url === 'index.php') {
    if (isset($_SESSION['user_id'])) {
        header('Location: ' . URL_ROOT . '/dashboard');
    } else {
        header('Location: ' . URL_ROOT . '/auth');
    }
    exit;
}

$controllerName = !empty($parts[0]) ? ucfirst($parts[0]) . 'Controller' : 'AuthController';
$methodName = $parts[1] ?? 'index';

$controllerClass = "App\\Controllers\\{$controllerName}";

if (class_exists($controllerClass)) {
    $controller = new $controllerClass();
    if (method_exists($controller, $methodName)) {
        call_user_func_array([$controller, $methodName], array_slice($parts, 2));
    } else {
        throw new \RuntimeException("Method {$methodName} not found in {$controllerName}.");
    }
} else {
    http_response_code(404);
    echo "404 - Page Not Found: " . htmlspecialchars($controllerClass);
}
