from flask import Blueprint, request, jsonify
from src.models.facturas import Facturas
from src.models.clientes import Clientes
from src.models.usuarios import Usuarios
from src.models.factura_detalle import FacturaDetalle
from src.utils.auth import token_required

facturas_bp = Blueprint('facturas', __name__)

# READ ALL
@facturas_bp.route('/', methods=['GET'])
@token_required
def get_facturas():
    facturas = Facturas.get()
    facturas_list = []
    for fac in facturas:
        facturas_list.append({
            'id_factura': fac.id_factura,
            'numero_factura': fac.numero_factura,
            'id_cliente': fac.id_cliente,
            'id_usuario': fac.id_usuario,
            'fecha': fac.fecha.strftime('%Y-%m-%d %H:%M:%S') if fac.fecha else None,
            'estado': fac.estado,
            'total': fac.total
        })
    return jsonify(facturas_list), 200

# READ ONE
@facturas_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_factura(id):
    fac = Facturas.get_by_id(id)
    if fac:
        return jsonify({
            'id_factura': fac.id_factura,
            'numero_factura': fac.numero_factura,
            'id_cliente': fac.id_cliente,
            'id_usuario': fac.id_usuario,
            'fecha': fac.fecha.strftime('%Y-%m-%d %H:%M:%S') if fac.fecha else None,
            'estado': fac.estado,
            'total': fac.total
        }), 200
    return jsonify({'message': 'Factura no encontrada'}), 404

# CREATE
@facturas_bp.route('/', methods=['POST'])
@token_required
def create_factura():
    data = request.get_json() or {}

    numero_factura = str(data.get('numero_factura', '')).strip()
    id_cliente = data.get('id_cliente')
    id_usuario = data.get('id_usuario')

    if not numero_factura:
        return jsonify({'message': 'El número de factura es obligatorio'}), 400
    if not id_cliente or not Clientes.get_by_id(id_cliente):
        return jsonify({'message': 'El cliente asociado no es válido o no existe'}), 400
    if not id_usuario or not Usuarios.get_by_id(id_usuario):
        return jsonify({'message': 'El usuario/vendedor no es válido o no existe'}), 400

    if Facturas.get_by_numero(numero_factura):
        return jsonify({'message': f'La factura {numero_factura} ya existe'}), 400

    factura = Facturas(
        numero_factura=numero_factura,
        id_cliente=id_cliente,
        id_usuario=id_usuario,
        estado=data.get('estado', 'generada'),
        total=float(data.get('total', 0.0))
    )

    factura.save()
    return jsonify({
        'message': 'Factura creada exitosamente',
        'id_factura': factura.id_factura
    }), 201

# UPDATE
@facturas_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_factura(id):
    fac = Facturas.get_by_id(id)
    if not fac:
        return jsonify({'message': 'Factura no encontrada'}), 404

    data = request.get_json() or {}

    if 'estado' in data:
        fac.estado = data['estado']
    if 'total' in data:
        try:
            fac.total = float(data['total'])
        except (ValueError, TypeError):
            return jsonify({'message': 'El total debe ser un número válido'}), 400

    fac.save()
    return jsonify({'message': 'Factura actualizada exitosamente'}), 200

# DELETE
@facturas_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_factura(id):
    fac = Facturas.get_by_id(id)
    if not fac:
        return jsonify({'message': 'Factura no encontrada'}), 404

    # Eliminar primero los detalles para respetar la FK factura_detalle -> factura.
    for detalle in FacturaDetalle.get_by_factura(id):
        detalle.delete()

    fac.delete()
    return jsonify({'message': 'Factura eliminada exitosamente'}), 200
    return jsonify({'message': 'Factura no encontrada'}), 404