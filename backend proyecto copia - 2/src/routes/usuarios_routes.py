from flask import Blueprint, request, jsonify
from src.models.usuarios import Usuarios
from src.utils.auth import token_required, rol_required

usuarios_bp = Blueprint('usuarios', __name__)

# READ ALL
@usuarios_bp.route('/', methods=['GET'])
@token_required
@rol_required('Administrador')
def get_usuarios():
    usuarios = Usuarios.get()
    usuarios_list = []
    for usu in usuarios:
        usuarios_list.append({
            'id_usuario': usu.id_usuario,
            'nombre': usu.nombre,  # Campo heredado de Persona
            'nombre_usuario': usu.nombre_usuario,
            'email': usu.email,
            'rol': usu.rol,
            'activo': usu.activo,
            'creado_en': usu.creado_en.strftime('%Y-%m-%d %H:%M:%S') if getattr(usu, 'creado_en', None) else None
        })
    return jsonify(usuarios_list), 200

# READ ONE
@usuarios_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_usuario(id):
    usu = Usuarios.get_by_id(id)
    if usu:
        return jsonify({
            'id_usuario': usu.id_usuario,
            'nombre': usu.nombre,
            'nombre_usuario': usu.nombre_usuario,
            'email': usu.email,
            'rol': usu.rol,
            'activo': usu.activo,
            'creado_en': usu.creado_en.strftime('%Y-%m-%d %H:%M:%S') if getattr(usu, 'creado_en', None) else None
        }), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

# CREATE
@usuarios_bp.route('/', methods=['POST'])
@token_required
@rol_required('Administrador')
def create_usuario():
    data = request.get_json() or {}
    
    nombre = str(data.get('nombre', '')).strip()
    nombre_usuario = str(data.get('nombre_usuario', '')).strip()
    email = str(data.get('email', '')).strip()
    password = str(data.get('password', '')).strip()

    # Validaciones obligatorias de presencia
    if not nombre:
        return jsonify({'message': 'El nombre real es obligatorio'}), 400
    if not nombre_usuario:
        return jsonify({'message': 'El nombre de usuario es obligatorio'}), 400
    if not email:
        return jsonify({'message': 'El email es obligatorio'}), 400
    if not password:
        return jsonify({'message': 'La contraseña es obligatoria'}), 400

    # Validar que el email o nombre_usuario no estén registrados previamente
    if Usuarios.get_by_email(email):
        return jsonify({'message': f'El correo electrónico {email} ya se encuentra registrado'}), 400

    if Usuarios.get_by_username(nombre_usuario):
        return jsonify({'message': f'El nombre de usuario {nombre_usuario} ya está en uso'}), 400

    usuario = Usuarios(
        nombre=nombre,
        nombre_usuario=nombre_usuario,
        email=email,
        password_hash=password,
        rol=data.get('rol', 'Vendedor'),
        activo=int(data.get('activo', 1))
    )
    
    usuario.save()
    return jsonify({
        'message': 'Usuario creado exitosamente',
        'id_usuario': usuario.id_usuario
    }), 201

# UPDATE
@usuarios_bp.route('/<int:id>', methods=['PUT'])
@token_required
@rol_required('Administrador')
def update_usuario(id):
    usu = Usuarios.get_by_id(id)
    if not usu:
        return jsonify({'message': 'Usuario no encontrado'}), 404
        
    data = request.get_json() or {}

    # Actualización condicional del nombre
    if 'nombre' in data:
        nombre = str(data['nombre']).strip()
        if not nombre:
            return jsonify({'message': 'El nombre real no puede estar vacío'}), 400
        usu.nombre = nombre

    # Actualización condicional del nombre de usuario
    if 'nombre_usuario' in data:
        nombre_usu = str(data['nombre_usuario']).strip()
        if not nombre_usu:
            return jsonify({'message': 'El nombre de usuario no puede estar vacío'}), 400
        # Verificar que no entre en conflicto con otro registro
        existente = Usuarios.get_by_username(nombre_usu)
        if existente and existente.id_usuario != id:
            return jsonify({'message': f'El nombre de usuario {nombre_usu} ya está en uso'}), 400
        usu.nombre_usuario = nombre_usu

    # Actualización condicional del email
    if 'email' in data:
        email = str(data['email']).strip()
        if not email:
            return jsonify({'message': 'El email no puede estar vacío'}), 400
        # Verificar que no entre en conflicto con otro registro
        existente = Usuarios.get_by_email(email)
        if existente and existente.id_usuario != id:
            return jsonify({'message': f'El correo {email} ya está registrado'}), 400
        usu.email = email

    # Actualización de rol y estado activo
    if 'rol' in data:
        usu.rol = data['rol']

    if 'activo' in data:
        usu.activo = int(data['activo'])

    # Actualización opcional de la contraseña
    if 'password' in data and str(data['password']).strip():
        usu.establecer_password(str(data['password']).strip())

    usu.save()
    return jsonify({'message': 'Usuario actualizado exitosamente'}), 200

# DELETE
@usuarios_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@rol_required('Administrador')
def delete_usuario(id):
    usu = Usuarios.get_by_id(id)
    if usu:
        usu.delete()
        return jsonify({'message': 'Usuario eliminado exitosamente'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404