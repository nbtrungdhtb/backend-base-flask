# -*- coding: utf-8 -*-
"""Create an application instance."""

from app import create_app

app = create_app()

if __name__ == "__main__":
    from app.extensions import config

    app.run("0.0.0.0", config.get('DEBUG_PORT', 8000), debug=True, threaded=True)
