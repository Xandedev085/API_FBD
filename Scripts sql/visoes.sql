CREATE OR REPLACE VIEW vw_reservas_usuario AS
SELECT 
    r.id_reserva,
    r.status,
    r.data_checkin,
    r.data_checkout,
    r.valor_total,
    r.qtd_hospedes,
    r.id_quarto,
    r.id_hospedagem,
    u.cpf,
    u.nome AS nome_usuario
FROM 
    Reserva r
JOIN Usuario u ON r.cpf_usuario = u.cpf;

CREATE OR REPLACE VIEW vw_hospedagem_detalhes AS
SELECT 
    h.id_hospedagem,
    h.nome AS nome_hospedagem,
    h.tipo AS tipo_hospedagem,
    q.id_quarto,
    q.tipo AS tipo_quarto,
    q.descricao AS descricao_quarto,
    e.estado,
    e.pais,
    e.cep
FROM 
    Hospedagem h
JOIN Quarto q ON h.id_hospedagem = q.id_hospedagem
JOIN Endereco e ON h.fk_endereco = e.id_endereco;


CREATE OR REPLACE VIEW vw_avaliacoes_por_hospedagem AS
SELECT 
    h.id_hospedagem,
    h.nome AS nome_hospedagem,
    h.tipo,
    COUNT(a.id_avaliacao) AS total_avaliacoes,
    ROUND(AVG(a.nota), 2) AS media_nota,
    MAX(a.comentario) AS exemplo_comentario,
    e.estado,
    e.pais
FROM 
    Hospedagem h
LEFT JOIN Avaliacao a ON h.id_hospedagem = a.id_hospedagem
JOIN Endereco e ON h.fk_endereco = e.id_endereco
GROUP BY h.id_hospedagem, h.nome, h.tipo, e.estado, e.pais;

CREATE OR REPLACE VIEW vw_favoritos_usuarios AS
SELECT 
    u.cpf,
    u.nome AS nome_usuario,
    f.id_hospedagem,
    h.nome AS nome_hospedagem,
    f.data_favorito
FROM 
    Favoritos f
JOIN Usuario u ON f.cpf_usuario = u.cpf
JOIN Hospedagem h ON f.id_hospedagem = h.id_hospedagem;