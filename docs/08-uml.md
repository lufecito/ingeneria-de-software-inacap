# Diagramas UML

**Estado:** propuesta de diseño. No implementado.
**Sección del informe:** III. Desarrollo → Diagramas UML y modelo Entidad-Relación.
**Deriva de:** `docs/03-requerimientos.md` y `docs/07-modelo-datos.md`. El modelo entidad-relación se encuentra en ese documento; aquí se presentan casos de uso, clases, estados y secuencia.

---

## 1. Actores y casos de uso

| ID | Caso de uso | Actores | Requisitos |
|---|---|---|---|
| CU-01 | Registrar entrada de insumos | Encargado de bodega | RF-05 |
| CU-02 | Registrar salida a un servicio | Encargado de bodega | RF-06, RN-01, RN-02 |
| CU-03 | Anular movimiento | Encargado de bodega | RF-07, RN-09, RN-13 |
| CU-04 | Ajustar existencia por conteo | Administrador | RN-11 |
| CU-05 | Consultar existencias | Todos los roles | RF-08 |
| CU-06 | Consultar alertas de stock mínimo | Todos los roles | RF-09, RN-03 |
| CU-07 | Consultar próximos vencimientos | Todos los roles | RF-10 |
| CU-08 | Consultar historial de movimientos | Administrador, bodega, auditor | RF-11 |
| CU-09 | Consultar consumo del servicio | Jefe de servicio | RF-14 |
| CU-10 | Gestionar catálogo de insumos | Administrador | RF-03, RF-04 |
| CU-11 | Gestionar usuarios y roles | Administrador | RF-01, RF-02 |
| CU-12 | Consultar auditoría | Auditor | RF-13 |
| CU-13 | Generar reportes | Administrador, jefe de servicio, auditor | RF-12 |

## 2. Diagrama de casos de uso

```mermaid
flowchart LR
    BOD([Encargado de bodega])
    JEF([Jefe de servicio])
    ADM([Administrador])
    AUD([Auditor])

    subgraph SI[Gestión de inventario de insumos médicos]
        CU01(Registrar entrada)
        CU02(Registrar salida)
        CU03(Anular movimiento)
        CU04(Ajustar por conteo)
        CU05(Consultar existencias)
        CU06(Alertas de stock mínimo)
        CU07(Próximos vencimientos)
        CU08(Consultar historial)
        CU09(Consumo del servicio)
        CU10(Gestionar catálogo)
        CU11(Gestionar usuarios)
        CU12(Consultar auditoría)
        CU13(Generar reportes)
    end

    BOD --> CU01
    BOD --> CU02
    BOD --> CU03
    BOD --> CU05
    BOD --> CU06
    BOD --> CU07
    BOD --> CU08

    ADM --> CU04
    ADM --> CU10
    ADM --> CU11
    ADM --> CU05
    ADM --> CU06
    ADM --> CU08
    ADM --> CU13

    JEF --> CU09
    JEF --> CU05
    JEF --> CU06
    JEF --> CU13

    AUD --> CU08
    AUD --> CU12
    AUD --> CU13
```

## 3. Diagrama de clases

```mermaid
classDiagram
    class Categoria {
        +int id
        +str nombre
        +bool activo
    }

    class Insumo {
        +int id
        +str codigo
        +str nombre
        +str unidad_medida
        +Decimal stock_minimo
        +bool controla_lote
        +bool activo
        +existencias_disponibles() Decimal
        +esta_bajo_minimo() bool
    }

    class Lote {
        +int id
        +str numero
        +date fecha_vencimiento
        +date fecha_ingreso
        +esta_vencido() bool
        +saldo() Decimal
    }

    class Existencia {
        +int id
        +Decimal saldo
        +bloquear() void
        +aplicar(delta) void
    }

    class Movimiento {
        +int id
        +str tipo
        +Decimal cantidad
        +str estado
        +str motivo
        +str documento_referencia
        +datetime fecha_hora
        +efecto() Decimal
        +puede_anularse() bool
    }

    class Servicio {
        +int id
        +str nombre
        +bool activo
    }

    class Usuario {
        +int id
        +str username
        +str nombre
        +bool activo
        +es_autorizante_valido() bool
    }

    class EventoAuditoria {
        +int id
        +str accion
        +str entidad
        +str objeto_id
        +str resultado
        +datetime fecha_hora
    }

    Categoria "1" --> "0..*" Insumo
    Insumo "1" --> "0..*" Lote
    Lote "1" --> "1" Existencia
    Insumo "1" --> "0..*" Movimiento
    Lote "1" --> "0..*" Movimiento
    Servicio "1" --> "0..*" Movimiento
    Usuario "1" --> "0..*" Movimiento : registra
    Movimiento "0..1" --> "0..1" Movimiento : revierte
    Servicio "1" --> "0..*" Usuario
    Usuario "1" --> "0..*" EventoAuditoria
```

