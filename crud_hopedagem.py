from fastapi import APIRouter, HTTPException
from db import get_read_connection, get_admin_connection
from models import Hospedagem,HospedagemDetalhes,HospedagemUpdate
from typing import List

router= APIRouter()

@router.get("/listar", response_model=List[HospedagemDetalhes])
async def listar_hospedagem():
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_hospedagem, nome_hospedagem, tipo_hospedagem, id_quarto, tipo_quarto, descricao_quarto, estado, pais, cep FROM vw_hospedagem_detalhes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        HospedagemDetalhes(
            id_hospedagem=r[0], nome_hospedagem=r[1], tipo_hospedagem=r[2], id_quarto=r[3],
            tipo_quarto=r[4], descricao_quarto=r[5], estado=r[6],
            pais=r[7], cep=r[8]
        )
        for r in rows
    ]

@router.post("/criar")
async def criar_hopedagem(hos: Hospedagem):
    conn = get_admin_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO hospedagem (id_hospedagem, nome, avaliacao_media, tipo, descricao,fk_endereco) VALUES (%s,%s,%s,%s,%s,%s)",
            (
                hos.id_hospedagem, hos.nome, hos.avaliacao_media, hos.tipo, hos.descricao,
                hos.fk_endereco
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar hospedagem: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Hospedagem criada com sucesso"}

@router.get("/buscar/{id_hospedagem}")
async def get_hospedagem(id_hospedagem: int):
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_hospedagem, nome_hospedagem, tipo_hospedagem, id_quarto, tipo_quarto,descricao_quarto, estado, pais, cep FROM vw_hospedagem_detalhes WHERE id_hospedagem=%s", (id_hospedagem,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return HospedagemDetalhes(
            id_hospedagem=row[0], nome_hospedagem=row[1], tipo_hospedagem=row[2], id_quarto=row[3],
            tipo_quarto=row[4], descricao_quarto=row[5], estado=row[6],
            pais=row[7], cep=row[8]
        ).dict()
    raise HTTPException(404, "Hospedagem não encontrada")

@router.patch("/atualizar/{id_hospedagem}")
async def atualizar_hospedagem_parcial(id_hospedagem: int, hos: HospedagemUpdate):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_hospedagem FROM hospedagem WHERE id_hospedagem=%s", (id_hospedagem,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Hospedagem não encontrado")
    fields = []
    values = []
    for campo, valor in hos.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(id_hospedagem)
    try:
        cur.execute(f"UPDATE hospedagem SET {', '.join(fields)} WHERE id_hospedagem=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Hospedagem atualizada"}

@router.delete("/deletar/{id_hospedagem}")
async def deletar_hospedagem(id_hospedagem: int):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM hospedagem WHERE id_hospedagem=%s", (id_hospedagem,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Hospedagem removida"}