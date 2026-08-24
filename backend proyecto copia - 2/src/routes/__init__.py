from .auth_routes import auth_bp
from .categorias_routes import categorias_bp
from .clientes_routes import clientes_bp
from .facturas_routes import facturas_bp
from .factura_detalle_routes import factura_detalle_bp
from .productos_routes import productos_bp
from .usuarios_routes import usuarios_bp

all_blueprints = [
    auth_bp,
    categorias_bp,
    clientes_bp,
    facturas_bp,
    factura_detalle_bp,
    productos_bp,
    usuarios_bp
]