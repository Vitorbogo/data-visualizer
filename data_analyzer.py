from collections import Counter, defaultdict
from datetime import datetime, timedelta


class DataAnalyzer:
  def __init__(self):
    pass

  def analyze_listening_habits(self, top_tracks, top_artists, recent_tracks):
    """Analisa hábitos de escuta do usuário"""
    analysis = {
        'total_tracks': 0,
        'total_artists': 0,
        'top_genre': 'Desconhecido',
        'listening_diversity': 0,
        'recent_activity': 'Baixa',
        'music_mood': 'Neutro',
        'discovery_rate': 0
    }

    if top_tracks and 'items' in top_tracks:
      analysis['total_tracks'] = len(top_tracks['items'])

    if top_artists and 'items' in top_artists:
      analysis['total_artists'] = len(top_artists['items'])

      # Analisar gêneros
      genres = []
      for artist in top_artists['items']:
        genres.extend(artist.get('genres', []))

      if genres:
        genre_counter = Counter(genres)
        analysis['top_genre'] = genre_counter.most_common(
          1)[0][0] if genre_counter else 'Desconhecido'
        analysis['listening_diversity'] = len(set(genres))

    # Analisar atividade recente
    if recent_tracks and 'items' in recent_tracks:
      recent_count = len(recent_tracks['items'])
      if recent_count > 40:
        analysis['recent_activity'] = 'Alta'
      elif recent_count > 20:
        analysis['recent_activity'] = 'Média'
      else:
        analysis['recent_activity'] = 'Baixa'

    return analysis

  def get_genre_distribution(self, top_artists):
    """Cria distribuição de gêneros para gráfico"""
    if not top_artists or 'items' not in top_artists:
      return {'labels': [], 'values': []}

    genres = []
    for artist in top_artists['items']:
      genres.extend(artist.get('genres', []))

    genre_counter = Counter(genres)
    top_genres = genre_counter.most_common(10)

    return {
        'labels': [genre for genre, count in top_genres],
        'values': [count for genre, count in top_genres]
    }

  def get_audio_features_summary(self, audio_features):
    """Analisa características de áudio das músicas"""
    if not audio_features or 'audio_features' not in audio_features:
      return {'labels': [], 'values': []}

    features = audio_features['audio_features']
    if not features:
      return {'labels': [], 'values': []}

    # Filtrar None values
    valid_features = [f for f in features if f is not None]
    if not valid_features:
      return {'labels': [], 'values': []}

    # Características que queremos analisar
    feature_names = [
        'danceability', 'energy', 'speechiness',
        'acousticness', 'instrumentalness', 'liveness', 'valence'
    ]

    # Calcular médias
    averages = {}
    for feature in feature_names:
      values = [f[feature] for f in valid_features if feature in f]
      if values:
        averages[feature] = sum(values) / len(values)

    # Traduzir nomes para português
    feature_translations = {
        'danceability': 'Dançabilidade',
        'energy': 'Energia',
        'speechiness': 'Fala',
        'acousticness': 'Acústico',
        'instrumentalness': 'Instrumental',
        'liveness': 'Ao Vivo',
        'valence': 'Positividade'
    }

    labels = [feature_translations.get(f, f)
              for f in feature_names if f in averages]
    values = [averages[f] for f in feature_names if f in averages]

    return {
        'labels': labels,
        'values': values
    }

  def get_listening_time_distribution(self, recent_tracks):
    """Analisa distribuição de tempo de escuta"""
    if not recent_tracks or 'items' not in recent_tracks:
      return {'labels': [], 'values': []}

    hour_counter = defaultdict(int)

    for item in recent_tracks['items']:
      if 'played_at' in item:
        played_at = datetime.fromisoformat(
          item['played_at'].replace('Z', '+00:00'))
        hour = played_at.hour
        hour_counter[hour] += 1

    # Criar labels de hora mais legíveis
    hours = list(range(24))
    values = [hour_counter[hour] for hour in hours]
    labels = [f"{hour:02d}:00" for hour in hours]

    return {
        'labels': labels,
        'values': values
    }

  def calculate_music_score(self, user_data, top_tracks, recent_tracks):
    """Calcula um score gamificado baseado nos dados musicais"""
    score = 0
    achievements = []

    # Score por diversidade
    if top_tracks and 'items' in top_tracks:
      unique_artists = len(set([track['artists'][0]['id']
                           for track in top_tracks['items']]))
      score += unique_artists * 2

      if unique_artists > 15:
        achievements.append(
          "🎭 Explorador Musical - Você ouve muitos artistas diferentes!")

    # Score por atividade recente
    if recent_tracks and 'items' in recent_tracks:
      recent_count = len(recent_tracks['items'])
      score += recent_count

      if recent_count > 40:
        achievements.append("🎵 Viciado em Música - Muito ativo recentemente!")

    # Score por popularidade vs descoberta
    if top_tracks and 'items' in top_tracks:
      avg_popularity = sum([track['popularity']
                           for track in top_tracks['items']]) / len(top_tracks['items'])

      if avg_popularity < 50:
        score += 50
        achievements.append(
          "🔍 Caçador de Raridades - Você descobre músicas antes dos outros!")
      elif avg_popularity > 80:
        achievements.append(
          "📻 Mainstream Master - Você está sempre por dentro dos hits!")

    return {
        'score': score,
        'achievements': achievements,
        'level': self._calculate_level(score)
    }

  def _calculate_level(self, score):
    """Calcula nível baseado no score"""
    if score < 100:
      return "🥉 Iniciante Musical"
    elif score < 300:
      return "🥈 Entusiasta"
    elif score < 600:
      return "🥇 Expert Musical"
    else:
      return "👑 Mestre da Música"

  def get_music_insights(self, top_tracks, top_artists, recent_tracks):
    """Gera insights avançados sobre os hábitos musicais"""
    insights = []

    if top_artists and 'items' in top_artists:
      # Insight sobre diversidade de gêneros
      genres = []
      for artist in top_artists['items']:
        genres.extend(artist.get('genres', []))

      unique_genres = len(set(genres))
      if unique_genres > 15:
        insights.append({
            'icon': '🎭',
            'title': 'Explorador Musical',
            'description': f'Você escuta {unique_genres} gêneros diferentes! Sua diversidade musical é impressionante.',
            'type': 'positive'
        })
      elif unique_genres < 5:
        insights.append({
            'icon': '🎯',
            'title': 'Foco Musical',
            'description': f'Você tem um gosto musical bem definido com {unique_genres} gêneros principais.',
            'type': 'info'
        })

    if top_tracks and 'items' in top_tracks:
      # Insight sobre popularidade
      avg_popularity = sum([track['popularity']
                           for track in top_tracks['items']]) / len(top_tracks['items'])

      if avg_popularity < 40:
        insights.append({
            'icon': '🔍',
            'title': 'Caçador de Raridades',
            'description': 'Você descobre músicas antes de todo mundo! Suas escolhas são bem underground.',
            'type': 'special'
        })
      elif avg_popularity > 80:
        insights.append({
            'icon': '📻',
            'title': 'Hit Master',
            'description': 'Você está sempre por dentro dos maiores sucessos do momento!',
            'type': 'positive'
        })

      # Insight sobre décadas
      decades = {}
      for track in top_tracks['items']:
        if 'album' in track and 'release_date' in track['album']:
          year = int(track['album']['release_date'][:4])
          decade = (year // 10) * 10
          decades[decade] = decades.get(decade, 0) + 1

      if decades:
        most_common_decade = max(decades, key=decades.get)
        if most_common_decade < 2000:
          insights.append({
              'icon': '📻',
              'title': 'Nostálgico Musical',
              'description': f'Você tem uma paixão pela música dos anos {most_common_decade}s!',
              'type': 'info'
          })

    if recent_tracks and 'items' in recent_tracks:
      # Insight sobre horários de escuta
      hour_counts = defaultdict(int)
      for item in recent_tracks['items']:
        if 'played_at' in item:
          played_at = datetime.fromisoformat(
            item['played_at'].replace('Z', '+00:00'))
          hour = played_at.hour
          hour_counts[hour] += 1

      if hour_counts:
        peak_hour = max(hour_counts, key=hour_counts.get)
        if 6 <= peak_hour <= 10:
          insights.append({
              'icon': '🌅',
              'title': 'Matutino Musical',
              'description': 'Você gosta de começar o dia com música! Maioria das escutas pela manhã.',
              'type': 'positive'
          })
        elif 22 <= peak_hour or peak_hour <= 2:
          insights.append({
              'icon': '🌙',
              'title': 'Coruja Musical',
              'description': 'A madrugada é sua hora de ouvir música! Você é um verdadeiro night owl.',
              'type': 'info'
          })

    return insights
