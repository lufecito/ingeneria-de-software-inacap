# Estrategia y matriz de pruebas

**Estado:** propuesta. No ejecutada.
**Sección del informe:** III. Desarrollo → Estrategia y matriz de pruebas.
**Deriva de:** `docs/03-requerimientos.md`, `docs/07-modelo-datos.md` y `docs/08-uml.md`.

---

## 1. Qué se espera de las pruebas

Las pruebas deben demostrar tres cosas, en este orden:

1. **Que las reglas de negocio se cumplen**, incluso cuando el usuario intenta saltarlas.
2. **Que el inventario no se corrompe** bajo operación concurrente.
3. **Que cada movimiento es explicable**: todo cambio de existencia tiene un registro que lo justifica.

Una prueba que solo confirma el camino feliz no demuestra ninguna de las tres.

## 2. Niveles y herramientas

| Nivel | Alcance | Herramienta propuesta | Frecuencia |
|---|---|---|---|
| Unitarias | Reglas de cálculo, FEFO, validaciones del dominio | pytest | Cada cambio |
| Integración | Servicios de aplicación con PostgreSQL real | pytest-django, `TransactionTestCase` | Cada cambio |
| Concurrencia | Salidas simultáneas sobre el mismo lote | pytest-django con hilos y PostgreSQL | Antes de cada entrega |
| Aceptación | Flujos completos desde la interfaz | Playwright | Antes de cada entrega |
| No funcionales | Rendimiento, respaldo y accesibilidad | Locust, ensayo de restauración, revisión manual | Hito H2 y cierre |

Las versiones de las herramientas se fijan al iniciar la implementación. Ninguna prueba de concurrencia se ejecuta sobre SQLite: `select_for_update()` no tiene efecto allí y la prueba pasaría sin haber verificado nada.

## 3. Técnicas de diseño de casos

| Técnica | Aplicación en este sistema |
|---|---|
| Partición de equivalencia | Cantidades válidas, cero, negativas y no numéricas |
| Valores límite | Saldo igual al mínimo, un punto bajo el mínimo, salida igual al saldo y salida un punto mayor |
| Tabla de decisión | Combinaciones de insumo activo, lote vencido, control de lote y saldo disponible |
| Transición de estados | Movimiento vigente, anulado, intento de segunda anulación |
| Prueba de concurrencia | Dos salidas simultáneas que en conjunto exceden el saldo |

## 4. Matriz de casos de prueba

