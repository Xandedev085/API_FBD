  CREATE TABLE Endereco (
id_endereco NUMERIC PRIMARY KEY,
cep VARCHAR(10),
rua VARCHAR(50),
estado VARCHAR(35),
pais VARCHAR(40)
);

CREATE TABLE Hospedagem (
id_hospedagem NUMERIC PRIMARY KEY,
nome VARCHAR(25),
avaliacao_media NUMERIC,
tipo VARCHAR(20),
descricao VARCHAR(100),
fk_endereco NUMERIC,
FOREIGN KEY (fk_endereco) REFERENCES Endereco(id_endereco)
);

CREATE TABLE Usuario (
cpf VARCHAR(11) PRIMARY KEY,
nome VARCHAR(25),
senha CHAR(10),
data_cadastro DATE
);

CREATE TABLE Telefones (
cpf_usuario VARCHAR(11),
telefone VARCHAR(20),
PRIMARY KEY (cpf_usuario, telefone),
FOREIGN KEY (cpf_usuario) REFERENCES Usuario(cpf)
);

CREATE TABLE Emails (
cpf_usuario VARCHAR(11),
email VARCHAR(100),
PRIMARY KEY (cpf_usuario, email),
FOREIGN KEY (cpf_usuario) REFERENCES Usuario(cpf)
);

CREATE TABLE Quarto (
id_quarto NUMERIC PRIMARY KEY,
tipo VARCHAR(20),
descricao VARCHAR(100),
preco_diaria NUMERIC,
qtd_disponivel NUMERIC,
id_hospedagem NUMERIC,
FOREIGN KEY (id_hospedagem) REFERENCES Hospedagem(id_hospedagem)
);

CREATE TABLE Avaliacao (
id_avaliacao NUMERIC PRIMARY KEY,
nota NUMERIC,
comentario VARCHAR(100),
cpf_usuario VARCHAR(11),
id_hospedagem NUMERIC,
FOREIGN KEY (cpf_usuario) REFERENCES Usuario(cpf),
FOREIGN KEY (id_hospedagem) REFERENCES Hospedagem(id_hospedagem)
);

CREATE TABLE Reserva (
id_reserva NUMERIC PRIMARY KEY,
status VARCHAR(20),
data_checkin DATE,
data_checkout DATE,
valor_total NUMERIC,
qtd_hospedes NUMERIC,
cpf_usuario VARCHAR(11),
id_quarto NUMERIC,
id_hospedagem NUMERIC,
FOREIGN KEY (cpf_usuario) REFERENCES Usuario(cpf),
FOREIGN KEY (id_hospedagem) REFERENCES Hospedagem(id_hospedagem),
FOREIGN KEY (id_quarto) REFERENCES Quarto(id_quarto)
);

CREATE TABLE Favoritos (
cpf_usuario VARCHAR(11),
id_hospedagem NUMERIC,
data_favorito DATE,

PRIMARY KEY (cpf_usuario, id_hospedagem),
FOREIGN KEY (cpf_usuario) REFERENCES Usuario(cpf),
FOREIGN KEY (id_hospedagem) REFERENCES Hospedagem(id_hospedagem)
);

INSERT INTO Endereco (id_endereco, cep, rua, estado, pais)
VALUES 
(1, '12345-000', 'Rua das Palmeiras', 'Bahia', 'Brasil'),
(2, '12345-001', 'Avenida Atlântica', 'Rio de Janeiro', 'Brasil'),
(3, '12345-002', 'Rua dos Mochileiros', 'Minas Gerais', 'Brasil'),
(4, '12345-003', 'Estrada da Serra', 'Santa Catarina', 'Brasil'),
(5, '12345-004', 'Alameda Tropical', 'Bahia', 'Brasil'),
(6, '12345-005', 'Rua das Cachoeiras', 'Espírito Santo', 'Brasil'),
(7, '12345-006', 'Avenida Central', 'São Paulo', 'Brasil'),
(8, '12345-007', 'Rua Verde Vida', 'Paraná', 'Brasil'),
(9, '12345-008', 'Caminho da Lua', 'Rio Grande do Sul', 'Brasil'),
(10, '12345-009', 'Praia das Dunas', 'Ceará', 'Brasil');

INSERT INTO Hospedagem (id_hospedagem, nome, avaliacao_media, tipo, descricao, fk_endereco)
VALUES 
(1, 'Pousada Palmeira', 4.5, 'Pousada', 'Lugar tranquilo com muito verde.', 1),
(2, 'Hotel Atlântico', 4.7, 'Hotel', 'Luxuoso hotel à beira-mar.', 2),
(3, 'Hostel Mochileiros', 4.2, 'Hostel', 'Ambiente descontraído e jovem.', 3),
(4, 'Chalés da Serra', 4.8, 'Chalé', 'Ideal para descansar nas montanhas.', 4),
(5, 'Resort Tropical', 4.9, 'Resort', 'All inclusive com lazer completo.', 5),
(6, 'Pousada da Cachoeira', 4.4, 'Pousada', 'Próxima às principais trilhas.', 6),
(7, 'Hotel Central', 4.1, 'Hotel', 'Bem localizado no centro.', 7),
(8, 'Eco Lodge Verde Vida', 4.6, 'Lodge', 'Integração com a natureza.', 8),
(9, 'Camping Lua Cheia', 4.0, 'Camping', 'Espaço para barracas e trailers.', 9),
(10, 'Villa das Dunas', 4.9, 'Villa', 'Charme e conforto à beira-mar.', 10);


