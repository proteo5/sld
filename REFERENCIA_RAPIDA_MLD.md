# Referencia Rápida MLD v1.1

**Multi Line Data - Referencia rápida para desarrolladores**

---

## Delimitadores (v1.1)

| Símbolo | Propósito | Ejemplo |
|---------|-----------|---------|
| `;` | Separador de campos | `nombre[Alicia;edad[30` |
| `\n` | Separador de registros (salto de línea) | Un registro por línea |
| `[` | Marcador de propiedad | `nombre[valor` |
| `{` | Marcador de array (inicio) | `etiquetas{rojo~azul}` |
| `}` | Fin de array | `etiquetas{rojo~azul}` |
| `^` | Carácter de escape | `texto[Hola^; Mundo` |

**Diferencia clave con SLD:** MLD usa saltos de línea reales (`\n`) en lugar de tilde (`~`) para separar registros.

---

## Secuencias de Escape

| Secuencia | Resultado |
|-----------|-----------|
| `^;` | `;` literal |
| `^[` | `[` literal |
| `^{` | `{` literal |
| `^}` | `}` literal |
| `^^` | `^` literal |

Nota: Para representar un salto de línea dentro de un valor, usa la secuencia literal `\n` (dos caracteres), no `^\n`.

**Ejemplo:**
```
desc[Precio: $100^; incluye impuestos
```

---

## Tipos de Datos

### Cadena
```
nombre[Alicia
ciudad[Nueva York
```

### Número
```
edad[30
precio[99.99
cientifico[6.022e23
```

### Booleano
```
activo[^1        # verdadero
verificado[^0    # falso
```

### Nulo
```
segundoNombre[;edad[30    # segundoNombre es nulo
```

### Array
```
etiquetas{rojo~verde~azul}
puntuaciones{85~92~78}
```

---

## Ejemplos Básicos

### Objeto Simple (Una Línea)
```
nombre[Alicia;edad[30;ciudad[NYC
```

### Múltiples Registros (Múltiples Líneas)
```
id[1;nombre[Alicia
id[2;nombre[Roberto
id[3;nombre[Carlos
```

### Objeto con Array
```
usuario[alicia;etiquetas{admin~usuario};puntuacion[95
```

### Contenido con Escape
```
nota[Usa punto y coma^; no comas;fecha[2024-01-15
```

---

## Patrones Comunes

### Registro de Usuario
```
id[42;usuario[alicia;email[alicia@ejemplo.com;verificado[^1;rol[admin
```

### Catálogo de Productos
```
sku[LAP001;nombre[Laptop;precio[999.99;stock[^1;etiquetas{electronica~computadoras}
```

### Entrada de Log
```
timestamp[2024-12-01T10:30:00Z;nivel[INFO;servicio[api;mensaje[Petición procesada;usuario[alicia
```

### Configuración
```
host[localhost;puerto[8080;ssl[^1;timeout[30;reintentos[3
```

---

## Uso de Herramientas Unix

### Filtrar con grep
```bash
# Encontrar todos los logs de ERROR
grep "nivel\[ERROR" app.mld

# Encontrar actividad de usuario específico
grep "usuario\[alicia" actividad.mld

# Búsqueda insensible a mayúsculas
grep -i "estado\[activo" usuarios.mld
```

### Contar con wc
```bash
# Contar registros totales
wc -l datos.mld

# Contar errores
grep "nivel\[ERROR" logs.mld | wc -l
```

### Head/Tail
```bash
# Primeros 10 registros
head -10 datos.mld

# Últimos 20 registros
tail -20 datos.mld

# Monitoreo de logs en tiempo real
tail -f logs.mld
```

### Extraer con awk
```bash
# Extraer campo nombre de cada registro
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^nombre\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}' usuarios.mld
```

### Procesar con sed
```bash
# Reemplazar valores de estado
sed 's/estado\[pendiente/estado[activo/g' tareas.mld

# Eliminar registros
sed '/eliminado\[^1/d' usuarios.mld
```

---

## Guía de Codificación

**Python:**
```python
def escapar(s):
  return (
    s.replace("^", "^^")
     .replace(";", "^;")
     .replace("[", "^[")
     .replace("{", "^{")
     .replace("}", "^}")
     .replace("\n", "\\n")  # representar saltos de línea como dos caracteres
  )

def codificar_registro(obj):
    partes = [f"{escapar(k)}[{escapar(str(v))}" for k, v in obj.items()]
    return ";".join(partes)

# Escribir múltiples registros
with open('datos.mld', 'w') as f:
    for registro in registros:
        f.write(codificar_registro(registro) + '\n')
```

