from sqlalchemy import Column, Integer, String, ForeignKey
from src.models import session
from .persona import Persona


class Clientes(Persona):
   
    __tablename__ = 'cliente'

    id_cliente = Column(Integer, ForeignKey('persona.id_persona'), primary_key=True)
    documento = Column(String(20), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(150), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'cliente',
    }

    def __init__(self, nombre: str, documento: str, telefono: str = "", direccion: str = ""):
        super().__init__(nombre)
        self.documento = documento
        self.telefono = telefono
        self.direccion = direccion

    #  MÉTODOS DE CONSULTA (CRUD) 

    @staticmethod
    def get():
        """Obtiene la lista completa de clientes inscritos."""
        return session.query(Clientes).all()

    @staticmethod
    def get_by_id(id_cliente: int):
        """Busca un cliente específico por su ID primario."""
        return session.query(Clientes).filter_by(id_cliente=id_cliente).first()

    @staticmethod
    def get_by_documento(documento: str):
        """Busca un cliente por su número de documento o NIT."""
        return session.query(Clientes).filter_by(documento=documento).first()

    def __repr__(self):
        return f"<Clientes(id={self.id_cliente}, nombre='{self.nombre}', documento='{self.documento}')>"