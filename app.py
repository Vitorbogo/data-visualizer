from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from spotify_client import SpotifyClient
from data_analyzer import DataAnalyzer
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configurar Content Security Policy permissiva para desenvolvimento


@app.after_request
def after_request(response):
  # CSP permissiva para desenvolvimento - permite scripts inline e CDNs
  csp = (
      "default-src 'self'; "
      "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
      "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
      "style-src 'self' 'unsafe-inline' "
      "https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
      "img-src 'self' data: https: blob:; "
      "font-src 'self' https://cdnjs.cloudflare.com; "
      "connect-src 'self' https://api.spotify.com; "
      "frame-src 'none';"
  )
  response.headers['Content-Security-Policy'] = csp

  # Headers de segurança adicionais
  response.headers['X-Content-Type-Options'] = 'nosniff'
  response.headers['X-Frame-Options'] = 'DENY'
  response.headers['X-XSS-Protection'] = '1; mode=block'

  return response


# Cache simples para dados
cache = {}
CACHE_DURATION = timedelta(minutes=5)  # Cache por 5 minutos

# Configuração do Spotify
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

if not all([SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI]):
  print("⚠️  ATENÇÃO: Configure as variáveis de ambiente do Spotify no arquivo .env")
  print("📋 Copie .env.example para .env e preencha com suas credenciais")

spotify_client = SpotifyClient(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI
)


def get_cached_data(key, access_token, fetch_function, *args):
  """Função para gerenciar cache de dados"""
  now = datetime.now()
  cache_key = f"{key}_{access_token[:10]}"  # Usar parte do token como chave

  if cache_key in cache:
    data, timestamp = cache[cache_key]
    if now - timestamp < CACHE_DURATION:
      return data

  # Buscar dados novos
  fresh_data = fetch_function(access_token, *args)
  if fresh_data:
    cache[cache_key] = (fresh_data, now)

  return fresh_data


def refresh_token_if_needed():
  """Renova o token se necessário"""
  if 'refresh_token' not in session:
    return False

  try:
    token_info = spotify_client.refresh_access_token(session['refresh_token'])
    if token_info:
      session['access_token'] = token_info['access_token']
      if 'refresh_token' in token_info:
        session['refresh_token'] = token_info['refresh_token']
      return True
  except Exception as e:
    print(f"Erro ao renovar token: {e}")

  return False


@app.route('/')
def index():
  """Página inicial"""
  if 'access_token' in session:
    return redirect(url_for('dashboard'))
  return render_template('index.html')


@app.route('/login')
def login():
  """Iniciar processo de login com Spotify"""
  auth_url = spotify_client.get_auth_url()
  return redirect(auth_url)


@app.route('/callback')
def callback():
  """Callback do OAuth do Spotify"""
  code = request.args.get('code')
  error = request.args.get('error')

  if error:
    return render_template('index.html', error="Erro na autenticação com Spotify")

  if code:
    token_info = spotify_client.get_access_token(code)
    if token_info:
      session['access_token'] = token_info['access_token']
      session['refresh_token'] = token_info.get('refresh_token')
      return redirect(url_for('dashboard'))

  return render_template('index.html', error="Falha na autenticação")


@app.route('/dashboard')
def dashboard():
  """Dashboard principal com dados do Spotify"""
  if 'access_token' not in session:
    return redirect(url_for('index'))

  access_token = session['access_token']

  try:
    # Buscar dados do usuário com cache
    user_data = get_cached_data(
      'user_profile', access_token, spotify_client.get_user_profile)
    top_tracks = get_cached_data(
      'top_tracks', access_token, spotify_client.get_top_tracks, 'medium_term', 50)
    top_artists = get_cached_data(
      'top_artists', access_token, spotify_client.get_top_artists, 'medium_term', 50)
    recent_tracks = get_cached_data(
      'recent_tracks', access_token, spotify_client.get_recently_played, 50)

    # Verificar se algum dado falhou por token expirado
    if not user_data and refresh_token_if_needed():
      access_token = session['access_token']
      user_data = spotify_client.get_user_profile(access_token)
      top_tracks = spotify_client.get_top_tracks(
        access_token, 'medium_term', 50)
      top_artists = spotify_client.get_top_artists(
        access_token, 'medium_term', 50)
      recent_tracks = spotify_client.get_recently_played(access_token, 50)

    # Analisar dados
    analyzer = DataAnalyzer()
    analysis = analyzer.analyze_listening_habits(
      top_tracks, top_artists, recent_tracks)

    return render_template('dashboard.html',
                           user=user_data,
                           analysis=analysis,
                           top_tracks=top_tracks['items'][:10] if top_tracks else [
                             ],
                           top_artists=top_artists['items'][:10] if top_artists else [])

  except Exception as e:
    print(f"Erro no dashboard: {e}")
    # Se o token expirou, tentar renovar
    if "401" in str(e) or "token" in str(e).lower():
      if refresh_token_if_needed():
        return redirect(url_for('dashboard'))
      session.clear()
      return redirect(url_for('login'))
    return render_template('dashboard.html', error="Erro ao carregar dados do Spotify")


