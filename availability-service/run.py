from api import create_app
from flask import g
import os

app = create_app()

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'mongo_db_client'):
        g.mongo_db_client.close()

if __name__ == '__main__':
    # Using a default port of 5001, but allowing it to be overridden by an environment variable
    port = int(os.environ.get("PORT", 5004))
    app.run(port=port)
