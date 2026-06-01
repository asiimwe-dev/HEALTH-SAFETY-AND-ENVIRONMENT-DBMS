<?php
declare(strict_types=1);

namespace App\Models;

use App\Core\Model;

class DashboardModel extends Model {
    /**
     * Get aggregate HSE metrics for the dashboard
     */
    public function getKpis(): array {
        $sql = "SELECT
          (SELECT COUNT(*) FROM incidents)                                         AS total_incidents,
          (SELECT COUNT(*) FROM incidents WHERE inc_status = 'Open')              AS open_incidents,
          (SELECT COUNT(*) FROM incidents WHERE incident_type = 'LTI')            AS total_lti,
          (SELECT COUNT(*) FROM incidents WHERE severity IN ('High','Critical'))   AS high_critical,
          (SELECT site_name FROM sites
           ORDER BY FIELD(hse_risk_category,'Critical','High','Medium','Low')
           LIMIT 1)                                                                AS highest_risk_site,
          ROUND(
            (SELECT COUNT(*) FROM employee_training WHERE cert_status='Valid')
            * 100.0 / NULLIF((SELECT COUNT(*) FROM employee_training), 0)
          , 1)                                                                     AS training_pct";
        
        $stmt = $this->db->query($sql);
        return $stmt->fetch();
    }

    /**
     * Get monthly incident trend data (Translation from app.py)
     */
    public function getMonthlyTrend(): array {
        $sql = "SELECT DATE_FORMAT(incident_date,'%Y-%m') AS month,
                       COUNT(*) AS total,
                       SUM(CASE WHEN severity = 'Critical' THEN 1 ELSE 0 END) AS critical,
                       SUM(CASE WHEN severity = 'High' THEN 1 ELSE 0 END) AS high
                FROM incidents
                WHERE incident_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY month
                ORDER BY month ASC";
        
        $stmt = $this->db->query($sql);
        return $stmt->fetchAll();
    }

    /**
     * Get incidents by site distribution
     */
    public function getSiteDistribution(): array {
        $sql = "SELECT s.site_name, COUNT(i.incident_id) AS incident_count
                FROM sites s
                LEFT JOIN incidents i ON s.site_id = i.site_id
                GROUP BY s.site_id
                ORDER BY incident_count DESC";
        
        $stmt = $this->db->query($sql);
        return $stmt->fetchAll();
    }

    /**
     * Get recent incidents for the feed
     */
    public function getRecentIncidents(int $limit = 5): array {
        $sql = "SELECT i.*, s.site_name 
                FROM incidents i 
                JOIN sites s ON i.site_id = s.site_id 
                ORDER BY i.incident_date DESC 
                LIMIT :limit";
        
        $stmt = $this->db->prepare($sql);
        $stmt->bindValue(':limit', $limit, \PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll();
    }
}
