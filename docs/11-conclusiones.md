# Conclusiones

## 1. Cumplimiento del objetivo general

El objetivo general planteado fue formular y diseñar un sistema de gestión de inventario de insumos médicos no medicamentosos que permitiera registrar los movimientos de bodega, conocer las existencias disponibles y detectar oportunamente quiebres de stock y vencimientos. El trabajo entregado cumple ese objetivo en el plano documental: el sistema se encuentra formulado y diseñado, pero no construido ni operado.

El diseño resultante comprende quince requisitos funcionales, catorce reglas de negocio y diez requisitos no funcionales, un modelo de datos de nueve entidades, trece casos de uso, seis diagramas y una matriz de veinticuatro casos de prueba. Cada requisito obligatorio está asociado a un objetivo específico y a una regla verificable. Esa trazabilidad es, en sí misma, un resultado del trabajo: permite sostener que el sistema propuesto responde a un problema formulado y no a una lista de funcionalidades elegidas por preferencia.

## 2. Aportes del trabajo desarrollado

El primer aporte es haber separado, de manera explícita y sostenida, lo que se sabe de lo que se supone. Los requisitos provienen de un caso simulado; los procesos descritos, los volúmenes y las metas de los indicadores son propuestas. El informe declara esa condición en cada sección y define cinco supuestos con su método de validación, además de un procedimiento para registrar los cambios que surjan de las entrevistas. Un diseño que se presenta como conocimiento comprobado cuando no lo es se vuelve indefendible apenas se pregunta por su origen; este trabajo eligió la posición opuesta y quedó preparado para el cuestionamiento.

El segundo aporte está en las reglas que protegen la integridad del inventario. La decisión de no eliminar movimientos, sino anularlos mediante una reversión vinculada al registro original, convierte cada variación de existencias en un hecho explicable. La regla de cálculo correspondiente —sumar el efecto de todos los movimientos, sin filtrar por estado— evita el error clásico de restar dos veces la anulación. Junto con la restricción que impide saldos negativos en la base de datos, estas definiciones no son detalles de implementación: son la diferencia entre un sistema que registra y un sistema que permite auditar.

El tercer aporte es haber identificado el punto donde el diseño podía fallar en silencio. La verificación de existencia antes del bloqueo de filas deja una ventana en la que dos usuarios pueden autorizar el retiro de la misma unidad. El informe describe el flujo transaccional correcto y define un caso de prueba específico: con cinco unidades disponibles, dos salidas simultáneas de cuatro no pueden aprobarse ambas. Una prueba así no se escribe si el problema no se comprendió.

El cuarto aporte es metodológico. Las decisiones se registraron con la alternativa descartada y el motivo del descarte. Se documentó por qué no se modeló una entidad de solicitud, por qué no se adoptó stock en dos niveles y por qué los vencidos no cuentan como disponibilidad. Un lector puede discrepar de una decisión, pero no puede acusar de que fue arbitraria.

## 3. Decisiones de alcance y su justificación

El recorte de alcance fue la decisión de mayor impacto. Excluir medicamentos no responde a una simplificación cómoda, sino a que ese dominio incorpora requisitos regulatorios y de trazabilidad que cambian la naturaleza del sistema; incorporarlos habría exigido un proyecto distinto. Excluir los datos de pacientes redujo el riesgo legal y acotó el modelo de datos, sin afectar el problema central del control de insumos.

La elección de una sola ubicación de existencias, en lugar de un esquema de bodega y servicios con saldo propio, se sostuvo en el plazo disponible. El doble nivel obliga a modelar transferencias internas, conciliación entre ubicaciones y permisos adicionales: multiplica el trabajo sin agregar evidencia sobre el problema que se busca resolver. Lo mismo ocurre con el flujo digital de solicitudes: la primera versión registra quién autoriza, que es el dato necesario para la trazabilidad, y posterga los estados de una solicitud completa.

La arquitectura siguió el mismo criterio. Un monolito modular con páginas renderizadas en el servidor evita mantener una interfaz separada y concentra la complejidad en el dominio, que es donde el sistema tiene algo que demostrar. Django aporta autenticación, permisos y administración de datos; PostgreSQL aporta el control transaccional que el inventario requiere. Ninguna de esas capacidades resuelve por sí sola los requisitos del proyecto: los permisos por servicio y la bitácora de operaciones se diseñaron como desarrollo propio, y el informe lo declara.

## 4. Limitaciones del trabajo

La limitación principal es la ausencia de validación con usuarios reales. Todo el catálogo de requisitos deriva de un caso simulado construido por el equipo. Las entrevistas previstas pueden confirmar el problema, modificarlo o desmentirlo; hasta que ocurran, el diseño es una hipótesis documentada.

La segunda limitación es que las pruebas no se ejecutaron. La matriz de veinticuatro casos describe qué se probará, con qué datos y qué resultado se espera; no constituye evidencia de calidad del software, porque el software no existe todavía. Presentarla como resultado sería un error de lectura que el informe evita deliberadamente.

La tercera es que los indicadores carecen de línea base. Las metas de exactitud de inventario, pérdida por vencimiento y proporción de anulaciones fueron propuestas a partir del escenario simulado. Su calibración exige mediciones reales que aún no se han tomado. Del mismo modo, los objetivos de disponibilidad y recuperación son metas y no garantías: dependen de un alojamiento que todavía no se definió.

La cuarta limitación es de alcance temporal. El cronograma calculado deja dos horas de margen sobre ciento ocho disponibles. No es holgura: es el reconocimiento de que cualquier desvío obliga a recortar alcance antes que a extender fechas.

## 5. Próximos pasos

El paso inmediato es la validación con usuarios. Las entrevistas al encargado de bodega y a la jefatura administrativa permitirán contrastar los cinco supuestos declarados y ajustar la prioridad de los requisitos, manteniendo los identificadores para conservar la trazabilidad.

El paso siguiente es la implementación por incrementos, comenzando por el núcleo que sostiene la promesa del sistema: catálogo, entradas, salidas y existencias con control transaccional. Solo después de que ese núcleo resista la prueba de concurrencia tiene sentido agregar reportes y alertas, porque un reporte sobre datos inconsistentes agrega confianza sin fundamento.

La calibración de indicadores requiere al menos un ciclo mensual de operación con conteo físico. Hasta entonces, los valores propuestos deben tratarse como objetivos de diseño.

## 6. Reflexión final

El trabajo confirma una idea que la práctica suele desmentir: formular antes de programar no retrasa el proyecto, lo hace defendible. La mayor parte del esfuerzo se destinó a decidir qué no se iba a construir y a dejar registro de por qué. Esa renuncia explícita es lo que permite afirmar que el alcance es realizable con el equipo y el plazo disponibles, en lugar de prometer un sistema completo que nadie podría sostener.

Queda una pregunta abierta que excede este informe: si el problema descrito en el caso simulado se confirma en la operación real, la solución no será únicamente técnica. Un sistema de inventario cambia responsabilidades y exige disciplina de registro; sin esa disciplina, ninguna base de datos evita que el stock registrado se separe del stock físico. El diseño puede hacer visible la diferencia, pero no puede eliminarla por sí solo.
