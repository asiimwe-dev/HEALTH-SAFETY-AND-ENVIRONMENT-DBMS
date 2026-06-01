<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? APP_NAME ?></title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Bebas+Neue&display=swap" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-bebas { font-family: 'Bebas Neue', cursive; }
    </style>
</head>
<body class="h-full overflow-hidden">
    <div class="flex h-full">
        <!-- Sidebar -->
        <aside class="hidden md:flex md:w-64 md:flex-col fixed inset-y-0 bg-slate-900">
            <div class="flex flex-col flex-grow pt-5 overflow-y-auto">
                <div class="flex items-center flex-shrink-0 px-4 mb-8">
                    <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-indigo-600 text-white shadow-lg shadow-indigo-500/50">
                        <i class="fa-solid fa-shield-halved text-xl"></i>
                    </div>
                    <div class="ml-3">
                        <h1 class="text-2xl font-black tracking-tight leading-none text-white uppercase">HSE</h1>
                        <p class="text-[9px] font-bold text-slate-400 uppercase tracking-widest leading-none mt-1">Health, Safety, Environment</p>
                    </div>
                </div>
                <nav class="flex-1 px-2 space-y-1">
                    <a href="<?= URL_ROOT ?>/dashboard" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-slate-800 hover:text-white <?= ($activePage ?? '') === 'dashboard' ? 'bg-slate-800 text-white' : '' ?>">
                        <i class="fa-solid fa-gauge-high mr-3 text-lg opacity-75"></i>
                        Dashboard
                    </a>
                    <a href="<?= URL_ROOT ?>/incidents" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-slate-800 hover:text-white <?= ($activePage ?? '') === 'incidents' ? 'bg-slate-800 text-white' : '' ?>">
                        <i class="fa-solid fa-list-check mr-3 text-lg opacity-75"></i>
                        Incident Register
                    </a>
                    <a href="<?= URL_ROOT ?>/incidents/create" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-slate-800 hover:text-white <?= ($activePage ?? '') === 'report' ? 'bg-slate-800 text-white' : '' ?>">
                        <i class="fa-solid fa-circle-plus mr-3 text-lg opacity-75"></i>
                        Report Incident
                    </a>
                    <a href="<?= URL_ROOT ?>/training" class="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-slate-300 hover:bg-slate-800 hover:text-white <?= ($activePage ?? '') === 'training' ? 'bg-slate-800 text-white' : '' ?>">
                        <i class="fa-solid fa-graduation-cap mr-3 text-lg opacity-75"></i>
                        Training Matrix
                    </a>
                </nav>
            </div>
            <div class="flex-shrink-0 flex bg-slate-800 p-4">
                <div class="flex-shrink-0 w-full group block">
                    <div class="flex items-center">
                        <div>
                            <div class="inline-block h-9 w-9 rounded-full bg-slate-600 flex items-center justify-center text-white">
                                <i class="fa-solid fa-user"></i>
                            </div>
                        </div>
                        <div class="ml-3">
                            <p class="text-sm font-medium text-white"><?= $_SESSION['user_name'] ?? 'Guest' ?></p>
                            <p class="text-xs font-medium text-slate-400 group-hover:text-slate-300"><?= $_SESSION['user_role'] ?? 'Visitor' ?></p>
                        </div>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content Area -->
        <div class="md:pl-64 flex flex-col flex-1">
            <!-- Top Navigation -->
            <header class="sticky top-0 z-10 flex-shrink-0 flex h-16 bg-white shadow">
                <div class="flex-1 px-4 flex justify-between">
                    <div class="flex-1 flex">
                        <div class="w-full flex md:ml-0">
                            <div class="relative w-full text-slate-400 focus-within:text-slate-600 flex items-center">
                                <i class="fa-solid fa-magnifying-glass absolute left-3"></i>
                                <input class="block w-full h-full pl-10 pr-3 py-2 border-transparent text-slate-900 placeholder-slate-500 focus:outline-none focus:placeholder-slate-400 focus:ring-0 focus:border-transparent sm:text-sm" placeholder="Search records, sites, or employees..." type="search">
                            </div>
                        </div>
                    </div>
                    <div class="ml-4 flex items-center md:ml-6 space-x-4">
                        <button type="button" class="bg-white p-1 rounded-full text-slate-400 hover:text-slate-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            <span class="sr-only">View notifications</span>
                            <i class="fa-solid fa-bell"></i>
                        </button>
                        <div class="h-6 w-px bg-slate-200"></div>
                        <a href="<?= URL_ROOT ?>/auth/logout" class="text-sm font-medium text-slate-700 hover:text-indigo-600">
                            <i class="fa-solid fa-right-from-bracket mr-1"></i> Sign Out
                        </a>
                    </div>
                </div>
            </header>

            <!-- Page Content -->
            <main class="flex-1 relative overflow-y-auto focus:outline-none bg-slate-50">
                <div class="py-6">
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
