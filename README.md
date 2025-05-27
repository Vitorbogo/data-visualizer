# Personal Data Visualizer

Um dashboard interativo para visualizar e analisar seus dados pessoais, começando com a integração do Spotify.
Projeto que dei inicio na faculdade porém abandonei e decidi testar fazer o mesmo projeto utilizando python no backend

![image](https://github.com/user-attachments/assets/b91ace0f-b7a3-4ad2-9d24-ed3c7e5058b1)


## Funcionalidades

- **Integração Spotify**: Conecta com sua conta Spotify para analisar seus hábitos musicais
- **Dashboard Interativo**: Visualizações dinâmicas dos seus dados com Chart.js
- **Gráfico Radar de Características**: Análise visual das características sonoras das suas músicas (NEW! ✨)
- **Análise de Padrões**: Identifica tendências nos seus hábitos de escuta
- **Gamificação**: Sistema de pontuação e conquistas baseado nos seus dados musicais
- **Totalmente Responsivo**: Interface otimizada para mobile com design moderno
- **Performance Otimizada**: Sistema de cache inteligente para reduzir chamadas à API

## 🛠️ Configuração

### 1. Instalar Dependências

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar Spotify API

1. Acesse [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Clique em "Create App"
3. Preencha os dados:
   - **App name**: Personal Data Visualizer
   - **App description**: Dashboard para análise de dados musicais
   - **Website**: http://127.0.0.1:5000
   - **Redirect URI**: http://127.0.0.1:5000/callback
4. Aceite os termos e crie o app
5. Copie Client ID e Client Secret
6. Crie um arquivo `.env` na raiz do projeto:

```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
SECRET_KEY=sua_chave_secreta_flask_aqui
```

### 3. Executar a Aplicação

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Executar aplicação
python app.py
```

## 📊 O que você vai ver

### Dashboard Principal

- **Estatísticas Rápidas**: Total de músicas, artistas, gênero favorito, atividade recente
- **Gráfico de Gêneros**: Distribuição dos seus gêneros musicais favoritos (pizza/donut)
- **Horários de Escuta**: Padrão temporal de quando você mais ouve música (linha)
- **Características de Áudio**: Gráfico radar com 7 características sonoras principais
  - Dançabilidade - Energia - Fala - Acústico - Instrumental - Ao Vivo - Positividade
- **Top Lists**: Suas músicas e artistas mais tocados com imagens e índices de popularidade

### Análises Disponíveis

- **Diversidade**: Quantos gêneros diferentes você escuta
- **Padrões temporais**: Seus horários de pico de escuta
- **Perfil sonoro**: Características detalhadas das suas músicas favoritas
- **Sistema de Score**: Pontuação gamificada baseada na sua atividade musical
- **Conquistas**: Badges e achievements baseados nos seus hábitos de escuta

## Tecnologias Utilizadas

### Backend

- **Python**
- **Flask** - Framework web
- **Spotipy** - Cliente Python para Spotify API

### Frontend

- **HTML5 + CSS3 + JavaScript ES6**
- **Bootstrap 5** - Framework CSS responsivo
- **Chart.js** - Biblioteca de gráficos interativos

### APIs

- **Spotify Web API** - Dados musicais
- **OAuth 2.0** - Autenticação segura

## Próximos Passos

- [ ] **GitHub Integration**: Dados de atividade de desenvolvimento
- [ ] **Machine Learning**: Previsão de tendências musicais
- [ ] **Tema Escuro**: Interface dark mode
- [ ] **Deploy**: Heroku/Railway/Vercel

## Troubleshooting

### Erro "Não foi possível resolver a importação"

- Certifique-se de ativar o ambiente virtual: `source venv/bin/activate`
- Configure o Python interpreter no VS Code para usar o venv

### Erro de autenticação Spotify

- Verifique se o Redirect URI está correto no Spotify Dashboard
- Confirme se as variáveis no arquivo `.env` estão corretas

### Servidor não inicia

- Verifique se a porta 5000 não está sendo usada por outro processo
- Tente mudar a porta no `app.py`: `app.run(port=5001)`

---
