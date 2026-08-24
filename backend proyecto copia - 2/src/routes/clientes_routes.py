from flask import Blueprint, request, jsonify
from src.models.clientes import Clientes
from src.utils.auth import token_required

clientes_bp = Blueprint('clientes', __name__)

# READ ALL
@clientes_bp.route('/', methods=['GET'])
@token_required
def get_clientes():
    clientes = Clientes.get()
    clientes_list = []
    for cli in clientes:
        clientes_list.append({
            'id_cliente': cli.id_cliente,
            'nombre': cli.nombre,  # Atributo polimórfico de Persona
            'documento': cli.documento,
            'telefono': cli.telefono,
            'direccion': cli.direccion,
            'creado_en': cli.creado_en.strftime('%Y-%m-%d %H:%M:%S') if getattr(cli, 'creado_en', None) else None
        })
    return jsonify(clientes_list), 200

# READ ONE
@clientes_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_cliente(id):
    cli = Clientes.get_by_id(id)
    if cli:
        return jsonify({
            'id_cliente': cli.id_cliente,
            'nombre': cli.nombre,
            'documento': cli.documento,
            'telefono': cli.telefono,
            'direccion': cli.direccion,
            'creado_en': cli.creado_en.strftime('%Y-%m-%d %H:%M:%S') if getattr(cli, 'creado_en', None) else None
        }), 200
    return jsonify({'message': 'Cliente no encontrado'}), 404

# CREATE
@clientes_bp.route('/', methods=['POST'])
@token_required
def create_cliente():
    data = request.get_json() or {}

    nombre = str(data.get('nombre', '')).strip()
    documento = str(data.get('documento', '')).strip()
    telefono = str(data.get('telefono', '')).strip()
    direccion = str(data.get('direccion', '')).strip()

    if not nombre or not documento:
        return jsonify({'message': 'Nombre y documento son obligatorios'}), 400

    # Evitar duplicado de documento/NIT
    if Clientes.get_by_documento(documento):
        return jsonify({'message': f'El documento {documento} ya se encuentra registrado'}), 400

    nuevo_cliente = Clientes(
        nombre=nombre,
        documento=documento,
        telefono=telefono,
        direccion=direccion
    )
    
    nuevo_cliente.save()
    return jsonify({
        'message': 'Cliente registrado exitosamente',
        'id_cliente': nuevo_cliente.id_cliente
    }), 201

# UPDATE
@clientes_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_cliente(id):
    cli = Clientes.get_by_id(id)
    if not cli:
        return jsonify({'message': 'Cliente no encontrado'}), 404

    data = request.get_json() or {}

    if 'nombre' in data:
        nombre = str(data['nombre']).strip()
        if not nombre:
            return jsonify({'message': 'El nombre no puede estar vacío'}), 400
        cli.nombre = nombre

    if 'documento' in data:
        doc = str(data['documento']).strip()
        if not doc:
            return jsonify({'message': 'El documento no puede estar vacío'}), 400
        existente = Clientes.get_by_documento(doc)
        if existente and existente.id_cliente != id:
            return jsonify({'message': f'El documento {doc} ya pertenece a otro cliente'}), 400
        cli.documento = doc

    if 'telefono' in data:
        cli.telefono = str(data['telefono']).strip()

    if 'direccion' in data:
        cli.direccion = str(data['direccion']).strip()

    cli.save()
    return jsonify({'message': 'Cliente actualizado exitosamente'}), 200

# DELETE
@clientes_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(id):
    cli = Clientes.get_by_id(id)
    if cli:
        cli.delete()
        return jsonify({'message': 'Cliente eliminado exitosamente'}), 200
    return jsonify({'message': 'Cliente no encontrado'}), 404