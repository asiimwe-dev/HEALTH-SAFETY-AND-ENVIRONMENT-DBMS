<?php
declare(strict_types=1);

namespace App\Core;

use PDO;
use PDOException;
use RuntimeException;

/**
 * Database Wrapper (Singleton Pattern)
 * Handles fail-safe PDO connection logic.
 */
class Database {
    private static ?PDO $instance = null;

    public static function getInstance(): PDO {
        if (self::$instance === null) {
            $dsn = sprintf(
                "mysql:host=%s;dbname=%s;charset=%s",
                DB_HOST,
                DB_NAME,
                DB_CHARSET
            );

            $options = [
                PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES   => false,
            ];

            try {
                self::$instance = new PDO($dsn, DB_USER, DB_PASS, $options);
            } catch (PDOException $e) {
                // Log error internally and show generic message to user
                error_log("Database Connection Error: " . $e->getMessage());
                throw new RuntimeException("A technical error occurred while connecting to the database.");
            }
        }

        return self::$instance;
    }

    /**
     * Prevent cloning and serialization
     */
    private function __construct() {}
    private function __clone() {}
}
