from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt

from flask import current_app, request, jsonify

from src.models.usuarios import Usuarios


def generar_token(usuario, horas=8):
    """
    Genera un JWT para el usuario autenticado.
    """

    ahora = datetime.now(timezone.utc)

    payload = {
        "sub": str(usuario.id_usuario),
        "email": usuario.email,
        "rol": usuario.rol,
        "iat": ahora,
        "exp": ahora + timedelta(hours=horas),
    }

    secret_key = current_app.config.get("JWT_SECRET_KEY")

    if not secret_key:
        raise RuntimeError(
            "JWT_SECRET_KEY no está configurada en Flask."
        )

    return jwt.encode(
        payload,
        secret_key,
        algorithm="HS256",
    )


def token_required(f):
    """
    Protege una ruta que requiere autenticación JWT.
    """

    @wraps(f)
    def decorada(*args, **kwargs):

        auth = request.headers.get(
            "Authorization",
            ""
        )

        if not auth.startswith("Bearer "):
            return jsonify({
                "message": "Token faltante o mal formado"
            }), 401

        token = auth.split(
            " ",
            1
        )[1].strip()

        if not token:
            return jsonify({
                "message": "Token faltante o mal formado"
            }), 401

        secret_key = current_app.config.get(
            "JWT_SECRET_KEY"
        )

        if not secret_key:
            current_app.logger.error(
                "JWT_SECRET_KEY no está configurada."
            )

            return jsonify({
                "message": "Error de configuración del servidor"
            }), 500

        try:

            payload = jwt.decode(
                token,
                secret_key,
                algorithms=["HS256"],
            )

            user_id = int(
                payload["sub"]
            )

        except jwt.ExpiredSignatureError:

            return jsonify({
                "message": "El token ha expirado"
            }), 401

        except (
            jwt.InvalidTokenError,
            ValueError,
            KeyError,
            TypeError,
        ):

            return jsonify({
                "message": "Token inválido"
            }), 401

        usuario = Usuarios.get_by_id(
            user_id
        )

        if not usuario:
            return jsonify({
                "message": "Usuario no encontrado"
            }), 401

        if int(usuario.activo) != 1:
            return jsonify({
                "message": "El usuario está inactivo"
            }), 403

        request.usuario = usuario

        return f(
            *args,
            **kwargs
        )

    return decorada


def rol_required(*roles_permitidos):
    """
    Restringe una ruta a determinados roles.
    """

    def decorador(f):

        @wraps(f)
        def decorada(*args, **kwargs):

            usuario_actual = getattr(
                request,
                "usuario",
                None
            )

            if not usuario_actual:
                return jsonify({
                    "message": "Usuario no autenticado"
                }), 401

            if usuario_actual.rol not in roles_permitidos:
                return jsonify({
                    "message": (
                        "Acción denegada. "
                        "No tienes privilegios suficientes "
                        "para este recurso."
                    )
                }), 403

            return f(
                *args,
                **kwargs
            )

        return decorada

    return decorador
