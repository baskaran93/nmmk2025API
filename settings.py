INSTALLED_APPS = [
    'corsheaders'
    # ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...
]

CORS_ALLOW_ALL_ORIGINS = True  # For development only, restrict in production
