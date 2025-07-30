import psycopg2

def get_admin_connection():
    return psycopg2.connect(
        dbname="colaaqui",
        user="admin_colaaqui",
        password="Admin@1234",
        host="localhost"
    )

def get_read_connection():
    return psycopg2.connect(
        dbname="colaaqui",
        user="leitura_colaaqui",
        password="Leitura@1234",
        host="localhost"
    )
