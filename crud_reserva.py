from fastapi import APIRouter, HTTPException
from db import get_read_connection, get_admin_connection
from models import Reserva,ReservaViwew,ReservaUpdate
from typing import List

router= APIRouter()

@router.get("/listar", response_model=List[ReservaViwew])
async def listar_reservas():
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_reserva, status, data_checkin, data_checkout, valor_total,qtd_hospedes, id_quarto, id_hospedagem, cpf, nome_usuario FROM vw_reservas_usuario")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        ReservaViwew(
            id_reserva=r[0], status=r[1], data_checkin=r[2], data_checkout=r[3],
            valor_total=r[4], qtd_hospedes=r[5], id_quarto=r[6],
            id_hospedagem=r[7], cpf=r[8], nome_usuario=r[9]
        )
        for r in rows
    ]

@router.post("/criar")
async def criar_reservas(res: Reserva):
    conn = get_admin_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO reserva (id_reserva, status, data_checkin, data_checkout, valor_total,qtd_hospedes, id_quarto, id_hospedagem, cpf_usuario) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                res.id_reserva, res.status, res.data_checkin, res.data_checkout, res.valor_total,
                res.qtd_hospedes, res.id_quarto, res.id_hospedagem, res.cpf_usuario
            )
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar reserva: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Reserva criada com sucesso"}

@router.get("/buscar/{cpf}")
async def get_reserva(cpf: str):
    conn = get_read_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_reserva, status, data_checkin, data_checkout, valor_total,qtd_hospedes, id_quarto, id_hospedagem, cpf, nome_usuario FROM vw_reservas_usuario WHERE cpf=%s", (cpf,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return ReservaViwew(
            id_reserva=row[0], status=row[1], data_checkin=row[2], data_checkout=row[3],
            valor_total=row[4], qtd_hospedes=row[5], id_quarto=row[6],
            id_hospedagem=row[7], cpf=row[8], nome_usuario=row[9]
        ).dict()
    raise HTTPException(404, "Reseva não encontrada")

@router.patch("/atualizar/{id_reserva}")
async def atualizar_reserva_parcial(id_reserva: int, res: ReservaUpdate):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_reserva FROM reserva WHERE id_reserva=%s", (id_reserva,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Reserva não encontrado")
    fields = []
    values = []
    for campo, valor in res.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(id_reserva)
    try:
        cur.execute(f"UPDATE reserva SET {', '.join(fields)} WHERE id_reserva=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Reserva atualizada"}

@router.delete("/deletar/{id_reserva}")
async def deletar_reserva(id_reserva: int):
    conn = get_admin_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM reserva WHERE id_reserva=%s", (id_reserva,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Reserva removida"}