from .base import *


import os

env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .production import *
elif env == "ci":
    from .ci import *
else:
    from .development import *
