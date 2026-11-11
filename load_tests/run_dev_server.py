"""Start Django's local WSGI server with a larger listen backlog for load tests."""

import os
import socketserver
import sys
from pathlib import Path


# Django's WSGIServer declares a backlog of ten. The threaded runner ramps
# synthetic logins, so the accept queue must hold the in-flight connections.
socketserver.TCPServer.request_queue_size = 1024
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.servers.basehttp import ThreadedWSGIServer, WSGIServer  # noqa: E402
from django.core.management import execute_from_command_line  # noqa: E402

WSGIServer.request_queue_size = 1024
ThreadedWSGIServer.request_queue_size = 1024


execute_from_command_line([
    "manage.py",
    "runserver",
    *sys.argv[1:],
])
