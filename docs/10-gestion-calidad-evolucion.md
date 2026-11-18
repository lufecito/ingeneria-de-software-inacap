# Gestión del proyecto, calidad y evolución

**Estado:** propuesta de trabajo.
**Secciones del informe:** III. Desarrollo → Gestión del proyecto, roles y riesgos · Calidad y KPI/métricas · Mantenimiento y evolución.
**Complementa:** `docs/04-cronograma.md`, que contiene los riesgos de plazo.

---

# 1. Gestión del proyecto y roles

## 1.1 Matriz de responsabilidades

R = responsable del entregable · A = aprueba · C = colabora · I = informado

| Actividad | R1 | R2 | R3 | R4 | Docente |
|---|---|---|---|---|---|
| Formulación y alcance | R | A | C | I | A |
| Objetivos | C | R | I | I | A |
| Requisitos y reglas | C | R | I | C | A |
| Metodología | I | C | R | I | I |
| Arquitectura | C | I | R | C | A |
| Modelo entidad-relación | I | I | C | R | A |
| Diagramas UML | C | I | C | R | A |
| Matriz de pruebas | I | C | I | R | I |
| Riesgos y cronograma | A | R | I | I | I |
| Indicadores y calidad | C | R | I | C | I |
| Mantenimiento y evolución | R | C | C | I | I |
| Redacción integrada | R | C | C | C | — |
| Entrega | R | C | C | C | A |

## 1.2 Reglas de trabajo del equipo

1. Cada entregable tiene un responsable único; el resto colabora sin reemplazar la responsabilidad.
2. Ninguna sección se cierra sin revisión de un integrante distinto de quien la redactó.
3. Las decisiones se registran con su alternativa descartada; una decisión sin alternativa registrada no es una decisión, es una preferencia.
4. El docente actúa como contraparte técnica: sus observaciones se registran y se responden en el registro de cambios.
5. El repositorio es la fuente única del documento, los diagramas y las pruebas.

## 1.3 Riesgos del proyecto

Distintos de los riesgos de plazo `RC-01` a `RC-06` del cronograma: estos afectan la calidad o la viabilidad del resultado.

| ID | Riesgo | Prob. | Impacto | Mitigación | Resp. |
|---|---|---|---|---|---|
| RP-01 | El equipo presenta supuestos del caso simulado como hechos verificados | Alta | Alto | Advertencia metodológica en el documento y separación explícita entre supuesto y evidencia | R2 |
| RP-02 | Dependencia de una sola persona por sección | Media | Alto | Revisión cruzada obligatoria y documentación en el repositorio | R1 |
| RP-03 | Crecimiento del alcance por funcionalidades "que serían útiles" | Alta | Alto | Alcance congelado el 24 de noviembre; toda idea nueva va a la lista de evolución | R1 |
| RP-04 | Pérdida de trabajo por archivos dispersos o sin respaldo | Media | Alto | Repositorio Git con commits por hito y respaldo del documento | R3 |
| RP-05 | Herramientas de generación del documento no disponibles al cierre | Confirmado | Medio | Resolver la herramienta antes del 8 de diciembre, no el día de la entrega | R1 |
| RP-06 | Curva de aprendizaje de Django y PostgreSQL mayor a la estimada | Media | Medio | Prototipo mínimo antes de la etapa de construcción | R4 |
| RP-07 | Diagramas inconsistentes con el texto del informe | Media | Medio | Los diagramas se generan desde el repositorio y se revisan junto con la sección | R4 |

**Riesgo residual aceptado:** el proyecto no tiene holgura de plazo. Cualquier desvío se absorbe reduciendo alcance, nunca extendiendo fechas sin autorización del docente.

---

# 2. Calidad y métricas

## 2.1 Modelo de calidad

Se adopta como marco el modelo de calidad de producto de **ISO/IEC 25010:2023** (ISO/IEC, 2023), restringido a las características pertinentes a este sistema:

| Característica | Aplicación concreta |
|---|---|
| Adecuación funcional | Cada regla de negocio tiene una prueba asociada |
| Fiabilidad | El inventario no se corrompe ante concurrencia o error del usuario |
| Seguridad | Roles, permisos por servicio y auditoría de operaciones |
| Capacidad de interacción | Registro de salida en no más de tres pasos |
| Mantenibilidad | Separación entre vistas, servicios y modelos; pruebas automatizadas |
| Flexibilidad | Acceso por navegador, sin instalación en el cliente |

## 2.2 Indicadores de desempeño (KPI)

| ID | Indicador | Fórmula | Meta |
|---|---|---|---|
| KPI-01 | Exactitud de inventario | Ítems coincidentes en conteo / ítems contados | ≥ 98 % |
| KPI-02 | Tiempo de registro de una salida | Mediana de segundos por registro | ≤ 60 s |
| KPI-03 | Cobertura de reglas de negocio | Reglas con prueba automatizada / total de reglas | 14 de 14 |
| KPI-04 | Trazabilidad documental | Requisitos obligatorios con caso de prueba / total | 100 % |
| KPI-05 | Disponibilidad del servicio | Horas operativas / horas del horario de bodega | ≥ 99 % |
| KPI-06 | Cumplimiento de hitos | Hitos cerrados en fecha / hitos planificados | 100 % |

