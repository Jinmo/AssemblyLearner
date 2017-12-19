#!/usr/bin/env python3

from asmlearner import app, create_db

if __name__ == '__main__':
    create_db()

    app.run(host='0.0.0.0', port=8080, debug=True)
