"""
Settings loader — imports from environment-selected module.
"""
import os

ENV = os.environ.get("ENVIRONMENT", "development")

if ENV == "production":
    from .production import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403