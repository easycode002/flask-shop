from app import create_app,db
from flask_migrate import Migrate
from fastapi import FastAPI
from flask_fastapi import FastAPIApp

# Intialize Flask App
flask_app = create_app()
migrate = Migrate(flask_app,db)

# Intialize FastAPI
fastapi_app = FastAPI(
    title="Flask Shop",
    version="0.0.1",
    description="None",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)

@fastapi_app.get('/fastapi')
async def fastapi_route():
    return {'message':'Hello from FalstAPI'}

# Mount FastAPI inside Flask
flask_app.wsgi_app=FastAPIApp(fastapi_app,flask_app.wsgi_app,prefix="/api")

if __name__ == "__main__":
    flask_app.run(host='0.0.0.0',port=5000,debug=True)