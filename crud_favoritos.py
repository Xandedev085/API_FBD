from fastapi import APIRouter, HTTPException
from db import get_read_connection, get_admin_connection
from models2 import Favoritos,FavoritoUpdate,FavoritadoporUsuario
from typing import List

router= APIRouter()

@router.get("/listar", response_model=List[FavoritadoporUsuario])
async def listar_usuarios():
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf, nome_usuario, data_favorito, id_hospedagem, nome_hospedagem FROM vw_favoritos_usuarios")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        FavoritadoporUsuario(
            cpf=r[0], nome_usuario=r[1], data_favorito=r[2], 
            id_hospedagem=r[3], nome_hospedagem=r[4]
        )
        for r in rows
    ]

@router.post("/criar")
async def criar_usuario(fav: Favoritos):
    conn = get_admin_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO favoritos (cpf_usuario, id_hospedagem, data_favorito) VALUES (%s,%s,%s)",
            (
                fav.cpf_usuario, fav.id_hospedagem, fav.data_favorito
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao Favoritar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuario favoritou com sucesso"}

@router.get("/buscar/{cpf}")
async def get_usuario(cpf: str):
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf, nome_usuario, data_favorito, id_hospedagem, nome_hospedagem FROM vw_favoritos_usuarios WHERE cpf=%s", (cpf,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return FavoritadoporUsuario(
            cpf=row[0], nome_usuario=row[1], data_favorito=row[2], 
            id_hospedagem=row[3], nome_hospedagem=row[4]
        ).dict()
    raise HTTPException(404, "Usuario não encontrado")

@router.patch("/atualizar/{cpf_usuario}")
async def atualizar_usuario_parcial(cpf_usuario: str, fav: FavoritoUpdate):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf_usuario FROM favoritos WHERE cpf_usuario=%s", (cpf_usuario,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Usuario não encontrado")
    fields = []
    values = []
    for campo, valor in fav.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(cpf_usuario)
    try:
        cur.execute(f"UPDATE favoritos SET {', '.join(fields)} WHERE cpf_usuario=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Favorito atualizado"}

@router.delete("/deletar/{cpf_usuario}")
async def deletar_usuario(cpf_usuario: str):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM favoritos WHERE cpf_usuario=%s", (cpf_usuario,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Favorito removido"}