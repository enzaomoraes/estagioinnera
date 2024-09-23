import sqlite3

def add_psqi_score_column():
    conn = sqlite3.connect('database/responses.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            ALTER TABLE responses
            ADD COLUMN psqi_score INTEGER;
        ''')
        print("Coluna 'psqi_score' adicionada com sucesso.")
    except sqlite3.OperationalError as e:
        print(f"Erro ao adicionar coluna: {e}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_psqi_score_column()
