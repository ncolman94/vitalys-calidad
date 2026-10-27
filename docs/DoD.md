# Definition of Done — Vitalys App

**Alcance:** aplica por igual a todo incremento (feature, bug, refactor, documentación) que se proponga integrar a `main`.
**Naturaleza:** global y técnica. Los criterios de aceptación de cada historia de usuario se suman a esta DoD, no la reemplazan.
**Regla de compuerta:** un Pull Request que incumpla **uno solo** de los seis criterios recibe la etiqueta `dod: blocked` y no puede mergearse.

| ID | Criterio | Condición verificable | Herramienta / evidencia | Momento de control |
|---|---|---|---|---|
| DoD-1 | Integridad de compilación | El paquete se importa y la suite se recolecta sin errores ni warnings críticos (`SyntaxError`, `ImportError`, `DeprecationWarning` propios). | `python -m pytest --collect-only` (exit code 0) | Pre-commit (paso 3) |
| DoD-2 | Validación de pruebas automatizadas | El 100 % de las pruebas unitarias pasa. Un solo test en rojo veta la integración. | `pytest` → `junit-report.xml` con `failures="0" errors="0"` | Pre-commit (paso 3) |
| DoD-3 | Umbral mínimo de cobertura | ≥ 80 % de cobertura combinada de **sentencias y ramas** sobre `src/vitalys`. El código nuevo no puede bajar el porcentaje existente. | `pytest --cov --cov-branch --cov-fail-under=80` → `coverage.xml` / HTML | Pre-commit (paso 3) |
| DoD-4 | Revisión por pares obligatoria | Al menos 1 aprobación de un integrante distinto del autor, con los comentarios resueltos. El revisor verifica patrones, complejidad y que el PR referencie su issue. | Pull Request en GitHub (pestaña *Reviews*) | Antes del merge |
| DoD-5 | Gobernanza de estilo | Black sin cambios pendientes y Ruff sin observaciones (incluye complejidad ciclomática ≤ 10 por función, regla C901). | `black --check`, `ruff check` | Pre-commit (pasos 1 y 2) |
| DoD-6 | Sustento de la documentación técnica | Toda función pública con docstring. Si el cambio altera un contrato (interfaz `Protocol`, formato JSON, esquema), se actualiza la documentación correspondiente y el PR lleva la etiqueta `documentation`. Dependencias nuevas registradas en `requirements*.txt` y auditadas con `pip-audit` sin vulnerabilidades críticas. | Revisión del PR + `pip-audit` | Antes del merge |

## Cómo se audita
1. El **pre-commit hook** (`hooks/pre-commit`) bloquea localmente DoD-1, DoD-2, DoD-3 y DoD-5.
2. El **template de Pull Request** obliga a tildar los 6 criterios y adjuntar evidencias.
3. Las **etiquetas `dod:*`** reflejan el estado: `dod: blocked` → `dod: ready-for-review` → `dod: approved`.

## DoD vs. Criterios de aceptación
- **DoD:** igual para todo el código (ej.: "cobertura ≥ 80 % y Ruff sin observaciones").
- **Criterio de aceptación (HU de copago):** específico de una funcionalidad (ej.: "un paciente de 65 años abona el 50 % de la consulta").
