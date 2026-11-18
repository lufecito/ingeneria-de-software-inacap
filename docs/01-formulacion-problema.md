# Formulación del Proyecto — Sistema de Gestión de Inventario de Insumos Médicos

**Estado:** borrador de trabajo para revisión del equipo (Etapa 1: caso simulado).
**Sección del informe:** III. Desarrollo → 1. Formulación del Proyecto.
**Redacción:** tercera persona, tiempo presente, español neutro.

> **Advertencia metodológica.** El establecimiento, las cifras y los procesos descritos en este documento son un **caso simulado** construido para formular el proyecto. No corresponden a una institución real ni a datos obtenidos de pacientes, funcionarios o registros clínicos. Toda afirmación sobre la realidad de los establecimientos se declara explícitamente como **supuesto a validar** en la Etapa 2.

---

## 1. Identificación del caso de estudio simulado

| Campo | Definición |
|---|---|
| Establecimiento | Hospital Público Valle Norte (ficticio) |
| Tipo | Hospital de mediana complejidad, dependiente del servicio de salud de una comuna ficticia |
| Unidad piloto | Bodega Central de Insumos |
| Población atendida | Consultorio adosado y cuatro servicios clínicos de referencia |
| Dotación simulada | 180 funcionarios; 12 usuarios del sistema |
| Catálogo simulado | 320 insumos médicos no medicamentosos, agrupados en 9 categorías |
| Volumen simulado | 1.500 movimientos mensuales; 40 solicitudes diarias en promedio |
| Registro actual | Planilla de cálculo por bodega y vales de salida en papel |
| Periodicidad de control | Inventario físico mensual; conciliación manual |

### 1.1 Insumos considerados

Guantes de examen y quirúrgicos, gasas y apósitos, jeringas y agujas, suturas, material de curación, alcohol y soluciones de aseo, elementos de protección personal, sondas y catéteres, material de esterilización.

**Excluidos de la primera versión:** medicamentos, dispositivos implantables, reactivos de laboratorio y gases medicinales.

### 1.2 Actores simulados

| Actor | Rol en el proceso |
|---|---|
| Encargado de bodega | Registra entradas y salidas; responsable de la exactitud del stock |
| Jefe de servicio clínico | Solicita insumos y responde por el consumo de su unidad |
| Funcionario solicitante | Retira insumos con vale autorizado |
| Administrador del sistema | Gestiona usuarios, catálogo y parámetros de stock mínimo |
| Auditor interno | Revisa trazabilidad y diferencias de inventario |

### 1.3 Proceso actual simulado

1. El servicio clínico completa un vale de solicitud en papel.
2. El jefe de servicio autoriza la solicitud de forma manuscrita.
3. El encargado de bodega entrega los insumos y descuenta la cantidad en una planilla.
4. Al cierre de mes se compara la planilla con el conteo físico.
5. Las diferencias se investigan sin registro histórico de movimientos que permita reconstruir la causa.

---

## 2. Introducción y formulación del problema

### 2.1 Contexto

Los hospitales públicos y consultorios administran un volumen alto de insumos de uso clínico diario. La disponibilidad oportuna de estos insumos condiciona la continuidad de la atención, mientras que su control deficiente se traduce en compras de emergencia, pérdidas por vencimiento y diferencias de inventario difíciles de explicar.

En el caso simulado, la bodega central registra sus movimientos en una planilla y en vales de papel. No existe una fuente única que permita conocer la existencia disponible en un momento dado ni reconstruir quién retiró qué insumo, cuándo y para qué unidad.

### 2.2 Problema

La bodega central del establecimiento no dispone de información oportuna y confiable sobre las existencias y los movimientos de insumos médicos, lo que impide detectar quiebres de stock, controlar vencimientos y justificar las diferencias de inventario.

### 2.3 Consecuencias observadas en el caso simulado

- Solicitudes urgentes que no pueden atenderse por falta de disponibilidad conocida.
- Consumo no atribuible a una unidad, sin trazabilidad del responsable.
- Pérdidas por insumos vencidos detectadas solo en el conteo físico.
- Tiempo del encargado de bodega destinado a consolidar registros manuales.

Estas consecuencias describen el escenario simulado y **no constituyen evidencia empírica**; su magnitud real se determinará en la Etapa 2.

### 2.4 Supuestos a validar con usuarios reales

