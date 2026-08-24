from sqlalchemy import Column, Integer, String, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import Base, session
from .persona import Persona


class Usuarios(Persona):
    __tablename__ = "usuario"

    id_usuario = Column(Integer, ForeignKey("persona.id_persona"), primary_key=True)
    nombre_usuario = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="Vendedor")
    activo = Column(Integer, nullable=False, default=1)

    __mapper_args__ = {"polymorphic_identity": "usuario"}

    def __init__(self, nombre, nombre_usuario, email, password_hash,
                 rol="Vendedor", activo=1, password_hasheada=False):
        super().__init__(nombre)
        self.nombre_usuario = nombre_usuario
        self.email = email
        self.password_hash = (
            password_hash if password_hasheada
            else generate_password_hash(password_hash)
        )
        self.rol = rol
        self.activo = int(activo)

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)

    def establecer_password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "nombre_usuario": self.nombre_usuario,
            "email": self.email,
            "rol": self.rol,
            "activo": self.activo,
            "creado_en": self.creado_en.strftime("%Y-%m-%d %H:%M:%S")
            if self.creado_en else None,
        }

    def save(self):
        session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def get():
        return session.query(Usuarios).all()

    @staticmethod
    def get_by_id(id_usuario):
        return session.query(Usuarios).filter_by(id_usuario=id_usuario).first()

    @staticmethod
    def get_by_email(email):
        return session.query(Usuarios).filter_by(email=email).first()

    @staticmethod
    def get_by_username(nombre_usuario):
        return session.query(Usuarios).filter_by(nombre_usuario=nombre_usuario).first()

    def __repr__(self):
        return f"<Usuarios(id={self.id_usuario}, usuario='{self.nombre_usuario}', rol='{self.rol}')>"
