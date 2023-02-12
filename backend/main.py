from fastapi import FastAPI
from fastapi.middleware.cors import (
     CORSMiddleware
)
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from sqlalchemy.orm import Session

# Importa classes para persistencia dos dados no SQLite
import crud, models
from schemas import UserModel
from database import SessionLocal, engine

from service import Service

# Importar MovieUtils e Genre para usar na api do TMDB
from tmdb.models import Genre
from tmdb.api_utils import (
    RequestApi, MovieUtils
)
app = FastAPI()

# habilita CORS (permite que o Svelte acesse o fastapi)
origins = [
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8001"
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# todo: testar para ver se o banco nao esta sendo 
# apagado toda vez que inicia o fastapi
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =============================
# USER (sqlite)
# =============================

# /user/create
@app.post("/user/create")
def create_user(user: UserModel, db: Session = Depends(get_db)):
    # verifica se ja nao um usuario com este email
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="Email already registered"
        )
    # faz o insert no banco
    new_user = crud.create_user(db=db, user=user)
    # print(new_user)
    return new_user

# /user/list
@app.get("/user/list")
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

# /user/delete
@app.delete("/user/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.delete_user(db, user_id)
    return user

# /user/update
@app.put("/user/update/{user_id}")
def update_user(user_id: int, user: UserModel, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, user)
    return user

# =============================
# MOVIE (tmdb)
# =============================

@app.get("/genres")
async def get_genres():
    return Service.get_genres()

@app.get("/movies")
async def get_movies():
    # chamar a classe MovieUtils para consultar TMDB
    movies = MovieUtils.get_movies(Genre.Scifi.value)
    return movies

@app.get("/artista/name/{name}")
async def get_artista_by_name(name):
    artista = RequestApi.get_artista_by_name(name)

    if not artista:
        raise HTTPException(status_code=404, detail=f"No person found with name = {name}")

    return artista

@app.get("/artista/id/{id}")
async def get_artista(id):
    artista = RequestApi.get_artista(id)
    if "name" not in artista: 
        raise HTTPException(status_code=404, detail="No person found with id = {id}")
    return {
        "id": artista['id'],
        "name": artista['name'],
        "popularity": artista['popularity'],
        "profile_path": artista['profile_path'],
    }

# implementar endpoint que receba nome do artista

# Objetivo: Implementar o endpoint para 
# encontrar artistas pelo nome fornecido como 
# parametro na url.
# - Retorna uma lista de artistas.
# - Exemplo de endpoint na nossa API:
# /artista/name/arnold

@app.get("/find/{title}/{genre}")
async def find(title: str, genre):
    import json
    data = json.load(open('filmes.json'))
    encontrou = []
    for filme in data:
        # in - contains (ou contem um substring)
        if title.lower() in filme['title'].lower():
            # append - adiciona na lista
            encontrou.append(filme)
    return encontrou

@app.get("/")  # HTTP GET
async def home():
    return {"msg": "pycine back-end"}

# rodar o fastapi:
# uvicorn main:app --reload

# pip install -r requirements.txt
# source env/
# pip install fastapi uvicorn
