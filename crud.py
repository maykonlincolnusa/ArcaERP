from sqlalchemy.orm import Session
from . import models

def get_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def get_cliente(db: Session, cliente_id: int):
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()

def create_cliente(db: Session, cliente: dict):
    db_cliente = models.Cliente(**cliente)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, cliente_id: int, cliente_data: dict):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        for key, value in cliente_data.items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, cliente_id: int):
    db_cliente = get_cliente(db, cliente_id)
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
    return db_cliente

# CRUD para Contato
def get_contatos(db: Session, cliente_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Contato).filter(models.Contato.cliente_id == cliente_id).offset(skip).limit(limit).all()

def get_contato(db: Session, contato_id: int):
    return db.query(models.Contato).filter(models.Contato.id == contato_id).first()

def create_contato(db: Session, contato: dict):
    db_contato = models.Contato(**contato)
    db.add(db_contato)
    db.commit()
    db.refresh(db_contato)
    return db_contato

def update_contato(db: Session, contato_id: int, contato_data: dict):
    db_contato = get_contato(db, contato_id)
    if db_contato:
        for key, value in contato_data.items():
            setattr(db_contato, key, value)
        db.commit()
        db.refresh(db_contato)
    return db_contato

def delete_contato(db: Session, contato_id: int):
    db_contato = get_contato(db, contato_id)
    if db_contato:
        db.delete(db_contato)
        db.commit()
    return db_contato

# CRUD para Mensagem
def create_mensagem(db: Session, mensagem: dict):
    db_mensagem = models.Mensagem(**mensagem)
    db.add(db_mensagem)
    db.commit()
    db.refresh(db_mensagem)
    return db_mensagem

def get_mensagens_by_cliente(db: Session, cliente_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Mensagem).filter(models.Mensagem.cliente_id == cliente_id).offset(skip).limit(limit).all()

def update_mensagem_status(db: Session, mensagem_id: int, status: str):
    db_mensagem = db.query(models.Mensagem).filter(models.Mensagem.id == mensagem_id).first()
    if db_mensagem:
        db_mensagem.status = status
        db.commit()
        db.refresh(db_mensagem)
    return db_mensagem
