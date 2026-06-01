<?php
declare(strict_types=1);

namespace App\Controllers;

use App\Core\Controller;
use App\Models\IncidentsModel;

class IncidentsController extends Controller {
    private IncidentsModel $incidentsModel;

    public function __construct() {
        $this->requireAuth();
        $this->incidentsModel = new IncidentsModel();
    }

    /**
     * List all incidents
     */
    public function index(): void {
        $filters = [
            'site_id' => $_GET['site_id'] ?? null,
            'severity' => $_GET['severity'] ?? null,
            'status' => $_GET['status'] ?? null
        ];

        $incidents = $this->incidentsModel->getAll($filters);
        $sites = $this->incidentsModel->getSites();

        $data = [
            'title' => 'Incident Register | HSE System',
            'activePage' => 'incidents',
            'incidents' => $incidents,
            'sites' => $sites,
            'filters' => $filters,
            'flash' => $_SESSION['flash_message'] ?? null
        ];
        unset($_SESSION['flash_message']);

        $this->view('incidents/index', $data);
    }

    /**
     * Show form to report a new incident
     */
    public function create(): void {
        $sites = $this->incidentsModel->getSites();
        $employees = $this->incidentsModel->getEmployees();

        // Debug check: If sites or employees are empty, there might be a DB import issue
        if (empty($sites) || empty($employees)) {
            error_log("HSE Warning: Sites or Employees table is empty. Check DB import.");
        }

        $data = [
            'title' => 'Report Incident | HSE System',
            'activePage' => 'report',
            'sites' => $sites,
            'employees' => $employees,
            'csrf_token' => $this->generateCsrfToken()
        ];

        $this->view('incidents/create', $data);
    }

    /**
     * Handle incident submission
     */
    public function store(): void {
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            header('Location: ' . URL_ROOT . '/incidents/create');
            exit;
        }

        if (!$this->validateCsrfToken($_POST['csrf_token'] ?? '')) {
            throw new \RuntimeException("CSRF token validation failed.");
        }

        // Basic validation
        $errors = [];
        if (empty($_POST['description']) || strlen($_POST['description']) < 30) {
            $errors['description'] = "Description must be at least 30 characters.";
        }

        if (empty($errors)) {
            $incidentDate = $_POST['incident_date'] . ' ' . ($_POST['incident_time'] ?: '00:00:00');
            
            $saveData = [
                'incident_date' => $incidentDate,
                'site_id' => $_POST['site_id'],
                'reported_by' => $_POST['reported_by'],
                'involved_employee_id' => !empty($_POST['involved_employee_id']) ? $_POST['involved_employee_id'] : null,
                'incident_type' => $_POST['incident_type'],
                'severity' => $_POST['severity'],
                'description' => htmlspecialchars($_POST['description']),
                'root_cause' => $_POST['root_cause'],
                'immediate_action' => htmlspecialchars($_POST['immediate_action'] ?? ''),
                'corrective_action' => htmlspecialchars($_POST['corrective_action'] ?? '')
            ];

            if ($this->incidentsModel->create($saveData)) {
                $_SESSION['flash_message'] = "Incident successfully reported.";
                header('Location: ' . URL_ROOT . '/incidents');
                exit;
            } else {
                $errors['db'] = "Failed to save incident. Please try again.";
            }
        }

        // If we reach here, there were errors
        $sites = $this->incidentsModel->getSites();
        $employees = $this->incidentsModel->getEmployees();
        $this->view('incidents/create', [
            'title' => 'Report Incident | HSE System',
            'activePage' => 'report',
            'sites' => $sites,
            'employees' => $employees,
            'errors' => $errors,
            'old' => $_POST,
            'csrf_token' => $_POST['csrf_token'] // Keep the same token for the retry
        ]);
    }
}
