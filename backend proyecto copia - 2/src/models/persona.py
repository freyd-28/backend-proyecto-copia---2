from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from src.models import Base, session


class Persona(Base):
    
    __tablename__ = 'persona'

    id_persona = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(120), nullable=False)
    creado_en = Column(DateTime, default=datetime.now)
    tipo_persona = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': tipo_persona,
        'polymorphic_identity': 'persona'
    }

    def __init__(self, nombre: str):
        self.nombre = nombre

    def save(self):
        """Guarda o actualiza el registro actual en la base de datos."""
        session.add(self)
        session.commit()

    def delete(self):
        """Elimina el registro actual de la base de datos."""
        session.delete(self)
        session.commit()

    @staticmethod
    def get_all():
        """Obtiene el listado completo de registros base."""
        return session.query(Persona).all()

    @staticmethod
    def get_by_id(id_persona: int):
        """Obtiene una persona por su ID primario."""
        return session.query(Persona).filter_by(id_persona=id_persona).first()

    def __repr__(self):
        return f"<Persona(id={self.id_persona}, nombre='{self.nombre}', tipo='{self.tipo_persona}')>"