@app.route('/api/charts/<chart_type>')
def get_chart_data(chart_type):
  """API para dados dos gráficos"""
  if 'access_token' not in session:
    return jsonify({'error': 'Não autorizado'}), 401

  access_token = session['access_token']

  try:
    if chart_type == 'genres':
      top_artists = spotify_client.get_top_artists(access_token, limit=50)
      analyzer = DataAnalyzer()
      genre_data = analyzer.get_genre_distribution(top_artists)
      return jsonify(genre_data)

    elif chart_type == 'audio_features':
      print(f"🎵 Buscando características de áudio...")
      top_tracks = spotify_client.get_top_tracks(access_token, limit=50)
      if not top_tracks or 'items' not in top_tracks:
        print("❌ Erro: Nenhuma track encontrada")
        return jsonify({'error': 'Nenhuma track encontrada'}), 404

      track_ids = [track['id'] for track in top_tracks['items']]
      print(f"🎵 Encontradas {len(track_ids)} tracks para análise")

      audio_features = spotify_client.get_audio_features(
        access_token, track_ids)
      if not audio_features:
        print("❌ Erro: Não foi possível obter características de áudio")
        return jsonify({'error': 'Erro ao obter características de áudio'}), 500

      print(f"🎵 Características obtidas: {type(audio_features)}")
      analyzer = DataAnalyzer()
      features_data = analyzer.get_audio_features_summary(audio_features)
      print(f"🎵 Dados processados: {features_data}")
      return jsonify(features_data)

    elif chart_type == 'listening_time':
      recent_tracks = spotify_client.get_recently_played(
        access_token, limit=50)
      analyzer = DataAnalyzer()
      time_data = analyzer.get_listening_time_distribution(recent_tracks)
      return jsonify(time_data)

  except Exception as e:
    print(f"Erro ao buscar dados do gráfico {chart_type}: {e}")
    if "401" in str(e) or "token" in str(e).lower():
      return jsonify({'error': 'Token expirado', 'redirect': '/login'}), 401
    elif "429" in str(e):
      return jsonify({'error': 'Muitas requisições. Tente novamente em alguns segundos.'}), 429
    return jsonify({'error': str(e)}), 500

  return jsonify({'error': 'Tipo de gráfico não encontrado'}), 404


@app.route('/api/user/score')
def get_user_score():
  """API para score e gamificação do usuário"""
  if 'access_token' not in session:
    return jsonify({'error': 'Não autorizado'}), 401

  access_token = session['access_token']

  try:
    # Buscar dados necessários
    user_data = spotify_client.get_user_profile(access_token)
    top_tracks = spotify_client.get_top_tracks(access_token, limit=50)
    top_artists = spotify_client.get_top_artists(access_token, limit=50)
    recent_tracks = spotify_client.get_recently_played(access_token, limit=50)

    # Calcular score
    analyzer = DataAnalyzer()
    score_data = analyzer.calculate_music_score(
      user_data, top_tracks, recent_tracks)

    return jsonify(score_data)

  except Exception as e:
    return jsonify({'error': str(e)}), 500


@app.route('/api/user/insights')
def get_user_insights():
  """API para insights musicais personalizados"""
  if 'access_token' not in session:
    return jsonify({'error': 'Não autorizado'}), 401

  access_token = session['access_token']

  try:
    # Buscar dados necessários
    top_tracks = spotify_client.get_top_tracks(access_token, limit=50)
    top_artists = spotify_client.get_top_artists(access_token, limit=50)
    recent_tracks = spotify_client.get_recently_played(access_token, limit=50)

    # Gerar insights
    analyzer = DataAnalyzer()
    insights = analyzer.get_music_insights(
      top_tracks, top_artists, recent_tracks)

    return jsonify({'insights': insights})

  except Exception as e:
    return jsonify({'error': str(e)}), 500


@app.route('/logout')
def logout():
  """Fazer logout"""
  session.clear()
  return redirect(url_for('index'))


if __name__ == '__main__':
  print("🎵 Personal Data Visualizer")
  print("🚀 Iniciando servidor...")
  print("📱 Acesse: http://localhost:5000")
  app.run(debug=True, host='0.0.0.0', port=5000)