**JavaScript:**
```javascript
const escapar = s => s
  .replace(/\^/g, '^^')
  .replace(/;/g, '^;')
  .replace(/\[/g, '^[')
  .replace(/\{/g, '^{')
  .replace(/\}/g, '^}')
  .replace(/\n/g, '\\n'); // representar saltos de línea como dos caracteres

const codificarRegistro = obj => {
  const pares = Object.entries(obj).map(([k, v]) => `${escapar(k)}[${escapar(String(v))}`);
  return pares.join(';');
};

// Escribir a archivo
const lineas = registros.map(r => codificarRegistro(r)).join('\n');
fs.writeFileSync('datos.mld', lineas);
```

---

## Guía de Decodificación

**Python:**
```python
def desescape(s):
    resultado = []
    i = 0
    while i < len(s):
        if s[i] == '^' and i + 1 < len(s):
            resultado.append(s[i + 1])
            i += 2
        else:
            resultado.append(s[i])
            i += 1
    return ''.join(resultado)

def decodificar_registro(linea):
    obj = {}
    for prop in linea.split(';'):
        if '[' in prop:
            clave, valor = prop.split('[', 1)
            obj[desescape(clave)] = desescape(valor)
    return obj

# Leer archivo línea por línea
registros = []
with open('datos.mld', 'r') as f:
    for linea in f:
        registros.append(decodificar_registro(linea.rstrip('\n')))
```

---

## Conversión (MLD ↔ SLD)

**MLD a SLD:**
```bash
tr '\n' '~' < datos.mld > datos.sld
```

**SLD a MLD:**
```bash
tr '~' '\n' < datos.sld > datos.mld
```

**Conversión en Python:**
```python
# MLD a SLD
with open('datos.mld', 'r') as f:
    sld = f.read().replace('\n', '~')
    
# SLD a MLD
with open('datos.sld', 'r') as f:
    mld = f.read().replace('~', '\n')
```

---

## Errores Comunes

### ❌ Incorrecto: Incrustar saltos de línea sin escapar

```
descripcion[Primera línea
Segunda línea
```

### ✅ Correcto: Usar secuencia literal \\n o mantener en una línea

```
descripcion[Primera línea\\nSegunda línea
```

---

### ❌ Incorrecto: Usar separador tilde

```
nombre[Alicia;edad[30~
```

### ✅ Correcto: Usar salto de línea (un registro por línea)

```
nombre[Alicia;edad[30
```

---

### ❌ Incorrecto: No escapar punto y coma

```
nota[Costo: $50; incluye impuestos
```

### ✅ Correcto: Escapar punto y coma

```
nota[Costo: $50^; incluye impuestos
```

---

## MLD vs SLD - Cuándo Usar

### Usa MLD para:

✅ **Archivos de log** - Monitoreo en tiempo real con `tail -f`  
✅ **Datos en streaming** - Procesar registros incrementalmente  
✅ **Filtrado con grep** - Búsqueda rápida de texto sin parsing  
✅ **Herramientas basadas en líneas** - sed, awk, head, tail, wc  
✅ **Depuración humana** - Un registro por línea, fácil de leer  
✅ **Datasets grandes** - Procesar con memoria constante

### Usa SLD para:

✅ **Transmisión de red** - Datos en un solo paquete  
✅ **Configuraciones embebidas** - Cadenas de una línea en código  
✅ **Memoria limitada** - Huella ligeramente más pequeña  
✅ **Transferencia en bloque** - Menos delimitadores (overhead mínimo)

---

## Ejemplo de Streaming

**Procesar archivo MLD grande con memoria constante:**

```python
def procesar_mld_stream(archivo, callback):
    """Procesar archivo MLD línea por línea."""
    with open(archivo, 'r') as f:
        for linea in f:
            registro = decodificar_registro(linea.rstrip('\n'))
            callback(registro)

# Uso
def manejar_registro(registro):
    if registro.get('nivel') == 'ERROR':
        print(f"Error: {registro.get('mensaje')}")

procesar_mld_stream('logs.mld', manejar_registro)
```

---

## Monitoreo de Logs en Tiempo Real

```bash
# Monitorear logs en tiempo real
tail -f app.mld | grep "nivel\[ERROR"

# Contar errores por minuto
tail -f app.mld | grep "nivel\[ERROR" | while read linea; do
  echo "$(date): ERROR detectado"
done

# Extraer y procesar
tail -f app.mld | awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^mensaje\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}'
```

---

## Consejos de Rendimiento

1. **Streaming:** Procesar línea por línea para archivos grandes
2. **Memoria:** MLD usa memoria constante con streaming
3. **Grep:** Más rápido que parsear para filtros simples
4. **Indexación:** Construir índice de offsets de línea para acceso aleatorio
5. **Paralelo:** Procesar bloques en paralelo con `split`

**Dividir archivo para procesamiento paralelo:**
```bash
# Dividir en 4 bloques
split -n 4 datos.mld bloque_

# Procesar en paralelo
for bloque in bloque_*; do
  procesar_bloque.sh "$bloque" &
done
wait
```

---

## Solución Rápida de Problemas

**Problema:** Grep no encuentra registros  
**Solución:** Verificar punto y coma escapados en patrón de búsqueda

**Problema:** Líneas en blanco extra en salida  
**Solución:** Usar `grep -v '^$'` para filtrar líneas vacías

**Problema:** Registros divididos en múltiples líneas  
**Solución:** Asegurar que no hay saltos de línea literales en valores de propiedades

**Problema:** Rendimiento lento en archivos grandes  
**Solución:** Usar procesamiento streaming/línea por línea, no cargar archivo completo

---

## Documentos Relacionados

- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Especificación técnica completa
- [GUIA_SINTAXIS_MLD.md](GUIA_SINTAXIS_MLD.md) - Ejemplos detallados de sintaxis
- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Variante de línea única
- [MIGRACION.md](MIGRACION.md) - Guía de migración v1.0 a v1.1

---

**Versión:** 1.1  
**Formato:** MLD (Multi Line Data)  
**Última Actualización:** Diciembre 2024
