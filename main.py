from fastapi import FastAPI
from crud_reserva import router as reserva_router
from crud_hopedagem import router as hospedagem_router
from crud_avaliacoes import router as avaliacao_router
from crud_usuario import router as usuario_router
from crud_favoritos import router as favorito_router

app = FastAPI(
    title="API Colaaqui",
    version="1.0"
)

app.include_router(reserva_router, prefix="/reservas", tags=["Reserva"])
app.include_router(hospedagem_router, prefix="/hospedagem", tags=["Hospedagem"])
app.include_router(avaliacao_router, prefix="/avaliacao", tags=["Avaliacao"])
app.include_router(usuario_router, prefix="/usuario", tags=["Usuario"])
app.include_router(favorito_router, prefix="/favorito", tags=["Favorito"])