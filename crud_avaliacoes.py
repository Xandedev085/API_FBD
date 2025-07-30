from fastapi import APIRouter, HTTPException
from db import get_read_connection, get_admin_connection
from models import Avaliacao,AvaliacoesPorHospedagem,AvaliacoesUpdate
from typing import List

router= APIRouter()

@router.get("/listar", response_model=List[AvaliacoesPorHospedagem])
async def listar_avaliacoes():
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_hospedagem, nome_hospedagem, tipo, total_avaliacoes, media_nota, exemplo_comentario, estado, pais FROM vw_avaliacoes_por_hospedagem")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        AvaliacoesPorHospedagem(
            id_hospedagem=r[0], nome_hospedagem=r[1], tipo=r[2], total_avaliacoes=r[3],
            media_nota=r[4], exemplo_comentario=r[5], estado=r[6], 
            pais=r[7]
        )
        for r in rows
    ]

@router.post("/criar")
async def criar_avaliacao(ava: Avaliacao):
    conn = get_admin_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO avaliacao (id_avaliacao, nota, comentario, cpf_usuario, id_hospedagem) VALUES (%s,%s,%s,%s,%s)",
            (
                ava.id_avaliacao, ava.nota, ava.comentario, ava.cpf_usuario, ava.id_hospedagem
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar avaliacao: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Avaliacao criada com sucesso"}

@router.get("/buscar/{id_hospedagem}")
async def get_hospedagem(id_hospedagem: int):
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_hospedagem, nome_hospedagem, tipo, total_avaliacoes, media_nota,exemplo_comentario, estado, pais FROM vw_avaliacoes_por_hospedagem WHERE id_hospedagem=%s", (id_hospedagem,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return AvaliacoesPorHospedagem(
            id_hospedagem=row[0], nome_hospedagem=row[1], tipo=row[2], total_avaliacoes=row[3],
            media_nota=row[4], exemplo_comentario=row[5], estado=row[6],
            pais=row[7]
        ).dict()
    raise HTTPException(404, "Hospedagem não encontrada")

@router.patch("/atualizar/{id_avaliacao}")
async def atualizar_hospedagem_parcial(id_avaliacao: int, ava: AvaliacoesUpdate):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_avaliacao FROM avaliacao WHERE id_avaliacao=%s", (id_avaliacao,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Avaliacao não encontrada")
    fields = []
    values = []
    for campo, valor in ava.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(id_avaliacao)
    try:
        cur.execute(f"UPDATE avaliacao SET {', '.join(fields)} WHERE id_avaliacao=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Avaliacao atualizada"}

@router.delete("/deletar/{id_avaliacao}")
async def deletar_hospedagem(id_avaliacao: int):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM avaliacao WHERE id_avaliacao=%s", (id_avaliacao,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Avaliacao removida"}