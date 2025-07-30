from pydantic import BaseModel
from typing import Optional
from datetime import date

class Usuario(BaseModel):
    cpf: str
    nome: str
    senha: str
    data_cadastro: date

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    senha: Optional[str] = None
    data_cadrastro: Optional[str] = None 

class Favoritos(BaseModel):
    cpf_usuario: str
    id_hospedagem: int
    data_favorito: date

class FavoritoUpdate(BaseModel):
    id_hospedagem: Optional[int] = None
    data_favorito: Optional[str] = None 

class FavoritadoporUsuario(BaseModel):
    cpf: str
    nome_usuario: str
    data_favorito: date
    id_hospedagem: int
    nome_hospedagem: str