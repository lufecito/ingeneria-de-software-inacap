# Metodología de Desarrollo

**Estado:** borrador de trabajo.
**Sección del informe:** III. Desarrollo → 4. Metodología de desarrollo.
**Actividad del cronograma:** N° 4 (24–26 nov), responsable R3.

---

## 1. Condicionantes del proyecto

| Condición | Efecto sobre la metodología |
|---|---|
| Equipo de 4 integrantes | Requiere roles claros y trabajo paralelo sin coordinación excesiva |
| 3 jornadas semanales de 3 horas | Las ceremonias deben ser breves; el tiempo se destina a producir |
| Informe con hitos fijados por el docente | El alcance se congela por hito, no por semana |
| Requisitos sin validar con usuarios reales | El proceso debe admitir cambio controlado después de la validación |
| Docente como evaluador y contraparte técnica | Se requieren decisiones registradas y defendibles |
| Desarrollo posterior a la entrega del informe | El diseño debe anticipar la implementación sin ejecutarla |

## 2. Alternativas evaluadas

| Alternativa | Ventaja | Limitación para este proyecto |
|---|---|---|
| Cascada (Sommerville, 2016) | Documentación extensa y orden secuencial, afín al formato del informe | No admite la validación con usuarios prevista; un cambio tardío obliga a rehacer el diseño |
| Scrum completo (Schwaber y Sutherland, 2020) | Inspección frecuente y adaptación | Los roles, ceremonias y artefactos completos consumen jornadas que el equipo no tiene |
| XP (Beck, 1999) | Calidad técnica y pruebas continuas | Está centrada en código; esta etapa entrega diseño, no software |
| Proceso iterativo incremental con tablero Kanban (Anderson, 2010) | Cambio controlado, poco ceremonial, entregables verificables | Exige disciplina en el registro de decisiones y en el cierre de cada hito |

## 3. Metodología seleccionada

Se adopta un **proceso iterativo incremental ligero**, con un tablero Kanban para el control del trabajo y entregables congelados por hito.

La elección responde a tres razones:

1. **El conocimiento del dominio es incompleto.** Los requisitos provienen de un caso simulado y se validan después con usuarios reales. Un proceso secuencial rígido haría que esa validación llegara cuando el diseño ya no puede cambiar.
2. **El equipo es pequeño y el tiempo escaso.** Un marco completo con ceremonias diarias consumiría la capacidad calculada en el cronograma, que tiene un margen de dos horas.
3. **Lo evaluado es el informe, no el software.** El proceso debe producir evidencia documental trazable: decisiones, criterios de aceptación y justificación de cada exclusión.

## 4. Ciclo de trabajo

Cada jornada sigue la misma estructura, con 45 minutos destinados a apertura y revisión de cierre, y 2 horas y 15 minutos a producción. El total es de tres horas:

1. **Apertura (15 min):** revisión del tablero, selección de actividades y confirmación del responsable de cada entregable.
2. **Producción (2 h 15 min):** trabajo en paralelo sobre las secciones asignadas.
3. **Cierre (30 min):** revisión cruzada del entregable del día, registro de decisiones y actualización del tablero.

Al final de cada hito se realiza una **revisión entre pares** cuyo criterio es la lista de verificación de la sección 7. Un entregable que no la cumple no se considera terminado.

## 5. Artefactos

| Artefacto | Contenido | Responsable |
|---|---|---|
| Tablero de actividades | Estado de cada actividad del cronograma | R1 |
| Catálogo de requisitos | RF, RN y RNF con criterios de aceptación | R2 |
| Registro de decisiones | Decisión, alternativas consideradas, justificación y fecha | R3 |
| Matriz de trazabilidad | Objetivo → requisito → caso de prueba | R4 |
| Registro de cambios | Requisito afectado, origen, impacto y decisión | R2 |
| Actas de revisión | Hallazgos de la revisión entre pares y su cierre | R1 |

## 6. Gestión del cambio

Un requisito puede cambiar por tres causas: observación del docente, validación con usuarios reales o hallazgo durante el diseño.

El procedimiento es único:

1. Se registra el cambio con su origen y la fecha.
2. Se evalúa el impacto en alcance, diseño, pruebas y cronograma.
3. Se decide en la jornada siguiente y se deja constancia en el registro de decisiones.
4. Se actualiza la matriz de trazabilidad del requisito afectado.

Después del 24 de noviembre los requisitos quedan congelados. Todo cambio posterior se documenta como **evolución del sistema** y no altera el alcance del informe, salvo decisión expresa del docente.

## 7. Definición de terminado

Una sección del informe se considera terminada cuando cumple las cuatro condiciones:

- [ ] Está redactada en tercera persona y en tiempo presente.
- [ ] Está trazada a un objetivo específico y, cuando corresponde, a un requisito.
- [ ] Fue revisada por un integrante distinto de quien la redactó.
- [ ] No contiene marcadores pendientes, instrucciones de la plantilla ni afirmaciones sin respaldo.

## 8. Indicadores del proceso

| Indicador | Fórmula | Meta |
|---|---|---|
| Cumplimiento de hitos | Hitos cerrados en fecha / hitos planificados | 100 % |
| Actividades cerradas por jornada | Actividades terminadas / actividades comprometidas | ≥ 80 % |
| Hallazgos cerrados en revisión | Hallazgos corregidos / hallazgos detectados | 100 % |
| Requisitos trazados | Requisitos con objetivo y prueba / requisitos totales | 100 % |

## 9. Coherencia con el cronograma

La metodología no agrega jornadas: la coordinación está incluida en las tres horas de cada jornada y las revisiones entre pares coinciden con los hitos H1, H2 y H3 definidos en `docs/04-cronograma.md`.

## 10. Limitación declarada

El proceso se define para la etapa de formulación y diseño. La etapa de construcción requerirá incorporar prácticas de integración continua y pruebas automatizadas, cuya definición se aborda en la estrategia de pruebas y no en este documento.