| ID | Requisito | Escenario | Resultado esperado |
|---|---|---|---|
| CP-01 | RF-05 | Entrada de 100 unidades con lote y vencimiento | Saldo 100; movimiento registrado con usuario y fecha |
| CP-02 | RF-05, RN-04 | Entrada de insumo con control de lote sin indicar lote | Rechazo; el saldo no cambia |
| CP-03 | RF-06 | Salida de 10 unidades con saldo 50 | Saldo 40; servicio, responsable y autorizante registrados |
| CP-04 | RN-01 | Salida de 8 unidades con saldo 5 | Rechazo; saldo permanece en 5 |
| CP-05 | RN-01 | Salida de exactamente el saldo disponible | Aceptada; saldo 0; el insumo entra en alerta si el mínimo es mayor que cero |
| CP-06 | RN-12 | Intento de dejar saldo negativo por vía directa en base de datos | La restricción impide la escritura |
| CP-07 | RN-05 | Salida con dos lotes, uno con vencimiento anterior | Se consume primero el lote de vencimiento más próximo |
| CP-08 | RN-10 | Salida que solo puede cubrirse con un lote vencido | Rechazo con motivo explícito |
| CP-09 | RF-07, RN-09 | Anulación de una salida vigente | Saldo restituido; original marcado como anulado; reversión vinculada |
| CP-10 | RF-07 | Segunda anulación del mismo movimiento | Rechazo por anulación previa |
| CP-11 | RN-13 | Anulación de una entrada cuyos lotes ya tienen salidas | Rechazo; se sugiere ajuste por conteo |
| CP-12 | RN-11 | Ajuste por conteo con motivo y rol administrador | Saldo corregido; movimiento con motivo registrado |
| CP-13 | RN-11 | Ajuste intentado por rol bodega | Rechazo por permisos |
| CP-14 | RF-09, RN-03 | Existencia igual al stock mínimo | El insumo aparece en la alerta |
| CP-15 | RF-09, D-05 | Existencia bajo el mínimo solo por lotes vencidos | No aparece como disponible; sí en el reporte de vencidos |
| CP-16 | RF-11 | Historial filtrado por servicio y rango de fechas | Devuelve solo los movimientos que cumplen los filtros |
| CP-17 | RF-14 | Jefe de servicio consulta el consumo de otra unidad | Acceso denegado |
| CP-18 | RF-02 | Usuario deshabilitado intenta iniciar sesión | Acceso denegado; historial conservado |
| CP-19 | RF-13 | Anulación de un movimiento | Evento de auditoría con usuario, fecha y resultado |
| CP-20 | RN-06 | Intento de eliminar un movimiento desde el administrador | Operación no disponible |
| CP-21 | RNF-04 | Sesión inactiva supera el tiempo definido | La sesión expira y exige autenticación |
| CP-22 | RNF-02 | Consulta de existencias con 320 insumos y 50.000 movimientos | Respuesta en menos de un segundo |
| CP-23 | Concurrencia | Dos salidas simultáneas de 4 unidades con saldo 5 | Una se acepta, la otra se rechaza; saldo final 1 |
| CP-24 | RF-10, RN-14 | Lote con saldo que vence en 29, 30 y 31 días | Aparece en la alerta hasta los 30 días; a los 31 no aparece |

## 5. Prueba de concurrencia

Es la prueba que sostiene la promesa del sistema y la que más fácilmente se omite.

**Montaje:** base PostgreSQL, saldo de 5 unidades en un lote, dos transacciones que intentan registrar 4 unidades cada una, iniciadas de forma simultánea.

**Resultado esperado:** exactamente una operación confirma; la otra recibe rechazo por saldo insuficiente; el saldo final es 1; existen dos registros en auditoría, uno exitoso y uno rechazado.

**Resultado que invalida el diseño:** ambas operaciones confirman y el saldo queda en −3, o la restricción de base de datos aborta la transacción sin mensaje comprensible para el usuario.

## 6. Criterios de salida

| Criterio | Umbral |
|---|---|
| Casos de la matriz ejecutados | 100 % |
| Casos críticos aprobados (CP-04, CP-06, CP-09, CP-10, CP-11, CP-23) | 100 % |
| Defectos abiertos de severidad alta | 0 |
| Reglas de negocio con al menos una prueba automatizada | 14 de 14 |
| Requisitos con trazabilidad a un caso de prueba | Todos los marcados M |

## 7. Clasificación de defectos

| Severidad | Definición | Tratamiento |
|---|---|---|
| Crítica | Corrompe el inventario o permite acceso indebido | Bloquea la entrega |
| Alta | Incumple una regla de negocio sin corromper datos | Bloquea la entrega del requisito afectado |
| Media | Resultado incorrecto en un reporte o mensaje confuso | Se corrige antes del cierre |
| Baja | Detalle de presentación | Se registra y se prioriza |

## 8. Lo que no se prueba en esta etapa

- Integración con sistemas institucionales: fuera de alcance.
- Carga con usuarios reales: solo se simula el volumen declarado.
- Recuperación ante desastre real: se ensaya la restauración, no una caída productiva.
- Seguridad ofensiva: se revisa configuración, no se ejecuta un pentest.

Declarar estos límites es parte de la estrategia. Un informe que promete pruebas que no ejecutó pierde credibilidad en la defensa.

## 9. Evidencia para el informe

Cada ejecución deja: identificador del caso, fecha, resultado esperado, resultado obtenido, estado y defecto asociado cuando corresponda. La evidencia se adjunta en los anexos del informe y no se reconstruye de memoria al final.
