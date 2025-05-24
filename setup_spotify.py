import os
import re


def setup_spotify_credentials():
  """Configura as credenciais do Spotify no arquivo .env"""

  print("🎵 CONFIGURAÇÃO DO SPOTIFY API")
  print("=" * 50)
  print()
  print("1. Acesse: https://developer.spotify.com/dashboard")
  print("2. Crie um novo App com as seguintes configurações:")
  print("   - Nome: Personal Data Visualizer")
  print("   - Redirect URI: http://localhost:5000/callback")
  print("3. Obtenha Client ID e Client Secret")
  print()

  # Solicitar credenciais
  client_id = input("Cole seu SPOTIFY_CLIENT_ID: ").strip()
  if not client_id:
    print("❌ Client ID não pode estar vazio!")
    return False

  client_secret = input("Cole seu SPOTIFY_CLIENT_SECRET: ").strip()
  if not client_secret:
    print("❌ Client Secret não pode estar vazio!")
    return False

  # Ler arquivo .env atual
  env_path = ".env"
  if not os.path.exists(env_path):
    print(f"❌ Arquivo {env_path} não encontrado!")
    return False

  with open(env_path, 'r') as f:
    content = f.read()

  # Substituir credenciais
  content = re.sub(r'SPOTIFY_CLIENT_ID=.*',
                   f'SPOTIFY_CLIENT_ID={client_id}', content)
  content = re.sub(r'SPOTIFY_CLIENT_SECRET=.*',
                   f'SPOTIFY_CLIENT_SECRET={client_secret}', content)

  # Salvar arquivo
  with open(env_path, 'w') as f:
    f.write(content)

  print()
  print("✅ Credenciais configuradas com sucesso!")
  print("✅ Agora você pode executar: python app.py")
  print()

  return True


def validate_credentials():
  """Valida se as credenciais estão configuradas"""

  try:
    from dotenv import load_dotenv
    load_dotenv()

    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    if not client_id or client_id == 'SEU_CLIENT_ID_AQUI' or not client_id.strip():
      return False, "SPOTIFY_CLIENT_ID não configurado"

    if not client_secret or client_secret == 'SEU_CLIENT_SECRET_AQUI' or not client_secret.strip():
      return False, "SPOTIFY_CLIENT_SECRET não configurado"

    return True, "Credenciais válidas"

  except Exception as e:
    return False, f"Erro ao validar: {e}"


if __name__ == "__main__":
  # Verificar se já está configurado
  is_valid, message = validate_credentials()

  if is_valid:
    print("✅ Credenciais do Spotify já estão configuradas!")
    print("✅ Execute: python app.py")
  else:
    print(f"⚠️  {message}")
    print()
    setup_spotify_credentials()
