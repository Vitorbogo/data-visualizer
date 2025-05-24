#!/usr/bin/env python3
"""
Script para verificar se não há mais scripts inline nos templates
"""

import os
import re
from pathlib import Path


def check_inline_scripts():
  """Verifica se há scripts inline nos templates"""

  templates_dir = Path("templates")
  issues = []

  if not templates_dir.exists():
    print("❌ Diretório templates não encontrado!")
    return False

  # Padrões que indicam scripts inline
  inline_patterns = [
      r'onclick\s*=',
      r'onload\s*=',
      r'onchange\s*=',
      r'onsubmit\s*=',
      r'javascript:',
      r'<script[^>]*>[^<]*[^/]</script>',  # Scripts inline não vazios
  ]

  print("🔍 Verificando templates por scripts inline...")
  print("=" * 50)

  for html_file in templates_dir.glob("*.html"):
    print(f"📄 Verificando: {html_file.name}")

    with open(html_file, 'r', encoding='utf-8') as f:
      content = f.read()

    file_issues = []

    for pattern in inline_patterns:
      matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
      for match in matches:
        line_num = content[:match.start()].count('\n') + 1
        line_content = content.split('\n')[line_num - 1].strip()
        file_issues.append({
            'pattern': pattern,
            'line': line_num,
            'content': line_content[:100] + '...' if len(line_content) > 100 else line_content
        })

    if file_issues:
      issues.extend([(html_file.name, issue) for issue in file_issues])
      print(f"  ⚠️  {len(file_issues)} problemas encontrados")
    else:
      print(f"  ✅ Limpo")

  print("\n" + "=" * 50)

  if issues:
    print(f"❌ TOTAL: {len(issues)} problemas encontrados:")
    print()

    for filename, issue in issues:
      print(f"📁 {filename}:{issue['line']}")
      print(f"   Padrão: {issue['pattern']}")
      print(f"   Linha: {issue['content']}")
      print()

    return False
  else:
    print("✅ SUCESSO: Nenhum script inline encontrado!")
    print("✅ Todos os templates estão seguros para CSP")
    return True


def check_csp_headers():
  """Verifica se os headers CSP estão configurados no Flask"""

  print("\n🔒 Verificando configuração de CSP no Flask...")
  print("=" * 50)

  app_file = Path("app.py")
  if not app_file.exists():
    print("❌ Arquivo app.py não encontrado!")
    return False

  with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

  csp_indicators = [
      '@app.after_request',
      'Content-Security-Policy',
      'script-src',
      'style-src'
  ]

  found_indicators = []
  for indicator in csp_indicators:
    if indicator in content:
      found_indicators.append(indicator)

  if len(found_indicators) >= 3:  # Pelo menos @app.after_request, CSP e script-src
    print("✅ Configuração CSP encontrada no Flask")
    print(f"✅ Indicadores encontrados: {', '.join(found_indicators)}")
    return True
  else:
    print("❌ Configuração CSP não encontrada ou incompleta")
    print(f"⚠️  Indicadores encontrados: {', '.join(found_indicators)}")
    return False


if __name__ == "__main__":
  print("🛡️  VERIFICAÇÃO DE SEGURANÇA CSP")
  print("=" * 60)

  templates_ok = check_inline_scripts()
  csp_ok = check_csp_headers()

  print("\n" + "=" * 60)
  print("📊 RESUMO:")
  print(f"   Templates limpos: {'✅' if templates_ok else '❌'}")
  print(f"   CSP configurado: {'✅' if csp_ok else '❌'}")

  if templates_ok and csp_ok:
    print("\n🎉 TUDO OK! O erro de CSP deve estar resolvido.")
    print("🌐 Teste acessando: http://127.0.0.1:5000")
  else:
    print("\n⚠️  Ainda há problemas a resolver.")
