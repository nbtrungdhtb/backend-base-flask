MONGO_URI = "mongodb://10.130.92.189/test"
MONGO_ALT_URI = MONGO_URI
MONGO_PAYMENT_URI = "mongodb://10.130.92.189/test"

CACHE = {
    'CACHE_TYPE': "redis",
    'CACHE_REDIS_URL': "redis://localhost:6379/2"
}

REDIS_URL = "redis://localhost:6379/3"

JWT_SECRET_KEY = ''

GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''

SENTRY_ENABLED = False  # True for enable on production
SENTRY_DSL = ''  # Sentry connect string

DEBUG_PORT = 8000  # port for run flask debug

ELASTICSEARCH_HOSTS = ''
ES_HOSTS = ''

JWT_EXPIRATION_DELTA = 0
