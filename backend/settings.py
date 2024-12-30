INSTALLED_APPS = [
    # ...existing code...
    'corsheaders',
    # ...existing code...
]

MIDDLEWARE = [
    # ...existing code...
    'corsheaders.middleware.CorsMiddleware',
    # ...existing code...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
