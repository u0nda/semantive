import os
from dotenv import load_dotenv, find_dotenv
from src.app import create_app

# app = create_app()

load_dotenv(find_dotenv())

# env_name = os.getenv('test')
env_name = os.getenv('BUILD_ENV')
app = create_app(env_name)

if __name__ == '__main__':
    port = '8080'
    app.run(host='0.0.0.0', port=port)
    # app.run(host='127.0.0.1', port=port)
