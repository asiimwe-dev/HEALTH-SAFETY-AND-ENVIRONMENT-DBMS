<?php
declare(strict_types=1);

namespace App\Core;

use PDO;

/**
 * Base Model
 * Provides common database operations
 */
abstract class Model {
    protected PDO $db;

    public function __construct() {
        $this->db = Database::getInstance();
    }
}
