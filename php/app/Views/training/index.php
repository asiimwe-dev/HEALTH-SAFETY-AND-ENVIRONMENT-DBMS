<?php include APP_ROOT . '/app/Views/inc/header.php'; ?>

<div class="mb-8">
    <h2 class="text-xs font-semibold text-indigo-600 uppercase tracking-wide">Compliance & Certification</h2>
    <h1 class="text-3xl font-extrabold text-slate-900">Training & Certification Matrix</h1>
    <p class="mt-2 text-sm text-slate-600">Enterprise workforce compliance monitoring — many-to-many relationship mapping</p>
</div>

<!-- KPI row -->
<div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
    <div class="bg-white overflow-hidden shadow rounded-lg p-5 border-l-4 border-indigo-500">
        <div class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Total Records</div>
        <div class="text-2xl font-bold text-slate-900"><?= $stats['total_records'] ?></div>
        <div class="text-xs text-slate-500 mt-2">All employee certifications</div>
    </div>
    <div class="bg-white overflow-hidden shadow rounded-lg p-5 border-l-4 border-green-500">
        <div class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Valid Certs</div>
        <div class="text-2xl font-bold text-green-600"><?= $stats['valid_certs'] ?></div>
        <div class="text-xs text-slate-500 mt-2">Currently compliant</div>
    </div>
    <div class="bg-white overflow-hidden shadow rounded-lg p-5 border-l-4 border-red-500">
        <div class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Expired</div>
        <div class="text-2xl font-bold text-red-600"><?= $stats['expired_certs'] ?></div>
        <div class="text-xs text-slate-500 mt-2">Requires immediate renewal</div>
    </div>
    <div class="bg-white overflow-hidden shadow rounded-lg p-5 border-l-4 border-indigo-400">
        <div class="text-xs font-medium text-slate-500 uppercase tracking-wider mb-1">Avg Score</div>
        <div class="text-2xl font-bold text-slate-900"><?= $stats['avg_score'] ?>%</div>
        <div class="text-xs text-slate-500 mt-2">Assessment average</div>
    </div>
</div>

<!-- Filters -->
<div class="bg-white shadow rounded-lg p-6 mb-8">
    <form method="GET" action="<?= URL_ROOT ?>/training" class="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
        <div>
            <label for="category" class="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Course Category</label>
            <select name="category" id="category" class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="">All Categories</option>
                <?php foreach ($categories as $cat): ?>
                <option value="<?= $cat ?>" <?= ($filters['category'] === $cat) ? 'selected' : '' ?>><?= $cat ?></option>
                <?php endforeach; ?>
            </select>
        </div>
        <div>
            <label for="status" class="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-1">Cert Status</label>
            <select name="status" id="status" class="block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                <option value="">All Statuses</option>
                <option value="Valid" <?= ($filters['status'] === 'Valid') ? 'selected' : '' ?>>Valid</option>
                <option value="Expired" <?= ($filters['status'] === 'Expired') ? 'selected' : '' ?>>Expired</option>
                <option value="Pending Renewal" <?= ($filters['status'] === 'Pending Renewal') ? 'selected' : '' ?>>Pending Renewal</option>
            </select>
        </div>
        <div class="flex space-x-2">
            <button type="submit" class="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700">
                <i class="fa-solid fa-filter mr-1"></i> Apply
            </button>
            <a href="<?= URL_ROOT ?>/training" class="bg-slate-100 py-2 px-4 border border-slate-300 rounded-md text-sm font-medium text-slate-700 hover:bg-slate-200">Reset</a>
        </div>
    </form>
</div>

<!-- Matrix Table -->
<div class="bg-white shadow overflow-hidden sm:rounded-lg">
    <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-slate-200">
            <thead class="bg-slate-50">
                <tr>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Employee & Site</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Course</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Dates</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Compliance</th>
                    <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Score</th>
                </tr>
            </thead>
            <tbody class="bg-white divide-y divide-slate-200 text-sm">
                <?php foreach ($matrix as $row): ?>
                <tr class="hover:bg-slate-50">
                    <td class="px-6 py-4">
                        <div class="font-medium text-slate-900"><?= $row['employee_name'] ?></div>
                        <div class="text-xs text-slate-500"><?= $row['site_name'] ?></div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="text-slate-900"><?= $row['course_name'] ?></div>
                        <div class="text-xs font-mono text-indigo-600"><?= $row['course_code'] ?></div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="text-xs"><span class="text-slate-400">Comp:</span> <?= date('M d, Y', strtotime($row['completion_date'])) ?></div>
                        <div class="text-xs"><span class="text-slate-400">Exp:</span> <?= date('M d, Y', strtotime($row['expiry_date'])) ?></div>
                    </td>
                    <td class="px-6 py-4">
                        <?php if ($row['cert_status'] === 'Valid'): ?>
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                                <i class="fa-solid fa-check-circle mr-1"></i> Valid
                            </span>
                        <?php else: ?>
                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-red-100 text-red-800">
                                <i class="fa-solid fa-circle-xmark mr-1"></i> Expired
                            </span>
                        <?php endif; ?>
                        <div class="text-[10px] text-slate-400 mt-1"><?= $row['days_until_expiry'] ?> days remaining</div>
                    </td>
                    <td class="px-6 py-4">
                        <div class="w-full bg-slate-200 rounded-full h-1.5 mb-1">
                            <div class="bg-indigo-600 h-1.5 rounded-full" style="width: <?= $row['score'] ?>%"></div>
                        </div>
                        <div class="text-[10px] text-right font-bold text-slate-700"><?= $row['score'] ?>%</div>
                    </td>
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    </div>
</div>

<?php include APP_ROOT . '/app/Views/inc/footer.php'; ?>
