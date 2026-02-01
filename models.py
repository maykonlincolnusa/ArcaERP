# Modelo de Mensagem para WhatsApp
from datetime import datetime

class Mensagem(Base):
    __tablename__ = "mensagens"
    id = Column(Integer, primary_key=True, index=True)
    contato_id = Column(Integer, ForeignKey("contatos.id"))
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    texto = Column(String)
    status = Column(String, default="pendente")
    data_envio = Column(String, default=lambda: datetime.utcnow().isoformat())
    contato = relationship("Contato")
    cliente = relationship("Cliente")
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    endereco = Column(String)
    status = Column(String, default="ativo")

# Novo modelo de Contato
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Contato(Base):
    __tablename__ = "contatos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    telefone = Column(String, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    cliente = relationship("Cliente")
