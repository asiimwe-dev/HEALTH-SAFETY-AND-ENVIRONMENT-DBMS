<?php include APP_ROOT . '/app/Views/inc/header.php'; ?>

<div class="mb-8">
    <h2 class="text-xs font-semibold text-indigo-600 uppercase tracking-wide">Data Entry</h2>
    <h1 class="text-3xl font-extrabold text-slate-900">Report New Incident</h1>
    <p class="mt-2 text-sm text-slate-600">All fields marked * are mandatory. Records are committed to the HSE database immediately.</p>
</div>

<div class="bg-white shadow sm:rounded-lg overflow-hidden">
    <?php if (empty($sites) || empty($employees)): ?>
        <div class="p-8 text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 text-red-600 mb-4">
                <i class="fa-solid fa-database text-2xl"></i>
            </div>
            <h3 class="text-lg font-bold text-slate-900">Database Synchronization Issue</h3>
            <p class="mt-2 text-sm text-slate-500 max-w-md mx-auto">The system cannot find any active sites or employees in the database. Please ensure you have imported <code>hse_db.sql</code> correctly.</p>
            <a href="<?= URL_ROOT ?>/dashboard" class="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200">
                Return to Dashboard
            </a>
        </div>
    <?php else: ?>
        <form action="<?= URL_ROOT ?>/incidents/store" method="POST" class="divide-y divide-slate-200">
            <input type="hidden" name="csrf_token" value="<?= $csrf_token ?>">

            <!-- Section 1: Personnel -->
            <div class="p-6 md:p-8">
                <h3 class="text-lg font-medium text-slate-900 mb-6 flex items-center">
                    <span class="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 font-bold text-sm mr-3">1</span>
                    Incident Details & Personnel
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <label for="incident_date" class="block text-sm font-medium text-slate-700">Incident Date *</label>
                        <input type="date" name="incident_date" id="incident_date" required value="<?= $old['incident_date'] ?? date('Y-m-d') ?>" class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="incident_time" class="block text-sm font-medium text-slate-700">Incident Time *</label>
                        <input type="time" name="incident_time" id="incident_time" required value="<?= $old['incident_time'] ?? date('H:i') ?>" class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="site_id" class="block text-sm font-medium text-slate-700">Site *</label>
                        <select name="site_id" id="site_id" required class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <option value="">Select a site</option>
                            <?php foreach ($sites as $site): ?>
                                <option value="<?= $site['site_id'] ?>" <?= (isset($old['site_id']) && $old['site_id'] == $site['site_id']) ? 'selected' : '' ?>><?= htmlspecialchars($site['site_name']) ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div>
                        <label for="reported_by" class="block text-sm font-medium text-slate-700">Reporting Officer *</label>
                        <select name="reported_by" id="reported_by" required class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <option value="">Select officer</option>
                            <?php foreach ($employees as $emp): ?>
                                <option value="<?= $emp['employee_id'] ?>" <?= (isset($old['reported_by']) && $old['reported_by'] == $emp['employee_id']) ? 'selected' : '' ?>><?= htmlspecialchars($emp['name']) ?> (<?= htmlspecialchars($emp['job_title']) ?>)</option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Section 2: Classification -->
            <div class="p-6 md:p-8 bg-slate-50">
                <h3 class="text-lg font-medium text-slate-900 mb-6 flex items-center">
                    <span class="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 font-bold text-sm mr-3">2</span>
                    Classification & Root Cause
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div>
                        <label for="incident_type" class="block text-sm font-medium text-slate-700">Incident Type *</label>
                        <select name="incident_type" id="incident_type" required class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <?php foreach (['Near-Miss', 'First Aid', 'MTC', 'LTI', 'Fatality', 'Environmental'] as $type): ?>
                                <option value="<?= $type ?>" <?= (isset($old['incident_type']) && $old['incident_type'] === $type) ? 'selected' : '' ?>><?= $type ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div>
                        <label for="severity" class="block text-sm font-medium text-slate-700">Severity Level *</label>
                        <select name="severity" id="severity" required class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <?php foreach (['Low', 'Medium', 'High', 'Critical'] as $sev): ?>
                                <option value="<?= $sev ?>" <?= (isset($old['severity']) && $old['severity'] === $sev) ? 'selected' : '' ?>><?= $sev ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                    <div>
                        <label for="root_cause" class="block text-sm font-medium text-slate-700">Root Cause *</label>
                        <select name="root_cause" id="root_cause" required class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <?php foreach (['Procedural Violation', 'Equipment Failure', 'Human Error', 'Environmental Condition', 'Management System Gap'] as $rc): ?>
                                <option value="<?= $rc ?>" <?= (isset($old['root_cause']) && $old['root_cause'] === $rc) ? 'selected' : '' ?>><?= $rc ?></option>
                            <?php endforeach; ?>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Section 3: Narrative -->
            <div class="p-6 md:p-8">
                <h3 class="text-lg font-medium text-slate-900 mb-6 flex items-center">
                    <span class="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 font-bold text-sm mr-3">3</span>
                    Incident Narrative & Actions
                </h3>
                <div class="space-y-6">
                    <div>
                        <label for="description" class="block text-sm font-medium text-slate-700">Incident Description * (min 30 chars)</label>
                        <textarea name="description" id="description" rows="4" required placeholder="Describe what happened..." class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm <?= isset($errors['description']) ? 'border-red-300 text-red-900 focus:ring-red-500' : '' ?>"><?= htmlspecialchars($old['description'] ?? '') ?></textarea>
                        <?php if (isset($errors['description'])): ?>
                            <p class="mt-2 text-sm text-red-600"><?= $errors['description'] ?></p>
                        <?php endif; ?>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label for="immediate_action" class="block text-sm font-medium text-slate-700">Immediate Actions Taken</label>
                            <textarea name="immediate_action" id="immediate_action" rows="3" class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"><?= htmlspecialchars($old['immediate_action'] ?? '') ?></textarea>
                        </div>
                        <div>
                            <label for="corrective_action" class="block text-sm font-medium text-slate-700">Corrective Action Plan</label>
                            <textarea name="corrective_action" id="corrective_action" rows="3" class="mt-1 block w-full border-slate-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"><?= htmlspecialchars($old['corrective_action'] ?? '') ?></textarea>
                        </div>
                    </div>
                </div>
            </div>

            <div class="px-6 py-4 bg-slate-50 text-right sm:px-8">
                <a href="<?= URL_ROOT ?>/incidents" class="inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 mr-3">Cancel</a>
                <button type="submit" class="inline-flex items-center px-6 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    Submit Incident Report
                </button>
            </div>
        </form>
    <?php endif; ?>
</div>

<?php include APP_ROOT . '/app/Views/inc/footer.php'; ?>