Los métodos del diagrama representan comportamiento del dominio. `Existencia.bloquear()` corresponde al bloqueo de fila descrito en la arquitectura y no se invoca fuera de una transacción.

## 4. Diagrama de estados del movimiento

```mermaid
stateDiagram-v2
    [*] --> VIGENTE : se registra
    VIGENTE --> ANULADO : se anula y se crea reversión
    VIGENTE --> VIGENTE : sin cambios
    ANULADO --> [*]
```

Un movimiento anulado no vuelve a estado vigente. Si la anulación fue un error, se registra un movimiento nuevo; no se reescribe la historia.

## 5. Secuencia: registrar entrada

```mermaid
sequenceDiagram
    actor B as Encargado de bodega
    participant V as Vista de entrada
    participant S as ServicioInventario
    participant DB as PostgreSQL

    B->>V: Insumo, cantidad, lote y vencimiento
    V->>S: registrar_entrada(datos)
    S->>S: validar insumo activo y lote obligatorio
    S->>DB: BEGIN
    S->>DB: obtener o crear existencia (bodega, lote)
    S->>DB: SELECT existencia FOR UPDATE
    S->>DB: INSERT movimiento ENTRADA
    S->>DB: UPDATE existencia.saldo
    S->>DB: INSERT evento de auditoría
    S->>DB: COMMIT
    S-->>V: movimiento registrado
    V-->>B: confirmación con saldo actualizado
```

## 6. Secuencia: registrar salida con FEFO y control de concurrencia

```mermaid
sequenceDiagram
    actor B as Encargado de bodega
    participant V as Vista de salida
    participant S as ServicioInventario
    participant DB as PostgreSQL

    B->>V: Insumo, cantidad, servicio y autorizante
    V->>S: registrar_salida(datos)
    S->>S: validar permisos, cantidad positiva y autorizante
    S->>DB: BEGIN
    S->>DB: SELECT lotes elegibles ORDER BY vencimiento
    S->>DB: SELECT existencias FOR UPDATE (orden por id)
    alt saldo suficiente y lotes vigentes
        S->>DB: INSERT movimiento SALIDA
        S->>DB: UPDATE existencias descontadas
        S->>DB: INSERT evento de auditoría
        S->>DB: COMMIT
        S-->>V: movimiento registrado
        V-->>B: confirmación con saldo restante
    else saldo insuficiente o lote vencido
        S->>DB: ROLLBACK
        S-->>V: rechazo con motivo
        V-->>B: mensaje de error
    end
```

La comprobación de saldo ocurre **después** de bloquear las filas. Verificar antes de bloquear deja una ventana en la que dos usuarios pueden aprobar la misma unidad disponible.

## 7. Secuencia: anular movimiento

```mermaid
sequenceDiagram
    actor B as Encargado de bodega
    participant V as Vista de anulación
    participant S as ServicioInventario
    participant DB as PostgreSQL

    B->>V: Movimiento y motivo
    V->>S: anular_movimiento(id, motivo)
    S->>DB: BEGIN
    S->>DB: SELECT movimiento FOR UPDATE
    alt ya anulado
        S-->>V: rechazo por anulación previa
    else entrada con lotes consumidos
        S-->>V: rechazo y sugerencia de ajuste por conteo
    else anulación válida
        S->>DB: marcar original como ANULADO
        S->>DB: INSERT movimiento REVERSION vinculado
        S->>DB: UPDATE existencia.saldo
        S->>DB: INSERT evento de auditoría
        S->>DB: COMMIT
        S-->>V: anulación registrada
    end
```

## 8. Trazabilidad caso de uso → requisito

| Caso de uso | Reglas aplicadas | Criterio de aceptación asociado |
|---|---|---|
| CU-02 | RN-01, RN-02, RN-05 | Rechazo de salida sobre el stock y registro de autorizante |
| CU-03 | RN-06, RN-09, RN-13 | Reversión conservando el original y bloqueo de anulación inválida |
| CU-04 | RN-11 | Ajuste con motivo y rol autorizado |
| CU-06 | RN-03, D-05 | Alerta considera solo lotes no vencidos |
| CU-09 | RF-14 | El jefe de servicio no accede a otras unidades |

## 9. Pendiente

- Diagrama de despliegue: depende de la decisión de alojamiento, aún abierta.
- Diagrama de componentes: se deriva de la arquitectura y no aporta información adicional a la vista general ya documentada.
- Validación de los nombres de casos de uso con el docente antes del cierre del diseño.
