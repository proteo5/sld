# Guía de Referencia Rápida de SLD

## Tres Formas de Representar Datos

### 1. Formato Tabla

**Mejor para:** Listas de elementos similares, datos tipo CSV, datos tabulares

**Estructura:**

- Primera fila = encabezados
- Filas subsecuentes = datos
- Campos separados por `|`
- Filas separadas por `~`

**Ejemplo:**

```sld
nombre|precio|enStock~Laptop|3999.90|^1~Mouse|149.90|^0~Headset|499.00|^1
```

**Equivalente JSON:**

```json
[
  {"nombre": "Laptop", "precio": 3999.90, "enStock": true},
  {"nombre": "Mouse", "precio": 149.90, "enStock": false},
  {"nombre": "Headset", "precio": 499.00, "enStock": true}
]
```

---

### 2. Formato Objeto

**Mejor para:** Objetos individuales, datos de configuración, pares clave-valor

**Estructura:**

- Propiedades: `propiedad[valor|`
- Última propiedad: `propiedad[valor~`
- Siempre termina con `~`

**Ejemplo:**

```sld
nombre[Juan|edad[30|ciudad[NYC|activo[^1~
```

**Equivalente JSON:**

```json
{
  "nombre": "Juan",
  "edad": 30,
  "ciudad": "NYC",
  "activo": true
}
```

---

### 3. Formato Array

**Mejor para:** Arrays nombrados, colecciones de objetos

**Estructura:**

- Inicio: `nombreArray{`
- Objetos separados por `~`
- Cada objeto sigue las reglas de formato objeto

**Ejemplo:**

```sld
usuarios{id[1|nombre[Juan|apellido[Perez~id[2|nombre[María|apellido[García
```

**Equivalente JSON:**

```json
{
  "usuarios": [
    {"id": 1, "nombre": "Juan", "apellido": "Perez"},
    {"id": 2, "nombre": "María", "apellido": "García"}
  ]
}
```

---

## Referencia de Delimitadores

| Carácter | Propósito | Ejemplo |
|----------|-----------|---------|
| `\|` | Separador de propiedades/campos | `nombre[Juan\|edad[30\|` |
| `~` | Separador de registros O última propiedad | `ciudad[NYC~` |
| `[` | Marcador de valor de propiedad | `nombre[Juan` |
| `{` | Marcador de inicio de array | `usuarios{` |
| `^` | Escape y prefijo booleano | `^1`, `^0`, `^\|` |

---

## Valores Booleanos

- `^1` = `true`
- `^0` = `false`

**Ejemplos:**

```sld
activo[^1|verificado[^0|premium[^1~
```

---

## Valores Nulos/Vacíos

Valor vacío entre delimitadores:

```sld
nombre[Juan|segundo[|apellido[Perez~
```

(segundo nombre es nulo/vacío)

---

## Secuencias de Escape

Para incluir caracteres delimitadores literales:

| Escape | Resultado | Ejemplo |
|--------|-----------|---------|
| `^\|` | Literal `\|` | `empresa[Pipe^\|Works Inc\|` |
| `^~` | Literal `~` | `modelo[XZ^~2000\|` |
| `^[` | Literal `[` | `etiqueta[Versión^[1.0^]\|` |
| `^{` | Literal `{` | `llave[Abrir^{Aquí\|` |
| `^^` | Literal `^` | `caret[Potencia^^2\|` |

---

## Ejemplos Completos

### Productos E-commerce (Tabla)

```sld
id|nombre|precio|stock|destacado~1|Laptop Pro|3999.90|15|^1~2|Mouse Inalámbrico|149.90|50|^0~3|Audífonos USB-C|499.00|30|^1
```

### Perfil de Usuario (Objeto)

```sld
userId[12345|nombreUsuario[juan_dev|email[juan@ejemplo.com|verificado[^1|rol[admin|ultimoAcceso[2025-11-16~
```

### Miembros del Equipo (Array)

```sld
equipo{nombre[Alicia|rol[Desarrollador|activo[^1|nivel[5~nombre[Roberto|rol[Diseñador|activo[^1|nivel[3~nombre[Carlos|rol[Gerente|activo[^0|nivel[7
```

### Datos Mixtos con Escape

```sld
empresa[Tech^|Solutions Inc|email[contacto@tech.com|lema[Innovación^~Excelencia|fundada[2020|activo[^1~
```

---

## Elegir el Formato Correcto

| Tipo de Datos | Usar Formato | Por qué |
|---------------|--------------|---------|
| Listas tipo CSV | **Tabla** | Encabezados compactos, estructura clara |
| Configuración | **Objeto** | Propiedades auto-documentadas |
| Colecciones nombradas | **Array** | Nombre de array explícito + objetos |
| Tipos mixtos | **Objeto/Array** | Flexibilidad para datos anidados |

---

## Comparación de Eficiencia de Tokens

**JSON Original (125 tokens):**

```json
{
  "productos": [
    {"id": 1, "nombre": "Laptop", "precio": 3999.90},
    {"id": 2, "nombre": "Mouse", "precio": 149.90}
  ]
}
```

**SLD Formato Array (~35 tokens):**

```sld
productos{id[1|nombre[Laptop|precio[3999.90~id[2|nombre[Mouse|precio[149.90
```

**SLD Formato Tabla (~28 tokens):**

```sld
id|nombre|precio~1|Laptop|3999.90~2|Mouse|149.90
```

**Resultado:** ¡72-78% de reducción de tokens! 🎉

---

## Patrones Comunes

### Array Vacío

```sld
items{
```

### Array de Un Elemento

```sld
usuarios{id[1|nombre[Juan|activo[^1~
```

### Propiedades Anidadas (Aplanadas)

```sld
usuario_nombre[Juan|usuario_direccion_calle[Calle Principal|usuario_direccion_ciudad[NYC|usuario_direccion_zip[10001~
```

### Múltiples Flags Booleanos

```sld
permisos_lectura[^1|permisos_escritura[^1|permisos_eliminar[^0|permisos_admin[^0~
```

---

**Recuerda:** ¡Elige Tabla para uniformidad, Objeto para claridad, Array para colecciones nombradas!
