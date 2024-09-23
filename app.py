from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'appwebdoscrias'  # Necessário para usar 'flash'

def init_db():
    with sqlite3.connect('database/responses.db') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bedtime TEXT,
                minutes_to_sleep INTEGER,
                wake_time TEXT,
                hours_of_sleep INTEGER,
                difficulty_sleeping INTEGER,
                midnightwake INTEGER,
                bathroombreak INTEGER,
                goodsleep INTEGER,
                roncouforte INTEGER,
                toocold INTEGER,
                toohot INTEGER,
                baddream INTEGER,
                in_pain INTEGER,
                other_reason TEXT,
                reason_value INTEGER,
                sleep_quality INTEGER,
                sleep_meds INTEGER,
                social_sleep INTEGER,
                activity_happiness INTEGER,
                partner INTEGER,
                psqi_score INTEGER,
                user_id INTEGER,  -- Removendo o comentário para evitar problemas de sintaxe
                FOREIGN KEY(user_id) REFERENCES users(id)  -- Criando relação com a tabela users
            )
        ''')
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()


# Função para interpretar a pontuação PSQI
def interpretar_psqi(pontuacao):
    if pontuacao <= 5:
        return 'Boa qualidade de sono. Seu escore está dentro da faixa normal.'
    elif 6 <= pontuacao <= 10:
        return 'Qualidade de sono ligeiramente prejudicada. Considere avaliar hábitos de sono.'
    elif 11 <= pontuacao <= 15:
        return 'Qualidade de sono significativamente prejudicada. Pode ser útil consultar um especialista.'
    else:
        return 'Qualidade de sono muito ruim. É altamente recomendável buscar ajuda médica.'

# Rota para registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        try:
            with sqlite3.connect('database/responses.db') as conn:
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO users (username, password) 
                    VALUES (?, ?)''', (username, hashed_password))
                conn.commit()
            flash('Usuário registrado com sucesso!')
            return redirect(url_for('user_login'))
        except sqlite3.IntegrityError:
            flash('Nome de usuário já existe. Escolha outro.')
            return redirect(url_for('register'))
    
    return render_template('register.html')

