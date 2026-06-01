<?php
declare(strict_types=1);

namespace App\Controllers;

use App\Core\Controller;
use App\Models\DashboardModel;

class DashboardController extends Controller {
    private DashboardModel $dashboardModel;

    public function __construct() {
        $this->requireAuth();
        $this->dashboardModel = new DashboardModel();
    }

    public function index(): void {
        $kpis = $this->dashboardModel->getKpis();
        $recentIncidents = $this->dashboardModel->getRecentIncidents(5);
        $monthlyTrend = $this->dashboardModel->getMonthlyTrend();
        $siteDistribution = $this->dashboardModel->getSiteDistribution();

        $data = [
            'title' => 'Dashboard | HSE Management System',
            'activePage' => 'dashboard',
            'kpis' => $kpis,
            'recentIncidents' => $recentIncidents,
            'monthlyTrend' => $monthlyTrend,
            'siteDistribution' => $siteDistribution
        ];

        $this->view('dashboard/index', $data);
    }
}
