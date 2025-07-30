from pydantic import BaseModel
from typing import Optional
from datetime import date

class Reserva(BaseModel):
    id_reserva: int
    status: str
    data_checkin: date
    data_checkout: date
    valor_total: float
    qtd_hospedes: int
    id_quarto: int
    id_hospedagem: int
    cpf_usuario: str

class ReservaUpdate(BaseModel):
    status: Optional[str] = None
    data_checkin: Optional[date] = None
    data_checkout: Optional[date] = None
    valor_total: Optional[float] = None
    qtd_hospedes: Optional[int] = None
    id_quarto: Optional[int] = None
    id_hospedagem: Optional[int] = None

class ReservaViwew(BaseModel): #Referente a vissão de reserva
    id_reserva: int
    status: str
    data_checkin: date
    data_checkout: date
    valor_total: float
    qtd_hospedes: int
    id_quarto: int
    id_hospedagem: int
    cpf: str
    nome_usuario: str

class Hospedagem(BaseModel):
    id_hospedagem: int
    nome: str
    avaliacao_media: float
    tipo: str
    descricao: str
    fk_endereco: int

class HospedagemUpdate(BaseModel):
    nome: Optional[str] = None
    avaliacao_media: Optional[float] = None
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    fk_endereco: Optional[int] = None

class HospedagemDetalhes(BaseModel):#Referente a vissão de hospedagem
    id_hospedagem: int
    nome_hospedagem: str
    tipo_hospedagem: str
    id_quarto: int
    tipo_quarto: str
    descricao_quarto: str
    estado: str
    pais: str
    cep: str


class Avaliacao(BaseModel):
    id_avaliacao: int
    nota: float
    comentario: str
    cpf_usuario: str
    id_hospedagem: int

class AvaliacoesPorHospedagem(BaseModel):#Referente a vissão de avaliações
    id_hospedagem: int
    nome_hospedagem: str
    tipo: str
    total_avaliacoes: int
    media_nota: Optional[float] = None
    exemplo_comentario: Optional[str] = None
    estado: str
    pais: str

class AvaliacoesUpdate(BaseModel):
    nota: Optional[float] = None
    comentario: Optional[str] = None
    cpf_usuario: Optional[str] = None
    id_hospedagem: Optional[int] = None

