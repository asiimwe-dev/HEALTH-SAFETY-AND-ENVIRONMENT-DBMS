<!DOCTYPE html>
<html lang="en" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Internal Server Error</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="h-full flex items-center justify-center p-4">
    <div class="max-w-md w-full text-center">
        <div class="inline-flex items-center justify-center w-24 h-24 rounded-full bg-red-100 text-red-600 mb-8">
            <i class="fa-solid fa-server text-4xl"></i>
        </div>
        <h1 class="text-4xl font-extrabold text-slate-900 mb-4">500</h1>
        <h2 class="text-xl font-bold text-slate-800 mb-4">Internal Server Error</h2>
        <p class="text-slate-600 mb-8">
            A technical error occurred while processing your request. Our engineers have been notified.
        </p>
        <a href="<?= URL_ROOT ?>/dashboard" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700">
            <i class="fa-solid fa-house mr-2"></i> Back to Dashboard
        </a>
    </div>
</body>
</html>
