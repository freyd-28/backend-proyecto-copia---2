from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from src.utils.auth import generar_token, token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    for campo in ("email", "password", "nombre"):
        if not str(data.get(campo, "")).strip():
            return jsonify({"message": f"El campo {campo} es obligatorio"}), 400

    password = str(data["password"])
    email = str(data["email"]).strip().lower()
    nombre = str(data["nombre"]).strip()
    nombre_usuario = str(
        data.get("nombre_usuario") or email.split("@")[0]
    ).strip()

    if len(password) < 8:
        return jsonify({"message": "La contraseña debe tener al menos 8 caracteres"}), 400
    if "@" not in email:
        return jsonify({"message": "El correo electrónico no es válido"}), 400
    if Usuarios.get_by_email(email):
        return jsonify({"message": "Ese correo ya está registrado"}), 409
    if Usuarios.get_by_username(nombre_usuario):
        return jsonify({"message": "Ese nombre de usuario ya está registrado"}), 409

    # El registro público nunca permite crear un administrador.
    rol = "Vendedor"
    usuario = Usuarios(
        email=email,
        password_hash=password,
        nombre_usuario=nombre_usuario,
        nombre=nombre,
        rol=rol,
        activo=1,
    )
    usuario.save()

    return jsonify({
        "message": "Usuario registrado exitosamente",
        "usuario": usuario.to_dict(),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({"message": "Correo y contraseña son obligatorios"}), 400

    usuario = Usuarios.get_by_email(email)

    if not usuario:
        return jsonify({"message": "Credenciales inválidas"}), 401
    if int(usuario.activo) != 1:
        return jsonify({"message": "El usuario está inactivo"}), 403

    # Compatibilidad con registros antiguos que guardaban texto plano.
    valido = False
    try:
        valido = usuario.verificar_password(password)
    except ValueError:
        valido = False

    if not valido and usuario.password_hash == password:
        usuario.establecer_password(password)
        usuario.save()
        valido = True

    if not valido:
        return jsonify({"message": "Credenciales inválidas"}), 401

    return jsonify({
        "access_token": generar_token(usuario),
        "token_type": "Bearer",
        "expires_in": 28800,
        "usuario": usuario.to_dict(),
    }), 200


@auth_bp.route("/me", methods=["GET"])
@token_required
def me():
    return jsonify(request.usuario.to_dict()), 200