INSERT INTO Usuario (cpf, nome, senha, data_cadastro)
VALUES 
('11111111111', 'João Silva', 'senha1234', '2025-06-01'),
('22222222222', 'Maria Souza', 'senha2345', '2025-06-02'),
('33333333333', 'Carlos Pereira', 'senha3456', '2025-06-03'),
('44444444444', 'Ana Lima', 'senha4567', '2025-06-04'),
('55555555555', 'Lucas Mendes', 'senha5678', '2025-06-05'),
('66666666666', 'Bruna Oliveira', 'senha6789', '2025-06-06'),
('77777777777', 'Pedro Santos', 'senha7890', '2025-06-07'),
('88888888888', 'Laura Martins', 'senha8901', '2025-06-08'),
('99999999999', 'Rafael Almeida', 'senha9012', '2025-06-09'),
('00000000000', 'Juliana Rocha', 'senha0123', '2025-06-10');


INSERT INTO Telefones (cpf_usuario, telefone)
VALUES 
('11111111111', '(11)91234-5678'),
('22222222222', '(21)92345-6789'),
('33333333333', '(31)93456-7890'),
('44444444444', '(41)94567-8901'),
('55555555555', '(51)95678-9012'),
('66666666666', '(61)96789-0123'),
('77777777777', '(71)97890-1234'),
('88888888888', '(81)98901-2345'),
('99999999999', '(91)99012-3456'),
('00000000000', '(31)90123-4567');

INSERT INTO Emails (cpf_usuario, email)
VALUES 
('11111111111', 'joao@email.com'),
('22222222222', 'maria@email.com'),
('33333333333', 'carlos@email.com'),
('44444444444', 'ana@email.com'),
('55555555555', 'lucas@email.com'),
('66666666666', 'bruna@email.com'),
('77777777777', 'pedro@email.com'),
('88888888888', 'laura@email.com'),
('99999999999', 'rafael@email.com'),
('00000000000', 'juliana@email.com');

INSERT INTO Quarto (id_quarto, tipo, descricao, preco_diaria, qtd_disponivel, id_hospedagem)
VALUES 
(1, 'Standard', 'Quarto com cama de casal', 200.00, 3, 1),
(2, 'Luxo', 'Quarto com vista para o mar', 350.00, 2, 2),
(3, 'Compartilhado', 'Beliche em quarto coletivo', 80.00, 5, 3),
(4, 'Chalé', 'Chalé com lareira e varanda', 500.00, 1, 4),
(5, 'Suíte Master', 'Suíte com banheira e varanda', 800.00, 1, 5),
(6, 'Deluxe', 'Suíte com hidromassagem', 600.00, 2, 6),
(7, 'Economy', 'Quarto simples e funcional', 100.00, 3, 7),
(8, 'Casal', 'Quarto aconchegante para dois', 220.00, 4, 8),
(9, 'Família', 'Espaçoso com 2 beliches', 280.00, 2, 9),
(10, 'Presidencial', 'Luxo extremo com vista panorâmica', 1200.00, 1, 10);

INSERT INTO Avaliacao (id_avaliacao, nota, comentario, cpf_usuario, id_hospedagem)
VALUES 
(1, 5.0, 'Excelente atendimento!', '11111111111', 1),
(2, 4.0, 'Ótima localização.', '22222222222', 2),
(3, 3.5, 'Bom custo-benefício.', '33333333333', 3),
(4, 4.8, 'Lugar maravilhoso!', '44444444444', 4),
(5, 3.9, 'Recomendo, mas pode melhorar.', '55555555555', 5),
(6, 4.0, 'Bom atendimento e conforto.', '66666666666', 6),
(7, 3.5, 'Satisfatório pelo preço.', '77777777777', 7),
(8, 5.0, 'Espetacular! Superou expectativas.', '88888888888', 8),
(9, 4.8, 'Excelente localização e serviço.', '99999999999', 9),
(10, 4.2, 'Muito agradável e limpo.', '00000000000', 10);

INSERT INTO Reserva (id_reserva, status, data_checkin, data_checkout, valor_total, qtd_hospedes, cpf_usuario, id_quarto, id_hospedagem)
VALUES 
(1, 'Confirmada', '2025-07-01', '2025-07-05', 800.00, 2, '11111111111', 1, 1),
(2, 'Pendente', '2025-07-06', '2025-07-10', 1400.00, 2, '22222222222', 2, 2),
(3, 'Cancelada', '2025-07-11', '2025-07-13', 0.00, 1, '33333333333', 3, 3),
(4, 'Confirmada', '2025-07-15', '2025-07-20', 2500.00, 2, '44444444444', 4, 4),
(5, 'Confirmada', '2025-07-21', '2025-07-25', 3200.00, 3, '55555555555', 5, 5),
(6, 'Confirmada', '2025-08-12', '2025-08-15', 1800.00, 2, '66666666666', 6, 6),
(7, 'Pendente', '2025-08-18', '2025-08-20', 200.00, 1, '77777777777', 7, 7),
(8, 'Confirmada', '2025-08-21', '2025-08-24', 660.00, 2, '88888888888', 8, 8),
(9, 'Cancelada', '2025-08-25', '2025-08-28', 0.00, 4, '99999999999', 9, 9),
(10, 'Confirmada', '2025-08-30', '2025-09-02', 3600.00, 2, '00000000000', 10, 10);

INSERT INTO Favoritos (cpf_usuario, id_hospedagem, data_favorito)
VALUES 
('11111111111', 1, '2025-06-01'),
('22222222222', 2, '2025-06-02'),
('33333333333', 3, '2025-06-03'),
('44444444444', 4, '2025-06-04'),
('55555555555', 5, '2025-06-05'),
('66666666666', 6, '2025-06-25'),
('77777777777', 7, '2025-06-26'),
('88888888888', 8, '2025-06-27'),
('99999999999', 9, '2025-06-28'),
('00000000000', 10, '2025-06-29');
