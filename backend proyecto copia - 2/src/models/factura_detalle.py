from sqlalchemy import Column, Integer, Float, ForeignKey
from src.models import Base, session


class FacturaDetalle(Base):
   
    __tablename__ = 'factura_detalle'

    id_detalle = Column(Integer, primary_key=True, autoincrement=True)
    id_factura = Column(Integer, ForeignKey('factura.id_factura'), nullable=False)
    id_producto = Column(Integer, ForeignKey('producto.id_producto'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    def __init__(self, id_factura: int, id_producto: int, cantidad: int, precio_unitario: float):
        self.id_factura = id_factura
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario

    # MÉTODOS DE CONSULTA (CRUD) 

    def save(self):
        """Guarda o actualiza el detalle actual en la base de datos."""
        session.add(self)
        session.commit()

    def delete(self):
        """Elimina el ítem del detalle de la base de datos."""
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        """Obtiene el listado completo de todos los detalles creados."""
        return session.query(FacturaDetalle).all()

    @staticmethod
    def get_by_id(id_detalle: int):
        """Busca un ítem de detalle por su ID primario."""
        return session.query(FacturaDetalle).filter_by(id_detalle=id_detalle).first()

    @staticmethod
    def get_by_factura(id_factura: int):
        """Obtiene todas las líneas de detalle pertenecientes a una factura específica."""
        return session.query(FacturaDetalle).filter_by(id_factura=id_factura).all()

    def __repr__(self):
        return f"<FacturaDetalle(id={self.id_detalle}, id_factura={self.id_factura}, id_producto={self.id_producto}, subtotal={self.subtotal})>"