<?php
declare(strict_types=1);

namespace App\Models;

use App\Core\Model;

class TrainingModel extends Model {
    /**
     * Get the full training matrix with compliance status
     */
    public function getMatrix(array $filters = []): array {
        $sql = "SELECT
          CONCAT(e.first_name, ' ', e.last_name) AS employee_name,
          e.job_title,
          COALESCE(s.site_name, 'Unknown Site') AS site_name,
          tc.course_code,
          tc.course_name,
          tc.category,
          et.completion_date,
          et.expiry_date,
          et.certificate_number,
          et.score,
          et.cert_status,
          DATEDIFF(et.expiry_date, CURDATE()) AS days_until_expiry
        FROM employee_training et
          LEFT JOIN employees        e  ON et.employee_id = e.employee_id
          LEFT JOIN training_courses tc ON et.course_id   = tc.course_id
          LEFT JOIN sites            s  ON e.site_id      = s.site_id
        WHERE 1=1";

        $params = [];
        if (!empty($filters['status'])) {
            $sql .= " AND et.cert_status = :status";
            $params['status'] = $filters['status'];
        }
        if (!empty($filters['category'])) {
            $sql .= " AND tc.category = :category";
            $params['category'] = $filters['category'];
        }

        $sql .= " ORDER BY e.last_name, et.expiry_date";
        
        $stmt = $this->db->prepare($sql);
        $stmt->execute($params);
        return $stmt->fetchAll();
    }

    /**
     * Get aggregate training stats
     */
    public function getStats(): array {
        $sql = "SELECT
          COUNT(*)                                       AS total_records,
          SUM(cert_status='Valid')                       AS valid_certs,
          SUM(cert_status='Expired')                     AS expired_certs,
          ROUND(AVG(score),1)                            AS avg_score
        FROM employee_training";
        
        $stmt = $this->db->query($sql);
        return $stmt->fetch();
    }

    /**
     * Get course coverage data for charts
     */
    public function getCourseCoverage(): array {
        $sql = "SELECT tc.course_code, et.cert_status, COUNT(*) AS cnt
                FROM employee_training et
                JOIN training_courses tc ON et.course_id = tc.course_id
                GROUP BY tc.course_code, et.cert_status
                ORDER BY tc.course_code";
        
        $stmt = $this->db->query($sql);
        return $stmt->fetchAll();
    }

    /**
     * Get unique categories for filtering
     */
    public function getCategories(): array {
        $stmt = $this->db->query("SELECT DISTINCT category FROM training_courses ORDER BY category");
        return $stmt->fetchAll(\PDO::FETCH_COLUMN);
    }
}
