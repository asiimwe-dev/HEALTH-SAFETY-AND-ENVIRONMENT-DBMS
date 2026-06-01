<?php
declare(strict_types=1);

namespace App\Controllers;

use App\Core\Controller;

class AuthController extends Controller {
    /**
     * Show Login Page
     */
    public function index(): void {
        if (isset($_SESSION['user_id'])) {
            header('Location: ' . URL_ROOT . '/dashboard');
            exit;
        }
        $this->view('auth/login', ['title' => 'Sign In | HSE System']);
    }

    /**
     * Handle Login Request
     */
    public function login(): void {
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            // Mock authentication based on the Python project's USERS
            $username = $_POST['username'] ?? '';
            $password = $_POST['password'] ?? '';

            $users = [
                'admin' => ['name' => 'Admin User', 'role' => 'HSE Administrator', 'pass' => 'admin123'],
                'gilbert' => ['name' => 'Gilbert', 'role' => 'HSE Manager', 'pass' => 'hse2025']
            ];

            if (isset($users[$username]) && $users[$username]['pass'] === $password) {
                $_SESSION['user_id'] = $username;
                $_SESSION['user_name'] = $users[$username]['name'];
                $_SESSION['user_role'] = $users[$username]['role'];
                header('Location: ' . URL_ROOT . '/dashboard');
                exit;
            } else {
                $this->view('auth/login', [
                    'title' => 'Sign In | HSE System',
                    'error' => 'Invalid username or password.'
                ]);
            }
        }
    }

    /**
     * Handle Logout
     */
    public function logout(): void {
        session_unset();
        session_destroy();
        header('Location: ' . URL_ROOT . '/auth');
        exit;
    }
}
