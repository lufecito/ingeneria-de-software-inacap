# Catálogo de Requerimientos

**Estado:** borrador de trabajo (Etapa 1: caso simulado, pendiente de validación con usuarios reales).
**Sección del informe:** III. Desarrollo → 2. Levantamiento de Requerimientos.
**Base:** alcance definido en `docs/01-formulacion-problema.md` y OE3 de `docs/02-objetivos.md`.

---

## 1. Método de levantamiento

En la primera etapa el catálogo se deriva del caso simulado. En la segunda etapa se contrasta mediante entrevistas y observación del proceso real, registrando qué requisito se confirma, se modifica o se descarta. Cada requisito conserva su origen para que la validación sea verificable.

**Prioridad (MoSCoW):** M = debe estar, S = debería estar, C = podría estar.

## 2. Actores del sistema

| Actor | Responsabilidad principal |
|---|---|
| Administrador | Gestiona usuarios, roles, catálogo y parámetros |
| Encargado de bodega | Registra entradas, salidas y anulaciones |
| Jefe de servicio | Solicita insumos y autoriza salidas de su unidad |
| Auditor | Consulta historial y reportes sin modificar registros |

## 3. Requisitos funcionales

| ID | Requisito | Prioridad | Criterio de aceptación resumido |
|---|---|---|---|
| RF-01 | El sistema autentica usuarios con credenciales y asigna el rol correspondiente. | M | Un usuario con credenciales válidas accede solo a las funciones de su rol; con credenciales inválidas no accede. |
| RF-02 | El administrador gestiona usuarios, roles y estado de habilitación. | M | Un usuario deshabilitado no puede iniciar sesión y conserva su historial asociado. |
| RF-03 | El administrador mantiene el catálogo de insumos con código, nombre, categoría, unidad de medida y stock mínimo. | M | Un insumo creado queda disponible para movimientos; no admite códigos duplicados. |
| RF-04 | El administrador mantiene las categorías de insumos. | S | Una categoría con insumos asociados no puede eliminarse. |
| RF-05 | El encargado de bodega registra entradas indicando insumo, cantidad, documento de referencia y, cuando corresponde, lote y vencimiento. | M | La entrada incrementa la existencia y queda en el historial con usuario y fecha. |
| RF-06 | El encargado de bodega registra salidas asociadas a un servicio solicitante, un responsable y la persona que autoriza. | M | La salida descuenta existencia y registra servicio, responsable, autorizante, usuario y fecha. |
| RF-07 | El encargado de bodega anula un movimiento indicando motivo, sin eliminar el registro original. | M | El movimiento anulado deja de afectar la existencia, permanece consultable y conserva el motivo. |
| RF-08 | Los usuarios autorizados consultan existencias por insumo y categoría, y el consumo acumulado por servicio. | M | La consulta refleja el efecto de los movimientos registrados al momento de la solicitud. |
| RF-09 | El sistema alerta los insumos cuya existencia es igual o inferior al stock mínimo definido. | M | Al alcanzar el umbral, el insumo aparece en la lista de alertas. |
| RF-10 | El sistema registra lotes y fechas de vencimiento y alerta los próximos vencimientos. | M | Los insumos con control de lote exigen lote y vencimiento en la entrada; la alerta se activa 30 días antes del vencimiento. |
| RF-11 | Los usuarios autorizados consultan el historial de movimientos con filtros por insumo, servicio, tipo y rango de fechas. | M | El historial devuelve únicamente los movimientos que cumplen los filtros aplicados. |
| RF-12 | El sistema genera reportes de existencias, consumo por servicio y próximos vencimientos. | S | El reporte exportado coincide con los datos consultados en pantalla. |
| RF-13 | El sistema registra una bitácora de acciones sensibles: inicio de sesión, cambios de catálogo y anulaciones. | M | Toda acción sensible queda registrada con usuario, fecha y resultado. |
| RF-14 | El jefe de servicio consulta el consumo registrado de su unidad y la disponibilidad del catálogo, sin acceso a registros de otras unidades. | S | El jefe de servicio accede solo a la información de su servicio. |
| RF-15 | El sistema admite la carga inicial del catálogo desde un archivo estructurado. | C | Una carga válida incorpora los insumos; una fila inválida se informa y no se incorpora. |

## 4. Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | No se registra una salida cuya cantidad supere la existencia disponible del insumo. |
| RN-02 | Toda salida requiere un servicio solicitante y un responsable identificado. |
| RN-03 | La alerta de stock se activa cuando la existencia es igual o inferior al stock mínimo del insumo. |
| RN-04 | Los insumos marcados con control de lote requieren lote y fecha de vencimiento en cada entrada. |
| RN-05 | Las salidas consumen primero los lotes de vencimiento más próximo (FEFO). |
| RN-06 | Los movimientos no se eliminan físicamente; solo se anulan con motivo registrado. |
| RN-07 | La unidad de medida de un insumo no puede modificarse si existen movimientos asociados. |
| RN-08 | Un insumo inactivo no admite nuevos movimientos, pero conserva su historial. |
| RN-09 | Toda anulación genera un movimiento de reversión vinculado; el movimiento original se conserva marcado como anulado. |
| RN-10 | Un lote vencido no puede utilizarse en una salida, aunque mantenga saldo. |
| RN-11 | Los ajustes por conteo requieren rol de administrador y un motivo registrado. |
| RN-12 | El saldo de una existencia nunca puede ser negativo; la restricción se garantiza en la base de datos. |
| RN-13 | No se revierte una entrada cuyos lotes ya registran salidas; la corrección se realiza mediante ajuste por conteo con motivo. |
| RN-14 | La alerta de próximos vencimientos cubre los lotes con saldo que vencen dentro de 30 días; el umbral es configurable por el administrador. |

