# Guía de Sintaxis de SLD

Esta guía proporciona ejemplos detallados y explicaciones de todos los aspectos de la sintaxis de SLD.

---

## Anatomía Visual del Formato

### Formato Tabla Desglosado
```
┌─ Encabezados (separados por |)
│
nombre|edad|ciudad~Juan|30|NYC~María|25|LA
      │    │     │    │  │  │      │  │ └─ Valor
      │    │     │    │  │  │      │  └─ Campo
      │    │     │    │  │  │      └─ Separador
      │    │     │    │  │  └─ Valor
      │    │     │    │  └─ Campo
      │    │     │    └─ Separador de fila (nueva fila de datos)
      │    │     └─ Valor de encabezado
      │    └─ Separador de campo
      └─ Valor de encabezado
```

### Formato Objeto Desglosado
```
┌─ Propiedad
│   ┌─ Inicio de valor
│   │ ┌─ Valor
│   │ │    ┌─ Separador de propiedad
│   │ │    │ ┌─ Propiedad
│   │ │    │ │    ┌─ Valor
│   │ │    │ │    │   ┌─ Terminador (última propiedad)
│   │ │    │ │    │   │
nombre[Juan|edad[30|activo[^1~
```

### Formato Array Desglosado
```
┌─ Nombre del array
│       ┌─ Marcador de inicio de array
│       │ ┌─ Primer objeto
│       │ │              ┌─ Separador de objeto
│       │ │              │ ┌─ Segundo objeto
│       │ │              │ │
usuarios{id[1|nombre[Ana~id[2|nombre[Bob
                          └─ Último objeto (sin ~ al final)
```

---

## Detalles de la Sintaxis

### 1. Nombres de Propiedades
```
nombre[Juan|edad[30|estaActivo[^1~
│      │    │    │  │          └─ Las propiedades booleanas funcionan como cualquier otra
│      │    │    │  └─ camelCase típico
│      │    │    └─ Nombres numéricos permitidos
│      │    └─ Nombres de una sola palabra típicos
│      └─ Siempre seguido por [
```

**Nombres de propiedades válidos:**
- `nombre`, `edad`, `ciudad` (palabras simples)
- `primerNombre`, `segundoNombre` (camelCase)
- `usuario_id`, `producto_precio` (guion bajo)
- `dato1`, `campo2` (con números)

**Nombres de propiedades inválidos:**
- `primer-nombre` (guiones no permitidos)
- `nombre de usuario` (espacios no permitidos)
- `precio$` (caracteres especiales no permitidos)

### 2. Tipos de Valores

#### Cadenas
```
nombre[Juan Pérez|ciudad[Nueva York~
```
- Sin comillas
- Espacios permitidos
- Acentos y UTF-8 soportados

#### Números
```
edad[30|precio[99.99|cantidad[-5|porcentaje[0.75~
```
- Enteros: `30`, `-5`, `0`
- Decimales: `99.99`, `0.75`, `-10.5`
- Sin separadores de miles: `1000000` (no `1,000,000`)

#### Booleanos
```
activo[^1|verificado[^0|premium[^1~
```
- `^1` = verdadero
- `^0` = falso
- ¡No `true`/`false`!

#### Valores Nulos/Vacíos
```
nombre[Juan|segundo[|apellido[Pérez~
              │
              └─ Valor vacío (nulo)
```

---

## Ejemplos del Mundo Real

### 1. Sistema E-Commerce

#### Catálogo de Productos (Tabla)
```
sku|nombre|precio|moneda|enStock|destacado~LAP001|Laptop Pro 15|3999.90|USD|^1|^1~MSE002|Mouse Ergonómico|149.90|USD|^1|^0~KBD003|Teclado RGB|299.00|USD|^0|^1
```

#### Detalles de Producto Individual (Objeto)
```
sku[LAP001|nombre[Laptop Pro 15|marca[TechBrand|precio[3999.90|moneda[USD|enStock[^1|cantidad[25|destacado[^1|categoria[Electrónicos|subcategoria[Computadoras|calificacion[4.7|reseñas[328~
```

#### Carrito de Compras (Array)
```
carrito{productoId[LAP001|cantidad[1|precio[3999.90~productoId[MSE002|cantidad[2|precio[149.90~productoId[KBD003|cantidad[1|precio[299.00
```

### 2. Sistema de Gestión de Usuarios

#### Lista de Usuarios (Tabla)
```
id|nombreUsuario|email|rol|verificado|activo|ultimoAcceso~1001|juan_dev|juan@ejemplo.com|admin|^1|^1|2025-11-16~1002|maria_design|maria@ejemplo.com|user|^1|^1|2025-11-15~1003|carlos_qa|carlos@ejemplo.com|user|^0|^0|2025-11-10
```

#### Perfil de Usuario Completo (Objeto)
```
userId[1001|nombreUsuario[juan_dev|email[juan@ejemplo.com|verificado[^1|rol[admin|activo[^1|fechaCreacion[2024-01-15|ultimoAcceso[2025-11-16|intentosInicioSesion[0|cuentaBloqueada[^0|perfil_nombre[Juan García|perfil_bio[Desarrollador Full Stack|perfil_ubicacion[Madrid|configuraciones_tema[oscuro|configuraciones_idioma[es|configuraciones_notificaciones[^1~
```

#### Sesiones de Usuario (Array)
```
sesiones{sesionId[s1001a|userId[1001|ipAddress[192.168.1.1|userAgent[Mozilla/5.0|inicioSesion[2025-11-16T08:00:00Z|expira[2025-11-17T08:00:00Z~sesionId[s1002b|userId[1002|ipAddress[192.168.1.2|userAgent[Chrome/120.0|inicioSesion[2025-11-16T09:30:00Z|expira[2025-11-17T09:30:00Z
```

