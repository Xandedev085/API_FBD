-- 1. Criação do usuário admin
CREATE USER admin_colaaqui WITH PASSWORD 'Admin@1234';

-- 2. Criação do usuário somente leitura
CREATE USER leitura_colaaqui WITH PASSWORD 'Leitura@1234';

-- 3. Conceder todos os privilégios ao admin
GRANT ALL PRIVILEGES ON DATABASE colaaqui TO admin_colaaqui;
GRANT ALL PRIVILEGES ON SCHEMA public TO admin_colaaqui;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_colaaqui;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_colaaqui;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin_colaaqui;

-- 4. Conceder permissões básicas ao usuário de leitura
GRANT CONNECT ON DATABASE colaaqui TO leitura_colaaqui;
GRANT USAGE ON SCHEMA public TO leitura_colaaqui;

-- 5. Conceder SELECT em todas as tabelas existentes
GRANT SELECT ON ALL TABLES IN SCHEMA public TO leitura_colaaqui;

-- 6. Configurar permissões padrão para futuras tabelas
ALTER DEFAULT PRIVILEGES 
    FOR USER admin_colaaqui
    IN SCHEMA public
    GRANT SELECT ON TABLES TO leitura_colaaqui;

-- 7. Permissão para sequences
ALTER DEFAULT PRIVILEGES 
    FOR USER admin_colaaqui
    IN SCHEMA public
    GRANT USAGE ON SEQUENCES TO leitura_colaaqui;

-- 8. Permissão para views
GRANT SELECT ON vw_favoritos_usuarios TO leitura_colaaqui;

ALTER DEFAULT PRIVILEGES FOR ROLE admin_colaaqui IN SCHEMA public GRANT SELECT ON TABLES TO leitura_colaaqui;
ALTER DEFAULT PRIVILEGES FOR ROLE admin_colaaqui IN SCHEMA public GRANT SELECT ON SEQUENCES TO leitura_colaaqui;
