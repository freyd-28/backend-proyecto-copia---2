from flask import Blueprint, request, jsonify
from src.models.factura_detalle import FacturaDetalle
from src.models.facturas import Facturas
from src.models.productos import Productos
from src.utils.auth import token_required

factura_detalle_bp = Blueprint('factura_detalle', __name__)


@factura_detalle_bp.route('/', methods=['GET'])
@token_required
def get_detalles():
    detalles = FacturaDetalle.get()

    detalles_list = []

    for det in detalles:
        detalles_list.append({
            'id_detalle': det.id_detalle,
            'id_factura': det.id_factura,
            'id_producto': det.id_producto,
            'cantidad': det.cantidad,
            'precio_unitario': det.precio_unitario,
            'subtotal': det.subtotal
        })

    return jsonify(detalles_list), 200


@factura_detalle_bp.route('/factura/<int:id_factura>', methods=['GET'])
@token_required
def get_detalles_por_factura(id_factura):

    if not Facturas.get_by_id(id_factura):
        return jsonify({
            'message': 'Factura no encontrada'
        }), 404

    detalles = FacturaDetalle.get_by_factura(id_factura)

    detalles_list = []

    for det in detalles:
        detalles_list.append({
            'id_detalle': det.id_detalle,
            'id_factura': det.id_factura,
            'id_producto': det.id_producto,
            'cantidad': det.cantidad,
            'precio_unitario': det.precio_unitario,
            'subtotal': det.subtotal
        })

    return jsonify(detalles_list), 200


@factura_detalle_bp.route('/', methods=['POST'])
@token_required
def create_detalle():

    data = request.get_json() or {}

    id_factura = data.get('id_factura')
    id_producto = data.get('id_producto')

    try:
        cantidad = int(data.get('cantidad', 0))
        precio_unitario = float(data.get('precio_unitario', 0))
    except (ValueError, TypeError):
        return jsonify({
            'message': 'Cantidad y precio deben ser valores numéricos válidos'
        }), 400

    if cantidad <= 0:
        return jsonify({
            'message': 'La cantidad debe ser mayor a cero'
        }), 400

    if precio_unitario <= 0:
        return jsonify({
            'message': 'El precio debe ser mayor a cero'
        }), 400

    factura = Facturas.get_by_id(id_factura)

    if not factura:
        return jsonify({
            'message': 'La factura no existe'
        }), 404

    producto = Productos.get_by_id(id_producto)

    if not producto:
        return jsonify({
            'message': 'El producto no existe'
        }), 404

    detalle = FacturaDetalle(
        id_factura=id_factura,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario
    )

    detalle.save()

    # Recalcular total factura
    factura.calcular_total()
    factura.save()

    return jsonify({
        'message': 'Detalle agregado exitosamente',
        'id_detalle': detalle.id_detalle,
        'subtotal': detalle.subtotal,
        'total_factura': factura.total
    }), 201


@factura_detalle_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_detalle(id):

    det = FacturaDetalle.get_by_id(id)

    if not det:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    data = request.get_json() or {}

    id_factura = det.id_factura

    if 'cantidad' in data:

        try:
            cantidad = int(data['cantidad'])
        except (ValueError, TypeError):
            return jsonify({
                'message': 'La cantidad debe ser un entero válido'
            }), 400

        if cantidad <= 0:
            return jsonify({
                'message': 'La cantidad debe ser mayor a cero'
            }), 400

        det.cantidad = cantidad

    if 'precio_unitario' in data:

        try:
            precio = float(data['precio_unitario'])
        except (ValueError, TypeError):
            return jsonify({
                'message': 'El precio debe ser un número válido'
            }), 400

        if precio <= 0:
            return jsonify({
                'message': 'El precio debe ser mayor a cero'
            }), 400

        det.precio_unitario = precio

    if 'id_producto' in data:

        producto = Productos.get_by_id(data['id_producto'])

        if not producto:
            return jsonify({
                'message': 'El producto no existe'
            }), 404

        det.id_producto = producto.id_producto

    # Recalcular subtotal
    det.subtotal = det.cantidad * det.precio_unitario

    det.save()

    # Recalcular factura
    factura = Facturas.get_by_id(id_factura)

    if factura:
        factura.calcular_total()
        factura.save()

    return jsonify({
        'message': 'Detalle actualizado exitosamente',
        'id_detalle': det.id_detalle,
        'subtotal': det.subtotal,
        'total_factura': factura.total if factura else None
    }), 200


@factura_detalle_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_detalle(id):

    det = FacturaDetalle.get_by_id(id)

    if not det:
        return jsonify({
            'message': 'Detalle no encontrado'
        }), 404

    id_factura = det.id_factura

    det.delete()

    # Recalcular factura
    factura = Facturas.get_by_id(id_factura)

    if factura:
        factura.calcular_total()
        factura.save()

    return jsonify({
        'message': 'Detalle eliminado exitosamente',
        'total_factura': factura.total if factura else None
    }), 200