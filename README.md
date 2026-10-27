# Vitalys App — laboratorio de calidad (Metodología de Sistemas II, Unidad 3)

Repositorio de práctica para los TP de las semanas 1, 2 y 3.

| Carpeta | Contenido | TP |
|---|---|---|
| `docs/DoD.md` | Definition of Done | TP1 |
| `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/labels.yml` | Plantillas y matriz de etiquetas | TP1 |
| `src/vitalys/`, `tests/` | Código de dominio y pruebas (AAA, Stub/Mock, ramas) | TP2 |
| `hooks/pre-commit` | Hook Formatter → Linter → Tests | TP3 |
| `src/legacy/` | Código de baja calidad bajo auditoría (excluido del linter) | TP3 |
| `evidencias/` | Logs reales del hook, cobertura y análisis estático | TP2 / TP3 |

## Puesta en marcha
```bash
python -m pip install -r requirements-dev.txt
git config core.hooksPath hooks      # activa el pre-commit hook
python -m pytest --cov --cov-branch  # suite + cobertura
```

## Análisis estático
```bash
python -m radon cc src -s -a                      # complejidad ciclomática
npx jscpd src --min-lines 4 --min-tokens 30       # duplicación
python -m pip_audit -r requirements.txt           # dependencias vs. CVE
```
`sonar-project.properties` está listo para un SonarQube local (`docker run -p 9000:9000 sonarqube:community` + `sonar-scanner`).