## 2.3 Indicadores de riesgo (KRI)

Los KRI anticipan el problema; los KPI lo describen cuando ya ocurrió. Para este sistema importan más los primeros.

| ID | Indicador | Señal de alerta |
|---|---|---|
| KRI-01 | Quiebres de stock no anticipados por la alerta | Un solo evento indica que el stock mínimo está mal calibrado |
| KRI-02 | Pérdida por vencimiento sobre el valor recibido | Por sobre 2 % mensual |
| KRI-03 | Movimientos sin autorizante registrado | Cualquier valor distinto de cero |
| KRI-04 | Proporción de anulaciones sobre movimientos | Por sobre 3 %: sugiere error de proceso, no de sistema |
| KRI-05 | Diferencias de inventario sin justificar | Por sobre 1 % de los ítems contados |
| KRI-06 | Intentos de acceso a información de otro servicio | Cualquier ocurrencia se revisa |

Los valores meta son **propuestos** a partir del caso simulado. Su calibración requiere la línea base real que se obtiene en la validación con usuarios; presentarlos como resultados medidos sería incorrecto.

## 2.4 Cómo se mide cada indicador

| Fuente | Indicadores |
|---|---|
| Conteo físico mensual comparado con el sistema | KPI-01, KRI-05 |
| Registro de tiempos de la aplicación | KPI-02 |
| Suite de pruebas en integración continua | KPI-03, KPI-04 |
| Monitoreo del servicio | KPI-05 |
| Reportes del sistema | KRI-01 a KRI-04 |
| Bitácora de auditoría | KRI-06 |

---

# 3. Mantenimiento y evolución

## 3.1 Tipos de mantenimiento previstos

| Tipo | Alcance | Frecuencia propuesta |
|---|---|---|
| Correctivo | Defectos que afectan el registro o el saldo | Atención inmediata si es crítico |
| Preventivo | Respaldos, actualización de dependencias, revisión de índices | Mensual |
| Adaptativo | Cambios de reglas del establecimiento o del catálogo | Según necesidad |
| Perfectivo | Mejoras de usabilidad y reportes | Trimestral |

## 3.2 Condiciones de soporte propuestas

| Aspecto | Propuesta |
|---|---|
| Ventana de soporte | Horario de funcionamiento de la bodega |
| Tiempo de respuesta ante defecto crítico | 4 horas hábiles |
| Respaldo | Diario, con ensayo de restauración trimestral |
| Versionado | Esquema mayor.menor.corrección; cambios de esquema siempre con migración |
| Registro de cambios | Obligatorio por versión, con requisito o defecto asociado |

Estas condiciones son una propuesta académica, no un acuerdo de nivel de servicio vigente.

## 3.3 Hoja de evolución

Ordenada por relación entre valor y costo. Ninguna de estas funcionalidades forma parte del alcance actual.

| Fase | Funcionalidad | Motivo de postergación |
|---|---|---|
| 1 | Solicitud digital con flujo de autorización y estados | Requiere un proceso completo, no un atributo |
| 2 | Transferencias entre bodegas y servicios con saldo propio | Duplica el modelo de existencias y la conciliación |
| 3 | Conversión entre presentación de compra y unidad de consumo | Exige tabla de equivalencias y validación con bodega |
| 4 | Integración con sistemas institucionales de abastecimiento | Depende de interfaces externas no disponibles |
| 5 | Aplicación móvil para conteo en terreno | No aporta al problema central de la primera versión |
| 6 | Gestión de medicamentos | Dominio regulado, con requisitos legales y de trazabilidad propios |

La incorporación de medicamentos no es una ampliación incremental: cambia el marco regulatorio del sistema y debe evaluarse como proyecto separado.

## 3.4 Criterio de decisión para evolucionar

Una funcionalidad entra a la hoja de evolución si cumple al menos una condición:

1. Resuelve un problema observado en la operación real, no uno imaginado en el diseño.
2. Reduce un KRI por sobre su umbral durante dos meses consecutivos.
3. Es exigida por una norma o por el establecimiento.

Sin una de estas tres condiciones, la funcionalidad no se prioriza.

---

## 4. Fuentes

- ISO/IEC. (2023). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model* (ISO/IEC 25010:2023). Organización Internacional de Normalización. https://www.iso.org/standard/78176.html
- Django Software Foundation. (s. f.). *Django documentation*. https://docs.djangoproject.com/

La edición citada es la segunda, publicada en noviembre de 2023, que reemplaza a ISO/IEC 25010:2011. En esa revisión la usabilidad pasó a denominarse capacidad de interacción y la portabilidad, flexibilidad.
