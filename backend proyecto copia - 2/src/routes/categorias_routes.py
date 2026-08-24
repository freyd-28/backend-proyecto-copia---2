from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.models.categorias import Categorias
from src.utils.auth import token_required, rol_required

categorias_bp = Blueprint("categorias", __name__)


def serializar(cat):
    return {
        "id_categoria": cat.id_categoria,
        "nombre": cat.nombre,
        "creado_en": cat.creado_en.strftime("%Y-%m-%d %H:%M:%S")
        if cat.creado_en else None,
    }


@categorias_bp.route("/", methods=["GET"])
@token_required
def get_categorias():
    return jsonify([serializar(cat) for cat in Categorias.get()]), 200


@categorias_bp.route("/<int:id>", methods=["GET"])
@token_required
def get_categoria(id):
    cat = Categorias.get_by_id(id)
    if not cat:
        return jsonify({"message": "Categoría no encontrada"}), 404
    return jsonify(serializar(cat)), 200


@categorias_bp.route("/", methods=["POST"])
@token_required
@rol_required("Administrador")
def create_categoria():
    data = request.get_json(silent=True) or {}
    nombre = str(data.get("nombre", "")).strip()
    if not nombre:
        return jsonify({"message": "El nombre de la categoría es obligatorio"}), 400
    if any(c.nombre.lower() == nombre.lower() for c in Categorias.get()):
        return jsonify({"message": "La categoría ya existe"}), 409

    categoria = Categorias(nombre=nombre)
    try:
        categoria.save()
    except IntegrityError:
        from src.models import session
        session.rollback()
        return jsonify({"message": "No fue posible crear la categoría"}), 409

    return jsonify({
        "message": "Categoría creada exitosamente",
        "id_categoria": categoria.id_categoria,
    }), 201


@categorias_bp.route("/<int:id>", methods=["PUT"])
@token_required
@rol_required("Administrador")
def update_categoria(id):
    cat = Categorias.get_by_id(id)
    if not cat:
        return jsonify({"message": "Categoría no encontrada"}), 404

    nombre = str((request.get_json(silent=True) or {}).get("nombre", "")).strip()
    if not nombre:
        return jsonify({"message": "El nombre de la categoría no puede estar vacío"}), 400

    existente = next(
        (c for c in Categorias.get()
         if c.id_categoria != id and c.nombre.lower() == nombre.lower()),
        None,
    )
    if existente:
        return jsonify({"message": "La categoría ya existe"}), 409

    cat.nombre = nombre
    cat.save()
    return jsonify({"message": "Categoría actualizada exitosamente"}), 200


@categorias_bp.route("/<int:id>", methods=["DELETE"])
@token_required
@rol_required("Administrador")
def delete_categoria(id):
    cat = Categorias.get_by_id(id)
    if not cat:
        return jsonify({"message": "Categoría no encontrada"}), 404

    # Evita borrar categorías utilizadas por productos.
    if getattr(cat, "productos", None):
        return jsonify({"message": "No se puede eliminar una categoría que tiene productos asociados"}), 409

    try:
        cat.delete()
    except IntegrityError:
        from src.models import session
        session.rollback()
        return jsonify({"message": "No se puede eliminar la categoría porque tiene productos asociados"}), 409

    return jsonify({"message": "Categoría eliminada exitosamente"}), 200
