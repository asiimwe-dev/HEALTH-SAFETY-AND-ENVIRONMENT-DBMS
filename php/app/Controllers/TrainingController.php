<?php
declare(strict_types=1);

namespace App\Controllers;

use App\Core\Controller;
use App\Models\TrainingModel;

class TrainingController extends Controller {
    private TrainingModel $trainingModel;

    public function __construct() {
        $this->requireAuth();
        $this->trainingModel = new TrainingModel();
    }

    public function index(): void {
        $filters = [
            'status' => $_GET['status'] ?? null,
            'category' => $_GET['category'] ?? null
        ];

        $matrix = $this->trainingModel->getMatrix($filters);
        $stats = $this->trainingModel->getStats();
        $categories = $this->trainingModel->getCategories();
        $courseCoverage = $this->trainingModel->getCourseCoverage();

        $data = [
            'title' => 'Training Matrix | HSE System',
            'activePage' => 'training',
            'matrix' => $matrix,
            'stats' => $stats,
            'categories' => $categories,
            'courseCoverage' => $courseCoverage,
            'filters' => $filters
        ];

        $this->view('training/index', $data);
    }
}