### 3. Sistema de Gestión de Tareas

#### Lista de Tareas (Tabla)
```
id|titulo|prioridad|estado|asignado|vencimiento~T001|Corregir error inicio sesión|alta|en-progreso|juan_dev|2025-11-20~T002|Actualizar documentación|media|pendiente|maria_design|2025-11-25~T003|Revisar solicitudes|baja|completado|carlos_qa|2025-11-18
```

#### Tarea Detallada con Comentarios (Array)
```
comentarios{comentarioId[C001|autorId[1002|autorNombre[María|texto[He revisado el código|timestamp[2025-11-16T10:00:00Z~comentarioId[C002|autorId[1001|autorNombre[Juan|texto[Gracias^| procederé con los cambios|timestamp[2025-11-16T10:15:00Z
```

---

## Caracteres de Escape en Acción

### Ejemplo 1: Contenido con Delimitadores
```
empresa[Datos^|Análisis Corp|lema[Innovación^~Excelencia|direccion[123 Main St^, Suite^[5^]|telefono[^(555^) 123-4567~
```

**Decodifica a:**
- empresa: `Datos|Análisis Corp`
- lema: `Innovación~Excelencia`
- direccion: `123 Main St, Suite[5]`
- telefono: `(555) 123-4567`

### Ejemplo 2: Fórmulas Matemáticas
```
formula[x^^2 + y^^2 = r^^2|operador[a ^| b significa a OR b|notacion[f^(x^) = x^^3~
```

**Decodifica a:**
- formula: `x^2 + y^2 = r^2`
- operador: `a | b significa a OR b`
- notacion: `f(x) = x^3`

### Ejemplo 3: Configuración JSON con Formato
```
config[^{^"theme^": ^"dark^"^, ^"lang^": ^"es^"^}|tipo[json|activo[^1~
```

**Decodifica a:**
- config: `{"theme": "dark", "lang": "es"}`
- tipo: `json`
- activo: `true`

---

## Patrones Comunes y Mejores Prácticas

### Estructura de Datos Anidados

**❌ Incorrecto (anidación real no soportada):**
```
usuario[nombre[Juan|edad[30~
```

**✅ Correcto (Opción 1: Aplanamiento con guiones bajos):**
```
usuario_nombre[Juan|usuario_edad[30~
```

**✅ Correcto (Opción 2: Array anidado):**
```
usuarios{nombre[Juan|edad[30
```

### Múltiples Flags Booleanos
```
permisos_lectura[^1|permisos_escritura[^1|permisos_eliminar[^0|permisos_admin[^0|permisos_exportar[^1~
```

### Marcas de Tiempo y Fechas
```
fechaCreacion[2025-11-16|timestamp[2025-11-16T14:30:00Z|fechaVencimiento[2025-12-31~
```

### Arrays de Valores Primitivos
```
tags{valor[javascript~valor[nodejs~valor[api~valor[backend
```

### Valores Opcionales/Nulos
```
nombre[Juan|segundo[|apellido[García|sufijo[|titulo[Dr~
```

---

## Lista de Validación

Al crear SLD, verifica:

- [ ] **Formato Tabla:** Primera fila contiene encabezados
- [ ] **Formato Tabla:** Todas las filas tienen el mismo número de campos
- [ ] **Formato Objeto:** Última propiedad termina con `~`
- [ ] **Formato Objeto:** Todas las demás propiedades terminan con `|`
- [ ] **Formato Array:** Comienza con `nombreArray{`
- [ ] **Formato Array:** Objetos separados por `~`
- [ ] **Formato Array:** Último objeto NO tiene `~` al final
- [ ] **Booleanos:** Usar `^1` y `^0` (no `true`/`false`)
- [ ] **Caracteres Especiales:** Escapados correctamente (`^|`, `^~`, `^[`, `^{`, `^^`)
- [ ] **Nombres de Propiedades:** No contienen espacios ni guiones
- [ ] **Valores:** Sin comillas a menos que sean parte del contenido
- [ ] **Codificación:** Archivo guardado como UTF-8

---

## Consejos de Depuración

### Síntoma: Parse falla al final del objeto
**Causa:** Falta `~` al final de la última propiedad del objeto
```
❌ nombre[Juan|edad[30|
✅ nombre[Juan|edad[30~
```

### Síntoma: Parse falla entre objetos del array
**Causa:** Falta `~` entre objetos en el array
```
❌ usuarios{id[1|nombre[Anaid[2|nombre[Bob
✅ usuarios{id[1|nombre[Ana~id[2|nombre[Bob
```

### Síntoma: Valores contienen caracteres inesperados
**Causa:** Delimitadores no escapados
```
❌ empresa[Datos|Soluciones Corp|
✅ empresa[Datos^|Soluciones Corp|
```

### Síntoma: Valor booleano interpretado como cadena
**Causa:** Usar `true`/`false` en lugar de `^1`/`^0`
```
❌ activo[true|
✅ activo[^1|
```

---

## Referencia Rápida de Sintaxis

```
Tabla:      encabezado1|encabezado2~valor1|valor2~valor3|valor4
Objeto:     prop1[val1|prop2[val2|prop3[val3~
Array:      arrayNombre{obj1~obj2~obj3
Booleano:   ^1 (true), ^0 (false)
Escape:     ^| ^~ ^[ ^{ ^^
```

---

Para más detalles técnicos, consulta [SPECIFICATION.md](SPECIFICATION.md).
