<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-900">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? APP_NAME ?></title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Bebas+Neue&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-bebas { font-family: 'Bebas Neue', cursive; }
    </style>
</head>
<body class="h-full flex items-center justify-center p-4">
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-2xl relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-1.5 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500"></div>
        
        <div class="text-center">
            <div class="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-indigo-600 text-white shadow-xl shadow-indigo-500/30 mb-4">
                <i class="fa-solid fa-shield-halved text-4xl"></i>
            </div>
            <h1 class="text-5xl font-black tracking-tighter text-slate-900 leading-none uppercase">HSE</h1>
            <p class="mt-2 text-xs text-slate-500 uppercase tracking-[0.3em] font-black">Health, Safety & Environment</p>
            <div class="mt-2 h-1.5 w-16 bg-indigo-600 mx-auto rounded-full"></div>
        </div>

        <?php if (isset($error)): ?>
        <div class="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
            <div class="flex">
                <div class="flex-shrink-0">
                    <i class="fa-solid fa-circle-exclamation text-red-400"></i>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-red-700"><?= $error ?></p>
                </div>
            </div>
        </div>
        <?php endif; ?>

        <form class="mt-8 space-y-6" action="<?= URL_ROOT ?>/auth/login" method="POST">
            <div class="rounded-md shadow-sm -space-y-px">
                <div class="mb-4">
                    <label for="username" class="block text-xs font-bold text-slate-500 uppercase mb-1">Username</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
                            <i class="fa-solid fa-user"></i>
                        </span>
                        <input id="username" name="username" type="text" required class="appearance-none rounded-lg relative block w-full px-3 py-3 pl-10 border border-slate-300 placeholder-slate-400 text-slate-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="e.g. admin">
                    </div>
                </div>
                <div>
                    <label for="password" class="block text-xs font-bold text-slate-500 uppercase mb-1">Password</label>
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 pl-3 flex items-center text-slate-400">
                            <i class="fa-solid fa-lock"></i>
                        </span>
                        <input id="password" name="password" type="password" required class="appearance-none rounded-lg relative block w-full px-3 py-3 pl-10 border border-slate-300 placeholder-slate-400 text-slate-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm" placeholder="••••••••">
                    </div>
                </div>
            </div>

            <div>
                <button type="submit" class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-bold rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all transform hover:-translate-y-0.5 shadow-lg shadow-indigo-500/30">
                    SIGN IN TO SYSTEM
                </button>
            </div>
        </form>

        <div class="mt-6 text-center">
            <p class="text-xs text-slate-400 font-mono">
                Authorised Personnel Only<br>
                v2.0 Build 2026.06.01
            </p>
        </div>
    </div>
</body>
</html>
