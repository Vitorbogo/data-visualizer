# Personal Data Visualizer

Um dashboard interativo para visualizar e analisar seus dados pessoais, começando com a integração do Spotify.

## 🌟 Status do Projeto

✅ **Funcional** - Projeto criado e rodando com sucesso!

## 🚀 Funcionalidades

- 🎵 **Integração Spotify**: Conecta com sua conta Spotify para analisar seus hábitos musicais
- 📊 **Dashboard Interativo**: Visualizações dinâmicas dos seus dados com Chart.js
- 🎯 **Gráfico Radar de Características**: Análise visual das características sonoras das suas músicas (NEW! ✨)
- 📈 **Análise de Padrões**: Identifica tendências nos seus hábitos de escuta
- 🎮 **Gamificação**: Sistema de pontuação e conquistas baseado nos seus dados musicais
- 📱 **Totalmente Responsivo**: Interface otimizada para mobile com design moderno
- ⚡ **Performance Otimizada**: Sistema de cache inteligente para reduzir chamadas à API

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
   - **Website**: http://localhost:5000
   - **Redirect URI**: http://localhost:5000/callback
4. Aceite os termos e crie o app
5. Copie Client ID e Client Secret
6. Crie um arquivo `.env` na raiz do projeto:

```env
SPOTIFY_CLIENT_ID=seu_client_id_aqui
SPOTIFY_CLIENT_SECRET=seu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=sua_chave_secreta_flask_aqui
```

### 3. Executar a Aplicação

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Executar aplicação
python app.py
```

Acesse `http://localhost:5000` no seu navegador.

## 📊 O que você vai ver

### Dashboard Principal
- **Estatísticas Rápidas**: Total de músicas, artistas, gênero favorito, atividade recente
- **Gráfico de Gêneros**: Distribuição dos seus gêneros musicais favoritos (pizza/donut)
- **Horários de Escuta**: Padrão temporal de quando você mais ouve música (linha)
- **Características de Áudio**: Gráfico radar com 7 características sonoras principais (NEW! ✨)
  - 🕺 Dançabilidade - 🔥 Energia - 🗣️ Fala - 🎸 Acústico - 🎼 Instrumental - 🎤 Ao Vivo - 😊 Positividade
- **Top Lists**: Suas músicas e artistas mais tocados com imagens e índices de popularidade

### Análises Disponíveis
- 🎭 **Diversidade musical**: Quantos gêneros diferentes você escuta
- ⏰ **Padrões temporais**: Seus horários de pico de escuta
- 🎯 **Perfil sonoro**: Características detalhadas das suas músicas favoritas
- 📈 **Sistema de Score**: Pontuação gamificada baseada na sua atividade musical
- 🏆 **Conquistas**: Badges e achievements baseados nos seus hábitos de escuta

## 🏗️ Estrutura do Projeto

```
project/
├── app.py                 # Aplicação principal Flask
├── spotify_client.py      # Cliente para API do Spotify
├── data_analyzer.py       # Análise de dados musicais
├── templates/            # Templates HTML
│   ├── base.html          # Template base
│   ├── index.html         # Página inicial
│   └── dashboard.html     # Dashboard principal
├── static/              # CSS, JS e recursos
│   ├── css/
│   │   └── style.css      # Estilos customizados
│   └── js/
│       └── dashboard.js   # JavaScript do dashboard
├── venv/                # Ambiente virtual Python
├── requirements.txt     # Dependências Python
├── .env.example        # Exemplo de variáveis de ambiente
└── .env               # Suas variáveis de ambiente (criar)
```

## 🔧 Tecnologias Utilizadas

### Backend
- **Python 3.12+**
- **Flask 3.1+** - Framework web
- **Spotipy 2.25+** - Cliente Python para Spotify API
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5 + CSS3 + JavaScript ES6**
- **Bootstrap 5** - Framework CSS responsivo
- **Chart.js** - Biblioteca de gráficos interativos
- **Font Awesome** - Ícones

### APIs
- **Spotify Web API** - Dados musicais
- **OAuth 2.0** - Autenticação segura

## 🎯 Próximos Passos

- [ ] **GitHub Integration**: Dados de atividade de desenvolvimento
- [ ] **Google Fit API**: Dados de saúde e fitness
- [ ] **Machine Learning**: Previsão de tendências musicais
- [ ] **Exportação de Dados**: PDF e CSV reports
- [ ] **Tema Escuro**: Interface dark mode
- [ ] **Cache Redis**: Performance melhorada
- [ ] **Banco de Dados**: Histórico de dados
- [ ] **Deploy**: Heroku/Railway/Vercel

## 🐛 Troubleshooting

### Erro "Não foi possível resolver a importação"
- Certifique-se de ativar o ambiente virtual: `source venv/bin/activate`
- Configure o Python interpreter no VS Code para usar o venv

### Erro de autenticação Spotify
- Verifique se o Redirect URI está correto no Spotify Dashboard
- Confirme se as variáveis no arquivo `.env` estão corretas

### Servidor não inicia
- Verifique se a porta 5000 não está sendo usada por outro processo
- Tente mudar a porta no `app.py`: `app.run(port=5001)`

## 📄 Licença

Este projeto é open source e está disponível sob a [MIT License](LICENSE).

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Fazer commit das suas mudanças
4. Enviar um pull request

---

**Criado com ❤️ para transformar dados em insights incríveis!**
