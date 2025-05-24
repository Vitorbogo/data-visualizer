# 🚨 IMPORTANTE: Mudança na Política de Redirect URI do Spotify

## ⚠️ Atualização Crítica - Maio 2025

A partir de **9 de abril de 2025**, o Spotify começou a aplicar validações mais rigorosas para redirect URIs:

### ❌ O que NÃO funciona mais:

```
http://localhost:5000/callback
```

### ✅ O que você DEVE usar:

```
http://127.0.0.1:5000/callback
```

## 🔧 Como Corrigir

### 1. No Spotify Developer Dashboard

1. Acesse: https://developer.spotify.com/dashboard
2. Abra seu app "Personal Data Visualizer"
3. Vá em **Settings**
4. Em **Redirect URIs**, remova: `http://localhost:5000/callback`
5. Adicione: `http://127.0.0.1:5000/callback`
6. Clique em **Save**

### 2. No seu arquivo .env

```env
# CORRETO (novo)
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback

# INCORRETO (antigo - não funciona mais)
# SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
```

## 📋 Verificação

Para confirmar que está tudo correto:

1. **Arquivo `.env`** deve ter:

   ```env
   SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
   ```

2. **Spotify Dashboard** deve mostrar:

   ```
   Redirect URIs: http://127.0.0.1:5000/callback
   ```

3. **Acesso à aplicação**:
   - Continue acessando: `http://localhost:5000` (funciona normalmente)
   - O redirect automaticamente usará `127.0.0.1:5000/callback`

## 🤔 Por que esta mudança?

Segundo a [documentação oficial do Spotify](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri):

> **"localhost is not allowed as redirect URI"**

A nova política exige:

- **HTTPS** para redirect URIs públicos
- **Endereços de loopback explícitos** (`127.0.0.1` ou `[::1]`) para desenvolvimento local
- **Sem `localhost`** para maior segurança

## ⚡ Solução Rápida

Se você já tem o projeto rodando:

1. **Pare a aplicação** (Ctrl+C)
2. **Edite o .env**: `SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback`
3. **Atualize o Spotify Dashboard** com o novo URI
4. **Reinicie**: `python app.py`
5. **Teste o login** novamente

## 📞 Problemas?

Se ainda tiver erro de `invalid_redirect_uri`:

1. Confirme que não há espaços extras no .env
2. Verifique se salvou as mudanças no Spotify Dashboard
3. Aguarde alguns minutos para as mudanças se propagarem
4. Tente fazer logout e login novamente no Spotify

---

**Data da mudança**: Abril 2025  
**Data limite**: Novembro 2025  
**Status no projeto**: ✅ Corrigido
