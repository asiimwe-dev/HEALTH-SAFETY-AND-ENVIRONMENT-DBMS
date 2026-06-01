<?php
declare(strict_types=1);

namespace App\Models;

use App\Core\Model;

class IncidentsModel extends Model {
    /**
     * Get all incidents with site and employee details
     */
    public function getAll(array $filters = []): array {
        // Use LEFT JOIN to ensure incidents show even if site/employee records have issues
        $sql = "SELECT i.*, 
                       COALESCE(s.site_name, 'Unknown Site') AS site_name, 
                       COALESCE(s.district, 'N/A') AS district, 
                       COALESCE(CONCAT(rep.first_name, ' ', rep.last_name), 'Unknown Reporter') AS reporter_name,
                       COALESCE(CONCAT(inv.first_name, ' ', inv.last_name), '—') AS involved_name
                FROM incidents i
                LEFT JOIN sites s ON i.site_id = s.site_id
                LEFT JOIN employees rep ON i.reported_by = rep.employee_id
                LEFT JOIN employees inv ON i.involved_employee_id = inv.employee_id
                WHERE 1=1";
        
        $params = [];
        if (!empty($filters['site_id'])) {
            $sql .= " AND i.site_id = :site_id";
            $params['site_id'] = $filters['site_id'];
        }
        if (!empty($filters['severity'])) {
            $sql .= " AND i.severity = :severity";
            $params['severity'] = $filters['severity'];
        }
        if (!empty($filters['status'])) {
            $sql .= " AND i.inc_status = :status";
            $params['status'] = $filters['status'];
        }

        $sql .= " ORDER BY i.incident_date DESC";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll();
    }

    /**
     * Get a single incident by ID
     */
    public function getById(int $id): ?array {
        $sql = "SELECT i.*, s.site_name, s.district, 
                       CONCAT(rep.first_name, ' ', rep.last_name) AS reporter_name,
                       COALESCE(CONCAT(inv.first_name, ' ', inv.last_name), '—') AS involved_name
                FROM incidents i
                LEFT JOIN sites s ON i.site_id = s.site_id
                LEFT JOIN employees rep ON i.reported_by = rep.employee_id
                LEFT JOIN employees inv ON i.involved_employee_id = inv.employee_id
                WHERE i.incident_id = :id";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute(['id' => $id]);
        $result = $stmt->fetch();
        return $result ?: null;
    }

    /**
     * Insert a new incident
     */
    public function create(array $data): bool {
        $sql = "INSERT INTO incidents 
                (incident_date, site_id, reported_by, involved_employee_id, incident_type, 
                 severity, description, root_cause, immediate_action, corrective_action, inc_status)
                VALUES 
                (:incident_date, :site_id, :reported_by, :involved_employee_id, :incident_type, 
                 :severity, :description, :root_cause, :immediate_action, :corrective_action, 'Open')";
        
        $stmt = $this->db->prepare($sql);
        return $stmt->execute([
            'incident_date' => $data['incident_date'],
            'site_id' => $data['site_id'],
            'reported_by' => $data['reported_by'],
            'involved_employee_id' => $data['involved_employee_id'],
            'incident_type' => $data['incident_type'],
            'severity' => $data['severity'],
            'description' => $data['description'],
            'root_cause' => $data['root_cause'],
            'immediate_action' => $data['immediate_action'],
            'corrective_action' => $data['corrective_action']
        ]);
    }

    /**
     * Get all active sites for dropdowns
     */
    public function getSites(): array {
        $stmt = $this->db->query("SELECT site_id, site_name FROM sites ORDER BY site_name");
        return $stmt->fetchAll();
    }

    /**
     * Get all active employees for dropdowns
     */
    public function getEmployees(): array {
        $stmt = $this->db->query("SELECT employee_id, CONCAT(first_name, ' ', last_name) AS name, job_title FROM employees ORDER BY last_name");
        return $stmt->fetchAll();
    }
}