# Rota de login de usuário
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('user_login'))

        with sqlite3.connect('database/responses.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash('Login bem-sucedido!')
            return redirect(url_for('formulario'))
        else:
            flash('Credenciais inválidas.')
            return redirect(url_for('user_login'))

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você foi desconectado.')
    return redirect(url_for('user_login'))

def calcular_psqi(respostas):
    pontuacoes = {
        "qualidade_sono": 0,
        "latencia_sono": 0,
        "duracao_sono": 0,
        "eficiencia_sono": 0,
        "disturbios_sono": 0,
        "uso_medicacao": 0,
        "disfuncao_diurna": 0
    }

    # Qualidade Subjetiva do Sono
    pontuacoes['qualidade_sono'] = int(respostas['sleep_quality'])  # Questão 6

    # Latência do Sono
    tempo_latencia = respostas['minutes_to_sleep']
    if tempo_latencia <= 15:
        pontuacoes['latencia_sono'] = 0
    elif 16 <= tempo_latencia <= 30:
        pontuacoes['latencia_sono'] = 1
    elif 31 <= tempo_latencia <= 60:
        pontuacoes['latencia_sono'] = 2
    else:
        pontuacoes['latencia_sono'] = 3

    dificuldade_latencia = int(respostas['difficulty_sleeping'])
    if dificuldade_latencia == 0:
        pontuacoes['latencia_sono'] += 0
    elif 1 <= dificuldade_latencia <= 2:
        pontuacoes['latencia_sono'] += 1
    elif 3 <= dificuldade_latencia <= 4:
        pontuacoes['latencia_sono'] += 2
    elif 5 <= dificuldade_latencia <= 6:
        pontuacoes['latencia_sono'] += 3

    # Duração do Sono
    horas_sono = respostas['hours_of_sleep']
    if horas_sono > 7:
        pontuacoes['duracao_sono'] = 0
    elif 6 <= horas_sono <= 7:
        pontuacoes['duracao_sono'] = 1
    elif 5 <= horas_sono < 6:
        pontuacoes['duracao_sono'] = 2
    else:
        pontuacoes['duracao_sono'] = 3

    # Eficiência Habitual do Sono
    bedtime = datetime.strptime(respostas['bedtime'], '%H:%M')
    wake_time = datetime.strptime(respostas['wake_time'], '%H:%M')
    if wake_time < bedtime:
        wake_time += timedelta(days=1)
    tempo_cama = (wake_time - bedtime).total_seconds() / 3600
    if tempo_cama > 0:
        eficiencia = (respostas['hours_of_sleep'] / tempo_cama) * 100
    else:
        eficiencia = 0
    if eficiencia > 85:
        pontuacoes['eficiencia_sono'] = 0
    elif 75 <= eficiencia <= 84:
        pontuacoes['eficiencia_sono'] = 1
    elif 65 <= eficiencia <= 74:
        pontuacoes['eficiencia_sono'] = 2
    else:
        pontuacoes['eficiencia_sono'] = 3

    # Distúrbios do Sono
    disturbios = sum(int(respostas[key]) for key in [
        'midnightwake', 'bathroombreak', 'goodsleep', 'roncouforte', 
        'toocold', 'toohot', 'baddream', 'in_pain', 'reason_value'
    ])
    if disturbios == 0:
        pontuacoes['disturbios_sono'] = 0
    elif 1 <= disturbios <= 9:
        pontuacoes['disturbios_sono'] = 1
    elif 10 <= disturbios <= 18:
        pontuacoes['disturbios_sono'] = 2
    else:
        pontuacoes['disturbios_sono'] = 3

    # Uso de Remédio para Dormir
    pontuacoes['uso_medicacao'] = int(respostas['sleep_meds'])  # Questão 7

    # Disfunção Diurna
    disfuncao_diurna = int(respostas['social_sleep']) + int(respostas['activity_happiness'])
    if disfuncao_diurna == 0:
        pontuacoes['disfuncao_diurna'] = 0
    elif 1 <= disfuncao_diurna <= 2:
        pontuacoes['disfuncao_diurna'] = 1
    elif 3 <= disfuncao_diurna <= 4:
        pontuacoes['disfuncao_diurna'] = 2
    else:
        pontuacoes['disfuncao_diurna'] = 3

    return sum(pontuacoes.values())


# Página principal (redireciona para a página de login)
@app.route('/')
def index():
    return redirect(url_for('user_login'))

# Submissão do formulário PSQI
@app.route('/submit', methods=['POST'])
def submit():
    # Verificar se o usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para enviar respostas.')
        return redirect(url_for('user_login'))

    # Validar os campos obrigatórios
    required_fields = ['bedtime', 'minutes_to_sleep', 'wake_time', 'hours_of_sleep', 'partner']
    for field in required_fields:
        if not request.form.get(field):
            flash('Por favor, preencha todos os campos obrigatórios.')
            return redirect(url_for('formulario'))

    respostas = {key: request.form[key] for key in request.form}
    
    try:
        for key in ['hours_of_sleep', 'minutes_to_sleep', 'difficulty_sleeping', 'midnightwake', 'bathroombreak',
                    'goodsleep', 'roncouforte', 'toocold', 'toohot', 'baddream', 'in_pain', 'reason_value', 
                    'sleep_quality', 'sleep_meds', 'social_sleep', 'activity_happiness']:
            respostas[key] = int(respostas[key])
    except ValueError:
        flash('Os valores das respostas devem ser numéricos.')
        return redirect(url_for('formulario'))

    psqi_score = calcular_psqi(respostas)
    
    # Adicionar o ID do usuário às respostas
    user_id = session['user_id']

    with sqlite3.connect('database/responses.db') as conn:
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO responses (bedtime, minutes_to_sleep, wake_time, hours_of_sleep, difficulty_sleeping, midnightwake, 
                bathroombreak, goodsleep, roncouforte, toocold, toohot, baddream, in_pain, other_reason, reason_value, 
                sleep_quality, sleep_meds, social_sleep, activity_happiness, partner, psqi_score, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
            (respostas['bedtime'], respostas['minutes_to_sleep'], respostas['wake_time'], respostas['hours_of_sleep'], 
             respostas['difficulty_sleeping'], respostas['midnightwake'], respostas['bathroombreak'], 
             respostas['goodsleep'], respostas['roncouforte'], respostas['toocold'], respostas['toohot'], 
             respostas['baddream'], respostas['in_pain'], respostas['other_reason'], respostas['reason_value'], 
             respostas['sleep_quality'], respostas['sleep_meds'], respostas['social_sleep'], 
             respostas['activity_happiness'], respostas['partner'], psqi_score, user_id))  # Salvando o user_id junto com as respostas
        conn.commit()

    return redirect(url_for('resultados', psqi_score=psqi_score, **respostas))


# Página de resultados
@app.route('/resultados')
def resultados():
    psqi_score = request.args.get('psqi_score', type=int)
    respostas = {key: request.args[key] for key in request.args}
    interpretacao = interpretar_psqi(psqi_score)
    return render_template('resultados.html', psqi_score=psqi_score, respostas=respostas, interpretacao=interpretacao)

# Página do formulário PSQI
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        return redirect(url_for('submit'))
    
    return render_template('index.html')

@app.route('/responses')
def view_responses():
    with sqlite3.connect('database/responses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM responses')
        rows = cursor.fetchall()

    return render_template('responses.html', rows=rows)

@app.route('/minhas_respostas')
def minhas_respostas():
    # Verificar se o usuário está logado
    if 'user_id' not in session:
        flash('Você precisa estar logado para ver suas respostas.')
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    with sqlite3.connect('database/responses.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM responses WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()

    return render_template('minhas_respostas.html', rows=rows)

def pegar_pontuacoes_do_banco():
    with sqlite3.connect('database/responses.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT psqi_score FROM responses")
        pontuacoes = cursor.fetchall()
    return [score[0] for score in pontuacoes]

# app.py
@app.route('/historico')
def historico():
    return render_template('grafico_resultados.html')

@app.route('/historico_pontuacoes')
def historico_pontuacoes():
    pontuacoes = pegar_pontuacoes_do_banco()
    return jsonify(pontuacoes)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

