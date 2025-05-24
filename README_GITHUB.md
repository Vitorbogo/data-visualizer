# 🎵 Personal Data Visualizer

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-red.svg)](https://flask.palletsprojects.com/)
[![Spotify API](https://img.shields.io/badge/Spotify-API-1DB954.svg)](https://developer.spotify.com/documentation/web-api/)

> 🚀 **Um dashboard interativo para visualizar e analisar seus dados pessoais, começando com a integração do Spotify.**

## ✨ Demonstração

![Dashboard Preview](https://via.placeholder.com/800x400/1DB954/ffffff?text=Personal+Data+Visualizer+Dashboard)

_Dashboard principal mostrando análises musicais em tempo real_

## 🌟 Funcionalidades

- 🎵 **Integração Spotify**: Conecta com sua conta Spotify para analisar hábitos musicais
- 📊 **3 Tipos de Gráficos**: Distribuição de gêneros, padrões temporais e características de áudio
- 🎯 **Gráfico Radar**: Visualização única das características sonoras (dançabilidade, energia, etc.)
- 🎮 **Gamificação**: Sistema de pontuação, níveis e conquistas baseado nos seus dados
- 📱 **Mobile-First**: Interface responsiva que funciona perfeitamente em qualquer dispositivo
- ⚡ **Performance**: Sistema de cache inteligente para otimizar chamadas à API

## 🛠️ Tech Stack

### Backend

- **Python 3.12+** - Linguagem principal
- **Flask 3.1+** - Framework web minimalista
- **Spotipy 2.25+** - Cliente Python para Spotify API
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend

- **HTML5 + CSS3 + JavaScript ES6** - Stack web moderna
- **Bootstrap 5** - Framework CSS responsivo
- **Chart.js** - Biblioteca de gráficos interativos
- **Font Awesome** - Ícones

### Integrações

- **Spotify Web API** - Dados musicais em tempo real
- **OAuth 2.0** - Autenticação segura

## 🚀 Instalação e Uso

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USERNAME/personal-data-visualizer.git
cd personal-data-visualizer
```

### 2. Configure o ambiente

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

### 3. Configure a API do Spotify

1. Acesse [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crie uma nova aplicação:
   - **App name**: Personal Data Visualizer
   - **App description**: Dashboard para análise de dados musicais
   - **Website**: http://localhost:5000
   - **Redirect URI**: http://localhost:5000/callback
3. Copie o Client ID e Client Secret
4. Crie um arquivo `.env` baseado no `.env.example`:

```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=sua_chave_secreta_flask_aqui
```

### 4. Execute a aplicação

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Executar aplicação
python app.py
```

Acesse `http://localhost:5000` no seu navegador e conecte com sua conta Spotify!

## 📊 O que você vai descobrir

### 🎭 **Análise de Gêneros**

- Distribuição dos seus gêneros musicais favoritos
- Diversidade musical calculada automaticamente
- Insights sobre seu perfil musical

### ⏰ **Padrões Temporais**

- Horários de pico da sua atividade musical
- Análise de quando você mais ouve música
- Identificação de hábitos de escuta

### 🎯 **Características de Áudio**

Análise detalhada de 7 características principais:

- 🕺 **Dançabilidade** - O quão dançável são suas músicas
- ⚡ **Energia** - Intensidade e atividade musical
- 🗣️ **Fala** - Presença de elementos falados
- 🎸 **Acústico** - Nível de instrumentação acústica
- 🎼 **Instrumental** - Probabilidade de ser instrumental
- 🎤 **Ao Vivo** - Características de performance ao vivo
- 😊 **Positividade** - Sentimento positivo transmitido

### 🏆 **Sistema de Gamificação**

- **Pontuação**: Baseada em diversidade, atividade e descobertas
- **Níveis**: Iniciante → Entusiasta → Expert → Mestre da Música
- **Conquistas**: Badges especiais por atingir marcos específicos

## 🏗️ Estrutura do Projeto

```
personal-data-visualizer/
├── app.py                 # Aplicação principal Flask
├── spotify_client.py      # Cliente para API do Spotify
├── data_analyzer.py       # Motor de análise de dados
├── requirements.txt       # Dependências Python
├── .env.example          # Template de variáveis de ambiente
├── templates/            # Templates HTML (Jinja2)
│   ├── base.html
│   ├── index.html
│   └── dashboard.html
├── static/              # Assets estáticos
│   ├── css/
│   │   └── style.css    # Estilos customizados
│   └── js/
│       └── dashboard.js # JavaScript do dashboard
└── docs/               # Documentação adicional
```

## 🔧 API Endpoints

- `GET /` - Página inicial
- `GET /login` - Iniciar autenticação Spotify
- `GET /callback` - Callback OAuth do Spotify
- `GET /dashboard` - Dashboard principal
- `GET /api/charts/genres` - Dados do gráfico de gêneros
- `GET /api/charts/listening_time` - Dados do gráfico temporal
- `GET /api/charts/audio_features` - Dados do gráfico radar
- `GET /api/user/score` - Pontuação gamificada do usuário
- `GET /logout` - Logout da aplicação

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Áreas que precisam de ajuda:

- [ ] Integração com GitHub API
- [ ] Dados de Google Fit/Health
- [ ] Machine Learning para recomendações
- [ ] Testes automatizados
- [ ] Deploy em produção
- [ ] Documentação da API

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/) pela excelente documentação
- [Chart.js](https://www.chartjs.org/) pela biblioteca de gráficos fantástica
- [Bootstrap](https://getbootstrap.com/) pelo framework CSS responsivo
- Comunidade open source pelas bibliotecas incríveis

## 📞 Contato

**Vitor Bogo** - [vitorbogo@hotmail.com](mailto:vitorbogo@hotmail.com)

Project Link: [https://github.com/SEU_USERNAME/personal-data-visualizer](https://github.com/SEU_USERNAME/personal-data-visualizer)

---

⭐ **Se este projeto te ajudou, deixe uma estrela!**
