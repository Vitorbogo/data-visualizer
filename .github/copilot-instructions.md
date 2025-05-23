<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Personal Data Visualizer - Copilot Instructions

Este é um projeto de Personal Data Visualizer que conecta APIs pessoais para criar dashboards interativos e análises de dados.

## Contexto do Projeto

- **Linguagem Principal**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript com Bootstrap e Chart.js
- **Integração Principal**: Spotify Web API
- **Objetivo**: Visualizar dados pessoais de forma interativa e gamificada

## Padrões de Código

### Backend (Python/Flask)
- Use type hints quando possível
- Implemente tratamento de erros adequado para APIs externas
- Mantenha as credenciais em variáveis de ambiente
- Use padrão MVC: routes no app.py, lógica nos clients, análise no data_analyzer

### Frontend
- Use Bootstrap 5 para responsividade
- Implemente Chart.js para visualizações
- Mantenha JavaScript modular com classes ES6
- Use CSS custom properties para temas

### Integração de APIs
- Implemente OAuth2 adequado para Spotify
- Cache dados quando apropriado
- Trate rate limits e erros de API gracefully
- Use refresh tokens quando disponível

## Estrutura Esperada

```
project/
├── app.py                 # Flask app principal
├── spotify_client.py      # Cliente Spotify API
├── data_analyzer.py       # Análise e processamento
├── templates/            # Templates Jinja2
├── static/              # CSS, JS, assets
└── requirements.txt     # Dependências Python
```

## APIs e Integrações

### Spotify Web API
- Scopes necessários: user-read-private, user-read-email, user-top-read, user-read-recently-played
- Use PKCE flow quando possível
- Implemente refresh token logic

### Futuras Integrações
- GitHub API para dados de desenvolvimento
- Google Fit/Health APIs para dados de saúde
- APIs de gaming (Steam, etc.)

## Gamificação

- Calcule scores baseados em diversidade musical, atividade, descobertas
- Implemente achievements/conquistas
- Crie níveis e progressão
- Use badges visuais para conquistas

## Visualizações Prioritárias

1. **Gêneros Musicais**: Gráfico de pizza/donut
2. **Horários de Escuta**: Gráfico de linha temporal
3. **Características de Áudio**: Gráfico radar
4. **Top Lists**: Listas rankeadas com imagens
5. **Atividade Temporal**: Heatmaps e calendários

## Considerações de UX

- Interface responsiva mobile-first
- Loading states para todas as operações assíncronas
- Error handling com mensagens amigáveis
- Tema escuro/claro (futuro)
- Animações suaves para transições
