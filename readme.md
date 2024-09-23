Olá, essa é uma aplicacao em Python, utilizando Flask para o back-end, e HTML/CSS para o Front-End, e a aplicacao se resume a um Questionário PSQI interativo feito como processo seletivo de um estágio na Innera Health, a aplicacao é fácil de ser instalada e segue tutorial para a mesma.

# Clonar o repositório
git clone https://github.com/seu-usuario/seu-repositorio.git

# Entrar no diretório do projeto
cd seu-repositorio

# Criar um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar as dependências
pip install -r requirements.txt

# Rodar a aplicação
flask run

1. Preenchimento do questionário PSQI
A aplicação fornece um questionário de 10 perguntas baseado no Índice de Qualidade do Sono de Pittsburgh (PSQI). O usuário deve preencher todas as questões com base no seu padrão de sono do último mês. As perguntas abrangem o horário em que o usuário vai dormir, o tempo para adormecer, a quantidade de horas dormidas e outros fatores relacionados à qualidade do sono.

O formulário é simples e intuitivo, com opções de resposta de múltipla escolha e campos de texto para as respostas que exigem tempo (como "Quando você foi dormir?"). O usuário preenche o formulário e envia as respostas, que serão calculadas automaticamente para gerar a pontuação PSQI.

2. Gráfico de pontuação
Após a conclusão do questionário, a aplicação exibe a pontuação PSQI do usuário em forma de gráfico. Este gráfico compara a pontuação atual com as pontuações anteriores do mesmo usuário, fornecendo uma visão clara da evolução da qualidade do sono ao longo do tempo.

Cada barra do gráfico representa uma sessão de questionário preenchida. A pontuação vai de 0 a 21, e quanto menor for a pontuação, melhor a qualidade do sono.

3. Login e registro
A aplicação implementa um sistema de autenticação simples para garantir que os questionários e pontuações fiquem salvos e acessíveis apenas ao usuário que os criou. O processo de login permite que o usuário acesse seus dados anteriores de forma segura.

Registro: O usuário cria uma conta fornecendo um nome de usuário, e-mail e senha.
Login: Após registrado, o usuário pode acessar sua conta e ver questionários anteriores e gráficos de pontuação.
Essa funcionalidade é essencial para que cada usuário tenha acesso exclusivo às suas pontuações, podendo acompanhar a evolução do seu sono ao longo do tempo.

4. Legendas para o gráfico
Na página do gráfico de pontuação, há uma legenda explicando que a escala PSQI funciona da seguinte forma:

Quanto menor a pontuação, melhor a qualidade do sono.
Pontuações de 0 a 5 indicam boa qualidade de sono.
Pontuações de 6 a 10 indicam distúrbios moderados de sono.
Pontuações acima de 11 indicam graves problemas relacionados ao sono.
Isso ajuda o usuário a entender como interpretar as pontuações e o que elas significam em termos de qualidade de sono.

Extras Implementados
1. Interface Responsiva
A interface da aplicação foi projetada para ser responsiva, ou seja, ela se adapta a diferentes tamanhos de tela, como smartphones, tablets e desktops. Utilizando CSS responsivo e media queries, a aplicação ajusta automaticamente a disposição dos elementos da página para garantir uma boa experiência de uso, independentemente do dispositivo utilizado.

Nos dispositivos móveis, o formulário do questionário PSQI e os gráficos são redimensionados para facilitar a leitura e o preenchimento.
Os botões, campos de entrada e menus também são redimensionados para que sejam fáceis de clicar e interagir.
Essa funcionalidade melhora significativamente a usabilidade da aplicação, tornando-a acessível em qualquer ambiente.

2. Gráficos Interativos para Visualização dos Dados
A aplicação utiliza Chart.js para gerar gráficos interativos que mostram as pontuações PSQI do usuário ao longo do tempo. Os gráficos permitem uma visualização clara e dinâmica da evolução da qualidade do sono, com as seguintes funcionalidades:

Interatividade: O gráfico é interativo, permitindo que o usuário passe o mouse sobre as barras para ver a pontuação exata de cada questionário preenchido.
Comparação de Pontuações: Ao longo do tempo, o gráfico mostra como a pontuação do usuário variou entre diferentes questionários, ajudando a identificar padrões e melhorias no sono.
Legendas: A legenda do gráfico explica como interpretar as pontuações, destacando que "quanto menor a pontuação, melhor a qualidade do sono."
Esse recurso melhora a visualização dos dados, tornando mais fácil para o usuário acompanhar sua evolução.

3. Autenticação
O sistema de autenticação garante que cada usuário tenha acesso aos seus próprios questionários e pontuações, com segurança. A funcionalidade de autenticação foi implementada com as seguintes características:

Registro: Permite que novos usuários criem uma conta com nome de usuário, e-mail e senha.
Login: Usuários registrados podem fazer login e acessar seus questionários e pontuações anteriores.
Segurança: As senhas são criptografadas usando a biblioteca werkzeug.security para garantir a segurança dos dados do usuário.
Essa funcionalidade permite que os usuários salvem e acompanhem seu progresso ao longo do tempo, proporcionando uma experiência personalizada e segura.