| # | Supuesto | Cómo se valida |
|---|---|---|
| S1 | El registro de movimientos se realiza de forma manual o semiautomatizada | Entrevista al encargado de bodega |
| S2 | No existe consulta en línea de existencias por unidad | Observación del proceso y revisión de registros |
| S3 | El control de vencimientos es reactivo | Entrevista y revisión del procedimiento vigente |
| S4 | La trazabilidad por responsable y unidad es insuficiente | Revisión de vales y planillas |
| S5 | El establecimiento opera con una bodega única para estos insumos | Entrevista a jefatura administrativa |

### 2.5 Justificación

Un sistema que centralice el catálogo, registre cada movimiento con responsable y unidad, y exponga existencias y alertas en tiempo de consulta permite reemplazar la conciliación manual por un control verificable. El beneficio esperado es la reducción de quiebres no detectados, la disminución de pérdidas por vencimiento y la disponibilidad de evidencia para auditoría.

---

## 3. Alcance

La primera versión del sistema contempla:

1. Catálogo de insumos con categoría, unidad de medida y stock mínimo.
2. Registro de entradas por recepción de bodega.
3. Registro de salidas por solicitud autorizada, asociadas a servicio y responsable.
4. Consulta de existencias por insumo y por categoría.
5. Alertas de stock bajo el mínimo definido.
6. Control de lotes y fechas de vencimiento en los insumos que lo requieran.
7. Historial de movimientos con usuario, fecha, cantidad y unidad de destino.
8. Reportes básicos de existencias, consumo por unidad y próximos vencimientos.
9. Roles diferenciados: administrador, encargado de bodega, jefe de servicio y auditor.

**Establecimiento piloto:** una bodega de un establecimiento. La operación multicentro se aborda como evolución posterior.

## 4. Fuera de alcance

- Medicamentos, dispositivos implantables, reactivos y gases medicinales.
- Fichas clínicas, datos de pacientes y cualquier información de salud individual.
- Prescripciones, recetas y órdenes médicas.
- Facturación, contabilidad y gestión de compras a proveedores.
- Integración con sistemas institucionales existentes.
- Transferencias entre establecimientos y gestión de múltiples bodegas.
- Aplicación móvil nativa en la primera versión.

Cada exclusión se documenta como candidata a una segunda etapa, considerando su impacto en plazo y complejidad.

---

## 5. Trazabilidad hacia el informe

| Sección del informe | Estado |
|---|---|
| III.1 Formulación del Proyecto | Cubierta por este documento |
| III.1 Identificación del problema | Cubierta (secciones 1 y 2) |
| III.1 Introducción y formulación del problema | Cubierta (sección 2) |
| III.1 Alcance y fuera de alcance | Cubierta (secciones 3 y 4) |
| II. Objetivos | Cubierta (`docs/02-objetivos.md`) |
| III.2 Levantamiento de Requerimientos | Cubierta en borrador (`docs/03-requerimientos.md`) |
| III.3 Metodología de desarrollo | Cubierta (`docs/05-metodologia.md`) |
| III.4 Arquitectura y diseño de software | Cubierta (`docs/06-arquitectura.md`) |
| III.5 Diagramas UML y modelo Entidad-Relación | Cubierta (`docs/07-modelo-datos.md`, `docs/08-uml.md`) |
| III.6 Desarrollo y codificación | **No forma parte de esta entrega**: la implementación corresponde a la etapa posterior, según lo indicado en clase |
| III.7 Estrategia y matriz de pruebas | Cubierta (`docs/09-pruebas.md`) |
| III.8 Gestión del proyecto, roles y riesgos | Cubierta (`docs/10-gestion-calidad-evolucion.md`) |
| III.9 Mantenimiento y evolución | Cubierta (`docs/10-gestion-calidad-evolucion.md`) |
| III.10 Calidad y KPI/métricas | Cubierta (`docs/10-gestion-calidad-evolucion.md`) |
| III.11 Cronograma | Cubierta (`docs/04-cronograma.md`) |
| I. Introducción | Cubierta (`docs/00-introduccion.md`) |
| IV. Conclusiones | Cubierta (`docs/11-conclusiones.md`) |
| V. Referencias bibliográficas | Cubierta (`docs/12-referencias.md`) |

## 6. Próximo paso

Redactar los objetivos general y específicos, y derivar de ellos el catálogo de requisitos funcionales y no funcionales con criterios de aceptación, manteniendo la distinción entre supuesto simulado y requisito validado.
