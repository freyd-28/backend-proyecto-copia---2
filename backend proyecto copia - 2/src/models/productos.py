from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from src.models import Base, session


class Productos(Base):
    
    __tablename__ = 'producto'

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120), nullable=False)
    precio_venta = Column(Float, nullable=False)
    id_categoria = Column(Integer, ForeignKey('categoria.id_categoria'), nullable=False)
    activo = Column(Integer, default=1)
    creado_en = Column(DateTime, default=datetime.now)

    def __init__(self, nombre: str, precio_venta: float, id_categoria: int, activo: int = 1):
        self.nombre = nombre
        self.precio_venta = precio_venta
        self.id_categoria = id_categoria
        self.activo = activo

    # --- MÉTODOS DE PERSISTENCIA Y CONSULTA (CRUD) ---

    def save(self):
        """Guarda o actualiza el producto actual en la base de datos."""
        session.add(self)
        session.commit()

    def delete(self):
        """Elimina el producto actual de la base de datos."""
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        """Obtiene el listado completo de productos."""
        return session.query(Productos).all()

    @staticmethod
    def get_by_id(id_producto: int):
        """Busca un producto específico por su ID primario."""
        return session.query(Productos).filter_by(id_producto=id_producto).first()

    def __repr__(self):
        return f"<Productos(id={self.id_producto}, nombre='{self.nombre}', precio={self.precio_venta})>"