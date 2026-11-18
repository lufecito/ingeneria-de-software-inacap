# Sistema de gestión de inventario de insumos médicos

Informe de **Formulación y Diseño** para la asignatura Ingeniería de Software (INACAP), Unidad 1.

El proyecto define un sistema de inventario de insumos médicos **no medicamentosos** para hospitales públicos y consultorios, formulado sobre un caso simulado y diseñado con Django y PostgreSQL. **El software todavía no está implementado**: este repositorio contiene la formulación, el diseño y el generador del informe.

## Estado

| Sección del informe | Estado |
|---|---|
| I. Introducción | Redactada |
| II. Objetivos | Redactado |
| III. Desarrollo (formulación, requisitos, arquitectura, UML, pruebas, gestión, calidad, cronograma) | Redactado |
| IV. Conclusiones | Redactado (2 páginas) |
| V. Referencias | Redactado (APA) |

Pendiente: revisión de forma del documento final y actualización del índice en Word.

## Estructura

```
docs/                      Fuente del informe en Markdown
  00-introduccion.md
  01-formulacion-problema.md
  02-objetivos.md
  03-requerimientos.md
  04-cronograma.md
  05-metodologia.md
  06-arquitectura.md
  07-modelo-datos.md
  08-uml.md
  09-pruebas.md
  10-gestion-calidad-evolucion.md
  11-conclusiones.md
  12-referencias.md
assets/diagramas/          Diagramas renderizados (PNG) y su fuente Mermaid
tools/build_informe.py     Genera el .docx desde docs/
tools/render_diagramas.py  Renderiza los bloques Mermaid a PNG
Informe_U1_Ingenieria_de_Software.docx
```

## Regenerar el documento

Requisitos: Python 3 con `python-docx` y Node con `@mermaid-js/mermaid-cli`.

```bash
python3 -m venv .venv
.venv/bin/pip install python-docx

# Diagramas (una sola vez, o al modificarlos)
.venv/bin/python tools/render_diagramas.py

# Documento
.venv/bin/python tools/build_informe.py
```

El generador necesita la plantilla institucional `Formato_Informe_U1_Ingenieria de software.docx` en la raíz. No se incluye en este repositorio.

## Alcance del sistema

Incluye catálogo de insumos, entradas y salidas con responsable y autorizante, existencias, alertas de stock mínimo, control de lotes con vencimiento a 30 días, historial, reportes, roles por servicio y bitácora de auditoría.

Fuera de alcance: medicamentos, datos de pacientes, facturación, integración con sistemas institucionales, múltiples bodegas y aplicación móvil.

## Advertencia metodológica

Los requisitos provienen de un caso simulado (**Hospital Público Valle Norte**, ficticio). No se presentan como necesidades verificadas de una institución real. Las metas de indicadores son propuestas, no mediciones.

## Integrantes

Completar con los nombres del equipo.

## Licencia

Uso académico.
