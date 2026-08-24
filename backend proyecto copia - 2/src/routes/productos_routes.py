from flask import Blueprint, request, jsonify
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.utils.auth import token_required

productos_bp = Blueprint('productos', __name__)

# READ ALL
@productos_bp.route('/', methods=['GET'])
@token_required
def get_productos():
    productos = Productos.get()
    productos_list = []
    for prod in productos:
        productos_list.append({
            'id_producto': prod.id_producto,
            'nombre': prod.nombre,
            'precio_venta': prod.precio_venta,
            'id_categoria': prod.id_categoria,
            'activo': prod.activo,
            'creado_en': prod.creado_en.strftime('%Y-%m-%d %H:%M:%S') if prod.creado_en else None
        })
    return jsonify(productos_list), 200

# READ ONE
@productos_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_producto(id):
    prod = Productos.get_by_id(id)
    if prod:
        return jsonify({
            'id_producto': prod.id_producto,
            'nombre': prod.nombre,
            'precio_venta': prod.precio_venta,
            'id_categoria': prod.id_categoria,
            'activo': prod.activo,
            'creado_en': prod.creado_en.strftime('%Y-%m-%d %H:%M:%S') if prod.creado_en else None
        }), 200
    return jsonify({'message': 'Producto no encontrado'}), 404

# CREATE
@productos_bp.route('/', methods=['POST'])
@token_required
def create_producto():
    data = request.get_json() or {}
    
    # 1. Validación del nombre
    nombre = str(data.get('nombre', '')).strip()
    if not nombre:
        return jsonify({'message': 'El nombre del producto es obligatorio'}), 400
    
    # 2. Validación del precio
    try:
        precio = float(data.get('precio_venta', 0))
        if precio <= 0:
            return jsonify({'message': 'El precio debe ser un número mayor a cero'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'El precio ingresado debe ser un número válido'}), 400

    # 3. Validación de la categoría asociada
    try:
        id_categoria = int(data.get('id_categoria', 0))
        if id_categoria <= 0:
            return jsonify({'message': 'El ID de la categoría no es válido'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'El ID de la categoría debe ser un número entero'}), 400

    # Verificar existencia de la categoría en la DB
    if not Categorias.get_by_id(id_categoria):
        return jsonify({'message': f'La categoría con ID {id_categoria} no existe'}), 404

    # 4. Instancia y guardado
    try:
        activo = int(data.get('activo', 1))
    except (ValueError, TypeError):
        return jsonify({'message': 'El estado activo debe ser 0 o 1'}), 400

    if activo not in (0, 1):
        return jsonify({'message': 'El estado activo debe ser 0 o 1'}), 400

    producto = Productos(
        nombre=nombre,
        precio_venta=precio,
        id_categoria=id_categoria,
        activo=activo
    )
    
    producto.save()
    return jsonify({
        'message': 'Producto creado exitosamente',
        'id_producto': producto.id_producto
    }), 201

# UPDATE
@productos_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_producto(id):
    prod = Productos.get_by_id(id)
    if not prod:
        return jsonify({'message': 'Producto no encontrado'}), 404
        
    data = request.get_json() or {}

    # Actualización condicional del nombre
    if 'nombre' in data:
        nombre = str(data['nombre']).strip()
        if not nombre:
            return jsonify({'message': 'El nombre del producto no puede estar vacío'}), 400
        prod.nombre = nombre

    # Actualización condicional del precio
    if 'precio_venta' in data:
        try:
            precio = float(data['precio_venta'])
            if precio <= 0:
                return jsonify({'message': 'El precio debe ser mayor a cero'}), 400
            prod.precio_venta = precio
        except (ValueError, TypeError):
            return jsonify({'message': 'El precio debe ser un número válido'}), 400

    # Actualización condicional de la categoría
    if 'id_categoria' in data:
        try:
            id_cat = int(data['id_categoria'])
            if not Categorias.get_by_id(id_cat):
                return jsonify({'message': f'La categoría con ID {id_cat} no existe'}), 404
            prod.id_categoria = id_cat
        except (ValueError, TypeError):
            return jsonify({'message': 'El ID de la categoría debe ser un número entero'}), 400

    # Actualización del estado activo
    if 'activo' in data:
        try:
            activo = int(data['activo'])
        except (ValueError, TypeError):
            return jsonify({'message': 'El estado activo debe ser 0 o 1'}), 400
        if activo not in (0, 1):
            return jsonify({'message': 'El estado activo debe ser 0 o 1'}), 400
        prod.activo = activo

    prod.save()
    return jsonify({'message': 'Producto actualizado exitosamente'}), 200

# DELETE
@productos_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_producto(id):
    prod = Productos.get_by_id(id)
    if prod:
        prod.delete()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    return jsonify({'message': 'Producto no encontrado'}), 404