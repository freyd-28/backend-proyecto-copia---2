from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.models import Base, session


class Categorias(Base):
    
    __tablename__ = 'categoria'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120), nullable=False)
    creado_en = Column(DateTime, default=datetime.now)

    def __init__(self, nombre: str):
        self.nombre = nombre

    # MÉTODOS CONSULTA (CRUD) 

    def save(self):
        """Guarda o actualiza la categoría actual en la base de datos."""
        session.add(self)
        session.commit()

    def delete(self):
        """Elimina la categoría actual de la base de datos."""
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        """Obtiene la lista completa de categorías."""
        return session.query(Categorias).all()

    @staticmethod
    def get_by_id(id_categoria: int):
        """Busca una categoría específica por su ID primario."""
        return session.query(Categorias).filter_by(id_categoria=id_categoria).first()

    def __repr__(self):
        return f"<Categorias(id={self.id_categoria}, nombre='{self.nombre}')>"