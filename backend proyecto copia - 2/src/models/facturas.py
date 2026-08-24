from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from src.models import Base, session


class Facturas(Base):
   
    __tablename__ = 'factura'

    id_factura = Column(Integer, primary_key=True, autoincrement=True)
    numero_factura = Column(String(20), unique=True, nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'), nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    estado = Column(String(50), nullable=False)
    total = Column(Float, nullable=False)

    def __init__(self, numero_factura: str, id_cliente: int, id_usuario: int, estado: str = 'generada', total: float = 0.0):
        self.numero_factura = numero_factura
        self.id_cliente = id_cliente
        self.id_usuario = id_usuario
        self.estado = estado
        self.total = total

    #  MÉTODOS DE CONSULTA (CRUD) 

    def save(self):
        """Guarda o actualiza la factura actual en la base de datos."""
        session.add(self)
        session.commit()

    def delete(self):
        """Elimina el registro de la factura de la base de datos."""
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        """Obtiene el listado completo de facturas."""
        return session.query(Facturas).all()

    @staticmethod
    def get_by_id(id_factura: int):
        """Busca una factura por su ID primario."""
        return session.query(Facturas).filter_by(id_factura=id_factura).first()

    @staticmethod
    def get_by_numero(numero_factura: str):
        """Busca una factura por su código/número consecutivo."""
        return session.query(Facturas).filter_by(numero_factura=numero_factura).first()
    def calcular_total(self):
        from src.models.factura_detalle import FacturaDetalle

        detalles = FacturaDetalle.get_by_factura(self.id_factura)

        self.total = sum(det.subtotal for det in detalles)

        return self.total
    def __repr__(self):
        return f"<Facturas(id={self.id_factura}, numero='{self.numero_factura}', total={self.total}, estado='{self.estado}')>"