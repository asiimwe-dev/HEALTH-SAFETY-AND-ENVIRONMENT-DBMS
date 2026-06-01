<?php include APP_ROOT . '/app/Views/inc/header.php'; ?>

<div class="mb-8">
    <h2 class="text-xs font-semibold text-indigo-600 uppercase tracking-wide">Operational Overview</h2>
    <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl">HSE Performance Dashboard</h1>
    <p class="mt-2 text-sm text-slate-600">Albertine Graben Operations — All Active Sites · Real-time data</p>
</div>

<!-- KPI Cards -->
<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 mb-8">
    <!-- Total Incidents -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 border-indigo-500">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-list-ol text-2xl text-slate-400"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">Total Incidents</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-bold text-slate-900"><?= $kpis['total_incidents'] ?></div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">All time recorded</div>
        </div>
    </div>

    <!-- Open Incidents -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 <?= $kpis['open_incidents'] > 0 ? 'border-orange-500' : 'border-green-500' ?>">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-folder-open text-2xl <?= $kpis['open_incidents'] > 0 ? 'text-orange-400' : 'text-green-400' ?>"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">Open Cases</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-bold text-slate-900"><?= $kpis['open_incidents'] ?></div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">Requires investigation</div>
        </div>
    </div>

    <!-- LTI Events -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 <?= $kpis['total_lti'] > 0 ? 'border-red-500' : 'border-green-500' ?>">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-user-injured text-2xl <?= $kpis['total_lti'] > 0 ? 'text-red-400' : 'text-green-400' ?>"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">LTI Events</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-bold text-slate-900"><?= $kpis['total_lti'] ?></div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">Lost Time Injuries</div>
        </div>
    </div>

    <!-- High/Critical -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 border-red-600">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-triangle-exclamation text-2xl text-red-500"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">High/Critical</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-bold text-slate-900"><?= $kpis['high_critical'] ?></div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">High severity tier</div>
        </div>
    </div>

    <!-- Training Compliance -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 border-indigo-600">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-user-graduate text-2xl text-indigo-400"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">Compliance</dt>
                        <dd class="flex items-baseline">
                            <div class="text-2xl font-bold text-slate-900"><?= $kpis['training_pct'] ?>%</div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">Valid certifications</div>
        </div>
    </div>

    <!-- Highest Risk Site -->
    <div class="bg-white overflow-hidden shadow rounded-lg border-t-4 border-slate-800">
        <div class="p-5">
            <div class="flex items-center">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-location-dot text-2xl text-slate-600"></i>
                </div>
                <div class="ml-5 w-0 flex-1">
                    <dl>
                        <dt class="text-xs font-medium text-slate-500 truncate uppercase tracking-wider">Risk Focus</dt>
                        <dd class="flex items-baseline">
                            <div class="text-lg font-bold text-slate-900 leading-tight"><?= $kpis['highest_risk_site'] ?></div>
                        </dd>
                    </dl>
                </div>
            </div>
        </div>
        <div class="bg-slate-50 px-5 py-2">
            <div class="text-xs text-slate-500">Critical risk category</div>
        </div>
    </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
    <!-- Incident Trend Chart -->
    <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-slate-900 mb-4 flex items-center">
            <i class="fa-solid fa-chart-line mr-2 text-indigo-500"></i>
            Monthly Incident Trend
        </h3>
        <div class="h-64">
            <canvas id="trendChart"></canvas>
        </div>
    </div>

    <!-- Site Distribution Chart -->
    <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-slate-900 mb-4 flex items-center">
            <i class="fa-solid fa-chart-pie mr-2 text-indigo-500"></i>
            Incidents by Site
        </h3>
        <div class="h-64">
            <canvas id="siteChart"></canvas>
        </div>
    </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
    <!-- Recent Incidents Feed -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200 flex justify-between items-center">
            <h3 class="text-lg font-medium text-slate-900 flex items-center">
                <i class="fa-solid fa-clock-rotate-left mr-2 text-indigo-500"></i>
                Recent Incidents Feed
            </h3>
            <a href="<?= URL_ROOT ?>/incidents" class="text-sm font-medium text-indigo-600 hover:text-indigo-500">View All</a>
        </div>
        <ul role="list" class="divide-y divide-slate-200">
            <?php foreach ($recentIncidents as $incident): ?>
            <li class="px-6 py-4 hover:bg-slate-50 transition-colors">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                            <?= $incident['severity'] === 'Critical' ? 'bg-red-100 text-red-800' : ($incident['severity'] === 'High' ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800') ?>">
                            <?= $incident['severity'] ?>
                        </span>
                        <p class="ml-3 text-sm font-medium text-slate-900 truncate"><?= $incident['incident_type'] ?></p>
                    </div>
                    <div class="text-xs text-slate-500">
                        <?= date('M d, Y', strtotime($incident['incident_date'])) ?>
                    </div>
                </div>
                <div class="mt-2 flex justify-between">
                    <p class="text-sm text-slate-600 italic">"<?= substr($incident['description'], 0, 80) ?>..."</p>
                    <p class="text-xs font-semibold text-slate-500 uppercase tracking-tighter"><?= $incident['site_name'] ?></p>
                </div>
            </li>
            <?php endforeach; ?>
        </ul>
    </div>

    <!-- Site Risk Summary -->
    <div class="bg-white shadow rounded-lg overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-200">
            <h3 class="text-lg font-medium text-slate-900 flex items-center">
                <i class="fa-solid fa-shield-virus mr-2 text-indigo-500"></i>
                Site Risk Summary
            </h3>
        </div>
        <div class="p-6">
            <div class="space-y-4">
                <?php foreach ($siteDistribution as $site): ?>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <span class="text-sm font-medium text-slate-700"><?= $site['site_name'] ?></span>
                        <span class="text-xs font-bold text-slate-500"><?= $site['incident_count'] ?> incidents</span>
                    </div>
                    <div class="w-full bg-slate-100 rounded-full h-2">
                        <div class="bg-indigo-600 h-2 rounded-full" style="width: <?= min(100, ($site['incident_count'] / max(1, $kpis['total_incidents'])) * 100) ?>%"></div>
                    </div>
                </div>
                <?php endforeach; ?>
            </div>
        </div>
    </div>
</div>

<script>
    // Inject data from PHP to JS
    const trendData = <?= json_encode($monthlyTrend) ?>;
    const siteData = <?= json_encode($siteDistribution) ?>;

    document.addEventListener('DOMContentLoaded', () => {
        // Trend Chart
        new Chart(document.getElementById('trendChart'), {
            type: 'line',
            data: {
                labels: trendData.map(d => d.month),
                datasets: [{
                    label: 'Total Incidents',
                    data: trendData.map(d => d.total),
                    borderColor: '#6366f1',
                    tension: 0.4,
                    fill: true,
                    backgroundColor: 'rgba(99, 102, 241, 0.1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, grid: { display: false } } }
            }
        });

        // Site Chart
        new Chart(document.getElementById('siteChart'), {
            type: 'bar',
            data: {
                labels: siteData.map(d => d.site_name.split(' ').slice(-2).join(' ')),
                datasets: [{
                    label: 'Incidents',
                    data: siteData.map(d => d.incident_count),
                    backgroundColor: '#6366f1',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });
    });
</script>

<?php include APP_ROOT . '/app/Views/inc/footer.php'; ?>
