from fastapi import APIRouter, HTTPException
from db import get_read_connection, get_admin_connection
from models2 import Usuario,UsuarioUpdate
from typing import List

router= APIRouter()

@router.get("/listar", response_model=List[Usuario])
async def listar_usuarios():
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf, nome, senha, data_cadastro FROM usuario")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        Usuario(
            cpf=r[0], nome=r[1], senha=r[2], 
            data_cadastro=r[3]
        )
        for r in rows
    ]

@router.post("/criar")
async def criar_usuario(user: Usuario):
    conn = get_admin_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuario (cpf, nome, senha, data_cadastro) VALUES (%s,%s,%s,%s)",
            (
                user.cpf, user.nome, user.senha, user.data_cadastro
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar Usuario: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuario criado com sucesso"}

@router.get("/buscar/{cpf}")
async def get_usuario(cpf: str):
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf, nome, senha, data_cadastro FROM usuario WHERE cpf=%s", (cpf,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return Usuario(
            cpf=row[0], nome=row[1], senha=row[2], 
            data_cadastro=row[3]
        ).dict()
    raise HTTPException(404, "Usuario não encontrado")

@router.patch("/atualizar/{cpf}")
async def atualizar_usuario_parcial(cpf: str, user: UsuarioUpdate):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("SELECT cpf FROM usuario WHERE cpf=%s", (cpf,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Usuario não encontrado")
    fields = []
    values = []
    for campo, valor in user.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(cpf)
    try:
        cur.execute(f"UPDATE usuario SET {', '.join(fields)} WHERE cpf=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Usuario atualizado"}

@router.delete("/deletar/{cpf}")
async def deletar_usuario(cpf: str):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE cpf=%s", (cpf,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Usuario removido"}