<?php include APP_ROOT . '/app/Views/inc/header.php'; ?>

<div class="mb-8 flex justify-between items-center">
    <div>
        <h2 class="text-xs font-semibold text-indigo-600 uppercase tracking-wide">Records Management</h2>
        <h1 class="text-3xl font-extrabold text-slate-900">Incident Register</h1>
        <p class="mt-2 text-sm text-slate-600">Full incident log — filter, search, and inspect all recorded events</p>
    </div>
    <a href="<?= URL_ROOT ?>/incidents/create" class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
        <i class="fa-solid fa-plus mr-2"></i> Report New Incident
    </a>
</div>

<!-- Filters -->
<div class="bg-white shadow rounded-lg p-6 mb-8">
    <form method="GET" action="<?= URL_ROOT ?>/incidents" class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <div>
            <label for="site_id" class="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Site</label>
            <select name="site_id" id="site_id" class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="">All Sites</option>
                <?php foreach ($sites as $site): ?>
                <option value="<?= $site['site_id'] ?>" <?= ($filters['site_id'] == $site['site_id']) ? 'selected' : '' ?>><?= $site['site_name'] ?></option>
                <?php endforeach; ?>
            </select>
        </div>
        <div>
            <label for="severity" class="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Severity</label>
            <select name="severity" id="severity" class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="">All Severities</option>
                <option value="Low" <?= ($filters['severity'] === 'Low') ? 'selected' : '' ?>>Low</option>
                <option value="Medium" <?= ($filters['severity'] === 'Medium') ? 'selected' : '' ?>>Medium</option>
                <option value="High" <?= ($filters['severity'] === 'High') ? 'selected' : '' ?>>High</option>
                <option value="Critical" <?= ($filters['severity'] === 'Critical') ? 'selected' : '' ?>>Critical</option>
            </select>
        </div>
        <div>
            <label for="status" class="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Status</label>
            <select name="status" id="status" class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="">All Statuses</option>
                <option value="Open" <?= ($filters['status'] === 'Open') ? 'selected' : '' ?>>Open</option>
                <option value="Under Investigation" <?= ($filters['status'] === 'Under Investigation') ? 'selected' : '' ?>>Under Investigation</option>
                <option value="Closed" <?= ($filters['status'] === 'Closed') ? 'selected' : '' ?>>Closed</option>
            </select>
        </div>
        <div class="flex space-x-2">
            <button type="submit" class="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                <i class="fa-solid fa-filter mr-1"></i> Filter
            </button>
            <a href="<?= URL_ROOT ?>/incidents" class="bg-slate-100 py-2 px-4 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 hover:bg-slate-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 text-center">
                Clear
            </a>
        </div>
    </form>
</div>

<!-- Results Table -->
<div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
                <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date & ID</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Site</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Type & Severity</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Reporter</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                    <th scope="col" class="relative px-6 py-3">
                        <span class="sr-only">Actions</span>
                    </th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-200">
                <?php foreach ($incidents as $incident): ?>
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm font-medium text-slate-900"><?= date('M d, Y', strtotime($incident['incident_date'])) ?></div>
                        <div class="text-xs text-slate-500">#INC-<?= str_pad((string)$incident['incident_id'], 5, '0', STR_PAD_LEFT) ?></div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-slate-900"><?= $incident['site_name'] ?></div>
                        <div class="text-xs text-slate-500"><?= $incident['district'] ?></div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <div class="text-sm text-slate-900"><?= $incident['incident_type'] ?></div>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium 
                            <?= $incident['severity'] === 'Critical' ? 'bg-red-100 text-red-800' : ($incident['severity'] === 'High' ? 'bg-orange-100 text-orange-800' : 'bg-blue-100 text-blue-800') ?>">
                            <?= $incident['severity'] ?>
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                        <?= $incident['reporter_name'] ?>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                            <?= $incident['inc_status'] === 'Open' ? 'bg-yellow-100 text-yellow-800' : ($incident['inc_status'] === 'Closed' ? 'bg-green-100 text-green-800' : 'bg-slate-100 text-slate-800') ?>">
                            <?= $incident['inc_status'] ?>
                        </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <a href="<?= URL_ROOT ?>/incidents/view/<?= $incident['incident_id'] ?>" class="text-indigo-600 hover:text-indigo-900">View Details</a>
                    </td>
                </tr>
                <?php endforeach; ?>
                <?php if (empty($incidents)): ?>
                <tr>
                    <td colspan="6" class="px-6 py-10 text-center text-slate-500 italic">
                        No incidents found matching the selected filters.
                    </td>
                </tr>
                <?php endif; ?>
            </tbody>
        </table>
    </div>
</div>

<?php include APP_ROOT . '/app/Views/inc/footer.php'; ?>
