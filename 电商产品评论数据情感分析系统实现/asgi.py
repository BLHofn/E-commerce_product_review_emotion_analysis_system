"""
ASGI config for 电商产品评论数据情感分析系统实现 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '电商产品评论数据情感分析系统实现.settings')

application = get_asgi_application()
