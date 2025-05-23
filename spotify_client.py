import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import urllib.parse as urllibparse
import time


class SpotifyClient:
  def __init__(self, client_id, client_secret, redirect_uri):
    self.client_id = client_id
    self.client_secret = client_secret
    self.redirect_uri = redirect_uri
    self.scope = "user-read-private user-read-email user-top-read user-read-recently-played user-read-playback-state"

  def get_auth_url(self):
    """Gera URL de autorização do Spotify"""
    auth_url = "https://accounts.spotify.com/authorize"
    params = {
        'client_id': self.client_id,
        'response_type': 'code',
        'redirect_uri': self.redirect_uri,
        'scope': self.scope,
        'show_dialog': 'true'
    }

    url_parts = list(urllibparse.urlparse(auth_url))
    query = dict(urllibparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllibparse.urlencode(query)

    return urllibparse.urlunparse(url_parts)

  def get_access_token(self, code):
    """Troca o código de autorização por token de acesso"""
    token_url = "https://accounts.spotify.com/api/token"

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': self.redirect_uri,
        'client_id': self.client_id,
        'client_secret': self.client_secret
    }

    try:
      response = requests.post(token_url, data=data, timeout=10)

      if response.status_code == 200:
        return response.json()
      else:
        print(f"Erro ao obter token: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
      print(f"Erro de conexão ao obter token: {e}")
      return None

  def refresh_access_token(self, refresh_token):
    """Renova o token de acesso usando refresh token"""
    token_url = "https://accounts.spotify.com/api/token"

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': self.client_id,
        'client_secret': self.client_secret
    }

    try:
      response = requests.post(token_url, data=data, timeout=10)

      if response.status_code == 200:
        return response.json()
      else:
        print(f"Erro ao renovar token: {response.status_code} - {response.text}")
        return None
    except requests.RequestException as e:
      print(f"Erro de conexão ao renovar token: {e}")
      return None

  def _make_spotify_request(self, access_token, endpoint, retries=3):
    """Faz requisição autenticada para API do Spotify com retry"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    for attempt in range(retries):
      try:
        response = requests.get(f"https://api.spotify.com/v1/{endpoint}",
                              headers=headers, timeout=10)

        if response.status_code == 200:
          return response.json()
        elif response.status_code == 429:  # Rate limit
          retry_after = int(response.headers.get('Retry-After', 1))
          print(f"Rate limit atingido. Aguardando {retry_after}s...")
          time.sleep(retry_after)
          continue
        elif response.status_code == 401:  # Token inválido
          print("Token de acesso inválido ou expirado")
          return None
        else:
          print(f"Erro na API do Spotify: {response.status_code} - {response.text}")
          return None

      except requests.RequestException as e:
        print(f"Erro de conexão (tentativa {attempt + 1}/{retries}): {e}")
        if attempt < retries - 1:
          time.sleep(2 ** attempt)  # Backoff exponencial
          continue

    return None

  def get_user_profile(self, access_token):
    """Busca perfil do usuário"""
    return self._make_spotify_request(access_token, "me")

  def get_top_tracks(self, access_token, time_range="medium_term", limit=20):
    """Busca top tracks do usuário"""
    endpoint = f"me/top/tracks?time_range={time_range}&limit={limit}"
    return self._make_spotify_request(access_token, endpoint)

  def get_top_artists(self, access_token, time_range="medium_term", limit=20):
    """Busca top artists do usuário"""
    endpoint = f"me/top/artists?time_range={time_range}&limit={limit}"
    return self._make_spotify_request(access_token, endpoint)

  def get_recently_played(self, access_token, limit=50):
    """Busca músicas tocadas recentemente"""
    endpoint = f"me/player/recently-played?limit={limit}"
    return self._make_spotify_request(access_token, endpoint)

  def get_audio_features(self, access_token, track_ids):
    """Busca características de áudio das tracks"""
    if isinstance(track_ids, list):
      track_ids = ','.join(track_ids)

    endpoint = f"audio-features?ids={track_ids}"
    return self._make_spotify_request(access_token, endpoint)

  def get_current_playback(self, access_token):
    """Busca reprodução atual"""
    return self._make_spotify_request(access_token, "me/player")
