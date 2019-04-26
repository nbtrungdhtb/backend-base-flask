# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located in app/__init__.py."""
import os

from elasticsearch import Elasticsearch
from flask import Config
from flask_caching import Cache
from mongoengine import connect
from redis import StrictRedis

config = Config(root_path='')
config.from_object(os.getenv('FLASK_CONFIG') or 'config')

cache = Cache(config=config.get('CACHE'))

db = connect(alias="default", host=config.get("MONGO_URI", "localhost"))
db_payment = connect(alias="payment", host=config.get("MONGO_PAYMENT_URI", "localhost"))
db_alt = connect(alias="alt", host=config.get("MONGO_ALT_URI", "localhost"))

db_redis = StrictRedis.from_url(config.get("REDIS_URL", "redis://localhost:6379/1"))

client_es = Elasticsearch(hosts=config.get("ES_HOSTS", "localhost"))

if config.get('SENTRY_ENABLED', False) and config.get('SENTRY_DSL', '') != '':
    import sentry_sdk
    from sentry_sdk.integrations.flask import FlaskIntegration

    sentry_sdk.init(
        dsn=config.get('SENTRY_DSL', ''),
        integrations=[FlaskIntegration()]
    )
