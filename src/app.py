from flask import Flask
from flasgger import Swagger
from routes import books_bp
import os

app = Flask(__name__)

def create_app():
    swagger_config = {
        'headers': [],
        'specs': [
            {
                'endpoint': 'apispec',
                'route': '/api-docs.json',
                'rule_filter': lambda rule: True,
                'model_filter': lambda tag: True,
            }
        ],
        'static_url_path': '/flasgger_static',
        'swagger_ui': True,
        'specs_route': '/api-docs/'
    }
    Swagger(app, config=swagger_config, template_file=os.path.join(os.path.dirname(__file__), 'swagger.yml'))

    app.register_blueprint(books_bp, url_prefix='/api')

    @app.errorhandler(500)
    def internal_error(e):
        return {"error": "Internal Server Error"}, 500

    @app.route('/')
    def index():
        return "Welcome to the API"

    return app

create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)