## 5. Requisitos no funcionales

| ID | Categoría | Requisito | Criterio verificable |
|---|---|---|---|
| RNF-01 | Usabilidad | Registrar una salida completa no debe requerir más de tres pasos. | Prueba de usabilidad con un usuario del rol bodega. |
| RNF-02 | Rendimiento | La consulta de existencias responde en menos de un segundo con el volumen simulado. | Medición con 320 insumos y 50.000 movimientos. |
| RNF-03 | Disponibilidad | El sistema opera en horario de bodega con disponibilidad objetivo de 99 %. | Monitoreo mensual del servicio. |
| RNF-04 | Seguridad | Las contraseñas se almacenan con función de hash y sal; las sesiones expiran por inactividad. | Revisión de configuración y prueba de expiración. |
| RNF-05 | Privacidad | El sistema no almacena datos de pacientes ni información clínica individual. | Revisión del modelo de datos. |
| RNF-06 | Auditabilidad | Los movimientos son inmutables y toda anulación conserva el registro original. | Prueba de anulación y consulta posterior. |
| RNF-07 | Compatibilidad | El sistema opera en navegadores web actuales sin instalación en el cliente. | Prueba en dos navegadores distintos. |
| RNF-08 | Mantenibilidad | Las reglas de negocio cuentan con pruebas automatizadas. | Ejecución de la suite en integración continua. |
| RNF-09 | Respaldo | La base de datos se respalda diariamente, con recuperación objetivo de cuatro horas. | Ensayo de restauración documentado. |
| RNF-10 | Localización | Interfaz en español de Chile, fechas en formato dd-mm-aaaa y separador decimal con coma. | Revisión de interfaz y reportes. |

## 6. Criterios de aceptación detallados

**RF-06 · Registro de salida**

```gherkin
Dado un insumo con existencia 50 y un servicio solicitante autorizado
Cuando el encargado de bodega registra una salida de 10 unidades
Entonces la existencia resultante es 40
Y el movimiento queda en el historial con usuario, fecha, servicio y responsable
```

**RN-01 · Salida sobre el stock**

```gherkin
Dado un insumo con existencia 5
Cuando se intenta registrar una salida de 8 unidades
Entonces el sistema rechaza la operación
Y la existencia permanece en 5
Y se informa el motivo del rechazo
```

**RF-07 · Anulación**

```gherkin
Dado un movimiento de salida registrado
Cuando el encargado de bodega lo anula indicando un motivo
Entonces la existencia se restituye
Y el movimiento permanece consultable como anulado
Y el motivo queda asociado al registro
```

**RF-09 · Alerta de stock mínimo**

```gherkin
Dado un insumo con stock mínimo 20 y existencia 20
Cuando se consulta la lista de alertas
Entonces el insumo aparece en la lista
Y al registrar una entrada que eleva la existencia a 21 deja de aparecer
```

## 7. Trazabilidad

| Requisito | Objetivo | Problema que atiende |
|---|---|---|
| RF-05, RF-06, RF-11 | OE3 | Falta de trazabilidad de movimientos y responsables |
| RF-08, RF-09 | OE3 | Desconocimiento de existencias y quiebres de stock |
| RF-10 | OE3 | Pérdidas por vencimiento |
| RF-07, RF-13 | OE3 | Diferencias de inventario sin evidencia |
| RNF-04, RNF-05, RNF-06 | OE3, OE8 | Resguardo de información y auditabilidad |

## 8. Pendiente

Los requisitos marcados M constituyen el mínimo de la primera versión. La prioridad definitiva se ajusta después de la validación con usuarios reales, que puede reordenar el alcance sin alterar los identificadores.

## 9. Registro de cambios

| Fecha | Requisito | Cambio | Origen | Impacto |
|---|---|---|---|---|
| 17 nov 2026 | RF-06 | Se incorpora la persona que autoriza a los datos obligatorios de la salida | Decisión D-02 del modelo de datos: el vale autorizado se representa sin entidad de solicitud | Aceptación modificada; sin cambio de alcance |
| 17 nov 2026 | RF-08 | Se separa la consulta de existencias de la consulta de consumo por servicio | Decisión D-01: los servicios no mantienen stock propio | Aclaración de alcance |
| 17 nov 2026 | RF-14 | Se precisa que el jefe de servicio consulta consumo propio y disponibilidad, no stock de su unidad | Decisión D-01 | Aclaración de alcance |
| 17 nov 2026 | RN-09 a RN-12 | Se incorporan reglas de reversión, vencimiento, ajuste y saldo no negativo | Hallazgos del diseño transaccional | Cuatro reglas nuevas; criterios de prueba asociados |
| 17 nov 2026 | RN-13 | Se bloquea la reversión de una entrada cuyos lotes ya registran salidas | Decisión D-06 del modelo de datos | Una regla nueva; exige ajuste por conteo como vía de corrección |
| 17 nov 2026 | RF-10, RN-14 | Se fija en 30 días el horizonte de alerta de vencimientos, configurable | Definición del equipo | Aceptación modificada; una regla nueva |

Estos cambios son anteriores al congelamiento de requisitos del 24 de noviembre y no alteran el esfuerzo estimado del cronograma.
