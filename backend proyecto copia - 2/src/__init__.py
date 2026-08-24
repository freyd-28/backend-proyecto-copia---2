import os

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from src.config.config import config
from src.models import Base, engine, session


from src.routes import all_blueprints


load_dotenv()


def create_app(config_name=None):

  

    if config_name is None:
        config_name = os.getenv(
            "FLASK_CONFIG",
            "development",
        )



    app = Flask(__name__)


    selected_config = config.get(
        config_name,
        config["default"],
    )

    app.config.from_object(selected_config)

    
    # VERIFICACIÓN JWT

    if not app.config.get("JWT_SECRET_KEY"):
        raise RuntimeError(
            "JWT_SECRET_KEY no está configurada."
        )



    print()
    print("=" * 60)
    print(" BilleterAPP API")
    print("=" * 60)
    print(f" Configuración : {config_name}")
    print(
        f" JWT_SECRET_KEY: "
        f"{'CONFIGURADA' if app.config.get('JWT_SECRET_KEY') else 'NO CONFIGURADA'}"
    )
    print(
        f" API_BASE_URL  : "
        f"{app.config.get('API_BASE_URL')}"
    )
    print(
        f" DEBUG         : "
        f"{app.config.get('DEBUG')}"
    )
    print("=" * 60)
    print()



    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://127.0.0.1:5001",
                    "http://localhost:5001",
                ],
                "methods": [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "OPTIONS",
                ],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                ],
            }
        },
    )



    try:

        Base.metadata.create_all(engine)

    except SQLAlchemyError as exc:

        app.logger.exception(
            "No se pudo inicializar la base de datos"
        )

        raise RuntimeError(
            "No fue posible conectar o preparar la base de datos"
        ) from exc

    # REGISTRAR BLUEPRINTS  

    prefix = "/api/v1"

    for bp in all_blueprints:

        url_prefix = f"{prefix}/{bp.name}"

        app.register_blueprint(
            bp,
            url_prefix=url_prefix,
        )

        print(
            f"-> Blueprint registrado: "
            f"{bp.name} en ruta {url_prefix}"
        )

    # RUTA PRINCIPAL
  
    @app.get("/")
    def index():

        return jsonify({
            "status": "online",
            "system": "BilleterAPP API",
            "version": "1.0.0",
        }), 200


    @app.errorhandler(404)
    def not_found(error):

        return jsonify({
            "message": "Recurso no encontrado",
        }), 404


    @app.errorhandler(405)
    def method_not_allowed(error):

        return jsonify({
            "message": "Metodo HTTP no permitido",
        }), 405

    
    # ERROR DE INTEGRIDAD
    
    @app.errorhandler(IntegrityError)
    def integrity_error(error):

        session.rollback()

        return jsonify({
            "message": (
                "La operacion viola una "
                "restriccion de la base de datos"
            ),
        }), 409


    @app.teardown_appcontext
    def shutdown_session(exception=None):

        session.remove()

    return app
