#!/bin/bash

# 🚀 Script para conectar ao GitHub
# Execute este script após criar o repositório no GitHub

# Substitua 'SEU_USERNAME' pelo seu username do GitHub
USERNAME="Vitorbogo"
REPO_NAME="personal-data-visualizer"

echo "🔗 Conectando ao GitHub..."
git remote add origin https://github.com/$USERNAME/$REPO_NAME.git

echo "📤 Fazendo push para o GitHub..."
git branch -M main
git push -u origin main

echo "✅ Projeto enviado para o GitHub com sucesso!"
echo "🌐 URL: https://github.com/$USERNAME/$REPO_NAME"
