# Mensagem schemas
class MensagemBase(BaseModel):
    contato_id: int
    cliente_id: int
    texto: str

class MensagemCreate(MensagemBase):
    pass

class MensagemOut(MensagemBase):
    id: int
    status: str
    data_envio: str
    class Config:
        orm_mode = True

# Envio de mensagem (simulação WhatsApp)
@app.post("/mensagens/", response_model=MensagemOut)
def enviar_mensagem(mensagem: MensagemCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    # Aqui seria feita a integração real com API WhatsApp
    # Para MVP, registra como enviada e status pendente
    msg = crud.create_mensagem(db, {**mensagem.dict(), "status": "enviada"})
    return msg

# Listar mensagens por cliente
@app.get("/mensagens/{cliente_id}", response_model=List[MensagemOut])
def listar_mensagens(cliente_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.get_mensagens_by_cliente(db, cliente_id)

# Webhook para atualizar status da mensagem (simulação)
@app.post("/webhook/mensagem_status/")
def webhook_status(mensagem_id: int, status: str, db: Session = Depends(get_db)):
    msg = crud.update_mensagem_status(db, mensagem_id, status)
    if not msg:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return {"ok": True, "status": msg.status}

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, crud, database
from pydantic import BaseModel
from typing import List, Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI()

# JWT Config
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: database.SessionLocal())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user


# User schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    is_admin: Optional[bool] = False

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
    class Config:
        orm_mode = True

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

# Cliente schemas

# Contato schemas
class ContatoBase(BaseModel):
    nome: str
    telefone: str

class ContatoCreate(ContatoBase):
    cliente_id: int

class ContatoOut(ContatoBase):
    id: int
    cliente_id: int
    class Config:
        orm_mode = True

# Cliente schemas
class ClienteBase(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    status: Optional[str] = "ativo"

class ClienteCreate(ClienteBase):
    pass

class ClienteOut(ClienteBase):
    id: int
    class Config:
        orm_mode = True

# Rotas CRUD para Contato
@app.post("/contatos/", response_model=ContatoOut)
def criar_contato(contato: ContatoCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.create_contato(db, contato.dict())

@app.get("/contatos/{cliente_id}", response_model=List[ContatoOut])
def listar_contatos(cliente_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.get_contatos(db, cliente_id)

@app.put("/contatos/{contato_id}", response_model=ContatoOut)
def atualizar_contato(contato_id: int, contato: ContatoBase, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_contato = crud.update_contato(db, contato_id, contato.dict())
    if not db_contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return db_contato

@app.delete("/contatos/{contato_id}")
def deletar_contato(contato_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_contato = crud.delete_contato(db, contato_id)
    if not db_contato:
        raise HTTPException(status_code=404, detail="Contato não encontrado")
    return {"ok": True}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter((models.User.username == user.username) | (models.User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário ou e-mail já cadastrado")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/clientes/", response_model=ClienteOut)
def criar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.create_cliente(db, cliente.dict())


@app.get("/clientes/", response_model=List[ClienteOut])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    return crud.get_clientes(db, skip=skip, limit=limit)


@app.get("/clientes/{cliente_id}", response_model=ClienteOut)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    cliente = crud.get_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@app.put("/clientes/{cliente_id}", response_model=ClienteOut)
def atualizar_cliente(cliente_id: int, cliente: ClienteCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_cliente = crud.update_cliente(db, cliente_id, cliente.dict())
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente


@app.delete("/clientes/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_cliente = crud.delete_cliente(db, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"ok": True}
