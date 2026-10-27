---
name: "🐞 Reporte de defecto"
about: Informar un fallo reproducible del sistema
title: "BUG: [resumen breve del fallo]"
labels: ["bug", "status: triage"]
assignees: []
---

<!-- Completá TODAS las secciones. Un issue incompleto vuelve a "status: needs-info". -->

## 1. Descripción técnica del problema
<!-- Qué falla, en qué módulo/endpoint/pantalla, y desde cuándo (versión o commit). -->
- **Módulo / componente:**
- **Versión o commit (`git rev-parse --short HEAD`):**
- **Descripción:**

## 2. Entorno
| Campo | Valor |
|---|---|
| SO | |
| Navegador / runtime (ej. Python 3.13) | |
| Entorno (local / staging / fork) | |
| Datos de prueba usados | |

## 3. Pasos exactos para reproducir
<!-- Lista numerada y determinista: otra persona debe obtener el mismo fallo siguiéndola. -->
1.
2.
3.

**Frecuencia:** ☐ Siempre ☐ Intermitente (__ de __ intentos)

## 4. Comportamiento esperado
<!-- Qué debería pasar según la especificación / criterio de aceptación (citá la HU o el requisito). -->

## 5. Comportamiento observado
<!-- Qué pasó realmente: mensaje de error, código HTTP, valor incorrecto, congelamiento, etc. -->

## 6. Severidad e impacto
- **Severidad:** ☐ `severity: critical` ☐ `severity: major` ☐ `severity: minor`
- **Usuarios / funcionalidades afectadas:**
- **¿Existe workaround?** ☐ Sí ☐ No → describir:

## 7. Evidencias adjuntas
<!-- Capturas, stack trace, logs de consola, request/response. Pegá logs en bloque de código. -->
```text
(pegar log o stack trace)
```

## 8. Checklist del reportante
- [ ] Busqué issues duplicados antes de abrir este.
- [ ] Los pasos reproducen el fallo en un entorno limpio.
- [ ] Adjunté al menos una evidencia.
