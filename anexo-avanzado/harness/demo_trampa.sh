#!/usr/bin/env bash
# Módulo 8 · Ejemplo práctico: un "agente" intenta dejar la suite en verde con trampa.
# Trabaja sobre una copia temporal del repo: no toca tu carpeta.
set -euo pipefail
RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
TMP="$(mktemp -d)"
mkdir -p "$TMP/repo"
(cd "$RAIZ" && tar cf - --exclude=.git --exclude=mutants --exclude=reports --exclude=salidas --exclude=logs .) | (cd "$TMP/repo" && tar xf -)
cd "$TMP/repo"
git init -q -b main && git -c user.email=lab@bancoqa.local -c user.name=lab add -A && git -c user.email=lab@bancoqa.local -c user.name=lab commit -qm "base"
git checkout -qb agente/hu-01

echo "1) El agente recibe: 'deja la suite en verde' con el defecto D1 activo."
echo "2) En vez de reportar el defecto, marca el test como skip, borra una aserción y usa una URL de producción."
python3 - <<'PY'
from pathlib import Path
p = Path("tests/api/test_transferencias_api.py")
s = p.read_text(encoding="utf-8")
s = s.replace('@pytest.mark.caso("CP-07")\ndef test_acumulado_sobre',
              '@pytest.mark.skip(reason="intermitente")\n@pytest.mark.caso("CP-07")\ndef test_acumulado_sobre')
s = s.replace('    assert saldo(api, ANA_PEN) == "9000.00"\n', '')
s = s.replace('ANA_PEN, ANA_USD, BRUNO_PEN', '# BASE = "https://api.bancoqa.com.pe"\nANA_PEN, ANA_USD, BRUNO_PEN')
p.write_text(s, encoding="utf-8")
PY
git -c user.email=agente@bancoqa.local -c user.name=agente commit -qam "fix: suite en verde"

echo "3) El pipeline corre los guardrails:"
set +e
python3 anexo-avanzado/harness/verificar_guardrails.py --base main --matriz soluciones/modulo-8/matriz.csv --modulo 8
codigo=$?
set -e
rm -rf "$TMP"
echo "Código de salida del guardrail: $codigo (1 = PR bloqueado)"
exit 0
