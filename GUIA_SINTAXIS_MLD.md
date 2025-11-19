# Guía de Sintaxis MLD v2.0

**Ejemplos completos y patrones para Multi Line Data**

---

## Tabla de Contenidos

1. [Sintaxis Básica](#sintaxis-básica)
2. [Tipos de Datos en Detalle](#tipos-de-datos-en-detalle)
3. [Secuencias de Escape](#secuencias-de-escape)
4. [Arrays](#arrays)
5. [Integración con Herramientas Unix](#integración-con-herramientas-unix)
6. [Ejemplos del Mundo Real](#ejemplos-del-mundo-real)
7. [Patrones de Streaming](#patrones-de-streaming)
8. [Anti-Patrones](#anti-patrones)
9. [Mejores Prácticas](#mejores-prácticas)

---

## Sintaxis Básica

### Registro Único (Una Línea)
```
nombre[Alicia;edad[30;ciudad[NYC
```
**Resultado:** `{"nombre": "Alicia", "edad": 30, "ciudad": "NYC"}`

### Múltiples Registros (Múltiples Líneas)
```
id[1;nombre[Alicia
id[2;nombre[Roberto
id[3;nombre[Carlos
```
**Resultado:**
```json
[
  {"id": 1, "nombre": "Alicia"},
  {"id": 2, "nombre": "Roberto"},
  {"id": 3, "nombre": "Carlos"}
]
```

### Archivo Vacío
```
(sin contenido)
```
**Resultado:** `[]` (colección vacía)

### Registro de Propiedad Única
```
estado[ok
```
**Resultado:** `{"estado": "ok"}`

---

## Tipos de Datos en Detalle

### Cadenas

**Cadena simple:**
```
saludo[Hola Mundo
```

**Cadena vacía:**
```
valor[;otro[dato
```

**Cadena con espacios:**
```
direccion[Calle Principal 123, Apto 4B
```

**Texto multi-línea (escapado):**
```
descripcion[Línea 1^\nLínea 2^\nLínea 3
```
Nota: Los saltos de línea literales deben escaparse dentro de valores de propiedades

### Números

**Enteros:**
```
cantidad[42
edad[30
año[2024
```

**Decimales:**
```
precio[99.99
temperatura[23.5
```

**Negativos:**
```
balance[-150.50
offset[-10
```

**Notación científica:**
```
avogadro[6.022e23
planck[6.626e-34
```

### Booleanos

**Verdadero:**
```
activo[^1
habilitado[^1
verificado[^1
```

**Falso:**
```
eliminado[^0
publico[^0
archivado[^0
```

**Múltiples booleanos:**
```
id[100;activo[^1;verificado[^0;premium[^1
```

### Valores Nulos

**Un solo nulo:**
```
segundoNombre[;apellido[García
```

**Múltiples nulos:**
```
nombre[Alicia;telefono[;email[;direccion[Calle Principal 123
```

### Arrays

**Array de cadenas:**
```
etiquetas{rojo~verde~azul}
```

**Array de números:**
```
puntuaciones{85~92~78~95}
```

**Mezclado (como cadenas):**
```
datos{Alicia~30~NYC}
```

**Array vacío:**
```
items{}
```

---

## Secuencias de Escape

### Escapar Punto y Coma

**Simple:**
```
nota[Primer item^; segundo item^; tercer item
```

**En descripción:**
```
instrucciones[Mezclar ingredientes^; hornear a 180°C^; enfriar 10 minutos
```

### Escapar Saltos de Línea

**Contenido multi-línea:**
```
mensaje[Hola\\nEsta es la línea 2\\nY la línea 3
```

**Poema:**
```
poema[Las rosas son rojas\\nLas violetas azules\\nLos datos compactos\\nY eficientes también
```

### Escapar Corchetes

**Fragmento de código:**
```
codigo[array^[0^] = valor
```

**Expresión:**
```
formula[x^[2^] + y^[3^] = z
```

### Escapar Llaves

**Texto tipo JSON:**
```
ejemplo[Usa ^{clave: valor^} para objetos
```

### Escapar Circunflejos

**Notación de exponente:**
```
matematica[2^^3 significa 2 elevado a 3
```

**Múltiples escapes:**
```
texto[Usa ^^; ^^ es el carácter de escape
```

---

## Arrays

### Arrays Simples

```
colores{rojo~naranja~amarillo~verde~azul}
numeros{1~2~3~4~5~6~7~8~9~10}
```

### Arrays con Comas Escapadas

```
items{"Item 1, Parte A"~Item 2~"Item 3, Parte B"}
```

### Múltiples Arrays en Registro

```
id[1;etiquetas{web~movil~api};puntuaciones{95~87~92};estado[activo
```

### Arrays Largos

```
palabras_clave{javascript~python~java~cpp~csharp~go~rust~ruby~php~swift~kotlin~typescript}
```

---

## Integración con Herramientas Unix

### Ejemplos con Grep

**Encontrar registros por valor de campo:**
```bash
# Todos los usuarios activos
grep "estado\[activo" usuarios.mld

# Usuario específico
grep "nombreusuario\[alicia" usuarios.mld

# Logs de error
grep "nivel\[ERROR" app.mld

# Múltiples patrones
grep -E "nivel\[(ERROR|WARN)" app.mld
```

**Contar coincidencias:**
```bash
# Contar errores
grep -c "nivel\[ERROR" app.mld

# Contar usuarios activos
grep -c "activo\[^1" usuarios.mld
```

**Invertir coincidencia:**
```bash
# Todos los registros no eliminados
grep -v "eliminado\[^1" datos.mld
```

### Ejemplos con Awk

**Extraer campo específico:**
```bash
# Extraer todos los nombres de usuario
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^nombreusuario\[/) {
      split($i, arr, "[")
      print arr[2]
    }
  }
}' usuarios.mld
```

**Calcular estadísticas:**
```bash
# Edad promedio
awk -F';' '
{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^edad\[/) {
      split($i, arr, "[")
      sum += arr[2]
      count++
    }
  }
}
END {
  if (count > 0) print "Edad promedio:", sum/count
}' usuarios.mld
```

**Filtrar y transformar:**
```bash
# Extraer nombre y email
awk -F';' '{
  nombre = ""; email = ""
  for (i=1; i<=NF; i++) {
    if ($i ~ /^nombre\[/) { split($i, a, "["); nombre = a[2] }
    if ($i ~ /^email\[/) { split($i, a, "["); email = a[2] }
  }
  if (nombre && email) print nombre, email
}' usuarios.mld
```

### Ejemplos con Sed

**Reemplazar valores:**
```bash
# Actualizar estado
sed 's/estado\[pendiente/estado[completado/g' tareas.mld

# Actualizar precios
sed 's/precio\[99.99/precio[79.99/g' productos.mld
```

**Eliminar líneas:**
```bash
# Remover registros eliminados
sed '/eliminado\[^1/d' datos.mld

# Remover datos de prueba
sed '/^test/d' datos.mld
```

### Ejemplos con Head/Tail

**Primeros/últimos registros:**
```bash
# Primeros 10 registros
head -10 datos.mld

# Últimos 20 registros
tail -20 datos.mld

# Saltar primeros 100, mostrar siguientes 10
tail -n +101 datos.mld | head -10
```

**Monitoreo en tiempo real:**
```bash
# Seguir archivo de log
tail -f app.mld

# Seguir con filtro
tail -f app.mld | grep "nivel\[ERROR"

# Seguir múltiples archivos
tail -f app.mld acceso.mld
```

### Ejemplos con Sort

**Ordenar por campo extraído:**
```bash
# Ordenar por edad
awk -F';' '{
  edad = 0
  for (i=1; i<=NF; i++) {
    if ($i ~ /^edad\[/) { split($i, a, "["); edad = a[2] }
  }
  print edad "\t" $0
}' usuarios.mld | sort -n | cut -f2-
```

### Ejemplos con Uniq

**Contar duplicados:**
```bash
# Contar registros por estado
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^estado\[/) { split($i, a, "["); print a[2] }
  }
}' tareas.mld | sort | uniq -c
```

### Combinando Herramientas

**Pipeline complejo:**
```bash
# Encontrar usuarios activos premium, extraer emails, ordenar
grep "activo\[^1" usuarios.mld | \
  grep "premium\[^1" | \
  awk -F';' '{
    for (i=1; i<=NF; i++) {
      if ($i ~ /^email\[/) { split($i, a, "["); print a[2] }
    }
  }' | \
  sort | \
  uniq
```

---

## Ejemplos del Mundo Real

### Logs de Aplicación

```
timestamp[2024-12-01T08:00:00Z;nivel[INFO;servicio[auth;mensaje[Login de usuario;usuario[alicia;ip[192.168.1.10
timestamp[2024-12-01T08:01:15Z;nivel[WARN;servicio[database;mensaje[Consulta lenta;duracion[1.2s;query[SELECT * FROM usuarios
timestamp[2024-12-01T08:02:30Z;nivel[ERROR;servicio[pago;mensaje[Pago fallido;usuario[roberto;monto[99.99;error[E_TARJETA_RECHAZADA
timestamp[2024-12-01T08:03:45Z;nivel[INFO;servicio[auth;mensaje[Logout de usuario;usuario[alicia;duracion_sesion[225s
```

**Procesar con grep:**
```bash
# Todos los errores
grep "nivel\[ERROR" app.mld

# Errores de servicio específico
grep "nivel\[ERROR" app.mld | grep "servicio\[pago"

# Logs de hoy
grep "2024-12-01" app.mld
```

### Base de Datos de Usuarios

```
id[1;nombreusuario[alicia;email[alicia@ejemplo.com;verificado[^1;creado[2023-01-15;rol[admin;ultimo_login[2024-12-01
id[2;nombreusuario[roberto;email[roberto@ejemplo.com;verificado[^1;creado[2023-03-22;rol[usuario;ultimo_login[2024-11-30
id[3;nombreusuario[carlos;email[carlos@ejemplo.com;verificado[^0;creado[2024-01-10;rol[usuario;ultimo_login[
id[4;nombreusuario[diana;email[diana@ejemplo.com;verificado[^1;creado[2022-11-05;rol[moderador;ultimo_login[2024-12-01
```

**Consultas:**
```bash
# Usuarios verificados
grep "verificado\[^1" usuarios.mld

# Administradores
grep "rol\[admin" usuarios.mld

# Nunca han iniciado sesión
grep "ultimo_login\[;" usuarios.mld
```

### Catálogo de Productos

```
sku[LAP001;nombre[UltraBook Pro 15;precio[1299.99;stock[^1;cantidad[45;categoria[laptops;etiquetas{negocios,ultrabook,portatil
sku[MOU001;nombre[Mouse Inalámbrico;precio[29.99;stock[^1;cantidad[200;categoria[accesorios;etiquetas{inalambrico,ergonomico
sku[KEY001;nombre[Teclado Mecánico;precio[149.99;stock[^0;cantidad[0;categoria[accesorios;etiquetas{mecanico,rgb,gaming
sku[MON001;nombre[Monitor 4K 27 pulgadas;precio[499.99;stock[^1;cantidad[15;categoria[monitores;etiquetas{4k,ips,profesional
```

**Consultas:**
```bash
# Items en stock
grep "stock\[^1" productos.mld

# Fuera de stock
grep "stock\[^0" productos.mld

# Rango de precio (requiere awk)
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^precio\[/) {
      split($i, a, "[")
      if (a[2] >= 100 && a[2] <= 500) print $0
    }
  }
}' productos.mld
```

### Logs de Acceso

```
timestamp[2024-12-01T10:00:00Z;metodo[GET;ruta[/api/usuarios;estado[200;duracion[45ms;ip[192.168.1.100
timestamp[2024-12-01T10:00:05Z;metodo[POST;ruta[/api/login;estado[200;duracion[120ms;ip[192.168.1.101
timestamp[2024-12-01T10:00:10Z;metodo[GET;ruta[/api/productos;estado[404;duracion[15ms;ip[192.168.1.102
timestamp[2024-12-01T10:00:15Z;metodo[DELETE;ruta[/api/usuarios/5;estado[403;duracion[10ms;ip[192.168.1.103
```

**Análisis:**
```bash
# Errores 404
grep "estado\[404" acceso.mld

# Peticiones lentas
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^duracion\[/) {
      split($i, a, "[")
      if (a[2] ~ /[0-9]+ms/ && int(a[2]) > 100) print $0
    }
  }
}' acceso.mld

# Conteo de peticiones por método
awk -F';' '{
  for (i=1; i<=NF; i++) {
    if ($i ~ /^metodo\[/) { split($i, a, "["); print a[2] }
  }
}' acceso.mld | sort | uniq -c
```

---

## Patrones de Streaming

### Procesamiento Línea por Línea

**Python:**
```python
def procesar_archivo_mld(archivo):
    with open(archivo, 'r') as f:
        for num_linea, linea in enumerate(f, 1):
            try:
                registro = decodificar_registro(linea.rstrip('\n'))
                procesar_registro(registro)
            except Exception as e:
                print(f"Error en línea {num_linea}: {e}")
```

**Node.js:**
```javascript
const fs = require('fs');
const readline = require('readline');

async function procesarMLD(archivo) {
  const streamArchivo = fs.createReadStream(archivo);
  const rl = readline.createInterface({
    input: streamArchivo,
    crlfDelay: Infinity
  });

  for await (const linea of rl) {
    const registro = decodificarRegistro(linea);
    procesarRegistro(registro);
  }
}
```

### Filtrado Durante Streaming

**Python:**
```python
def filtrar_mld(archivo_entrada, archivo_salida, predicado):
    with open(archivo_entrada, 'r') as fin:
        with open(archivo_salida, 'w') as fout:
            for linea in fin:
                registro = decodificar_registro(linea.rstrip('\n'))
                if predicado(registro):
                    fout.write(linea)

# Uso
filtrar_mld('todos.mld', 'activos.mld', lambda r: r.get('activo') == '^1')
```

### Procesamiento por Bloques

**Python:**
```python
def procesar_bloques(archivo, tamano_bloque=1000):
    bloque = []
    with open(archivo, 'r') as f:
        for linea in f:
            bloque.append(decodificar_registro(linea.rstrip('\n')))
            if len(bloque) >= tamano_bloque:
                procesar_bloque(bloque)
                bloque = []
        if bloque:  # Procesar restantes
            procesar_bloque(bloque)
```

---

## Anti-Patrones

### ❌ No hacer: Incrustar saltos de línea literales

```
descripcion[Esta es la línea 1
Esta es la línea 2
```

**Por qué:** Crea múltiples registros en lugar de uno

**✅ Hacer:**
```
descripcion[Esta es la línea 1^\nEsta es la línea 2
```

---

### ❌ No hacer: Olvidar escapar punto y coma

```
nota[El precio es $50; impuestos incluidos
```

**Por qué:** El parser ve dos campos

**✅ Hacer:**
```
nota[El precio es $50^; impuestos incluidos
```

---

### ❌ No hacer: Cargar archivo completo para consultas simples

```python
# Malo: Cargar todo
with open('enorme.mld', 'r') as f:
    todos_datos = f.read()
    # Parsear y buscar...
```

**✅ Hacer: Streaming y filtrado:**
```python
# Bueno: Streaming línea por línea
with open('enorme.mld', 'r') as f:
    for linea in f:
        if 'estado[ERROR' in linea:
            print(linea)
```

---

### ❌ No hacer: Usar MLD para transmisión de un solo paquete

**Por qué:** SLD es más eficiente para envíos de red

**✅ Hacer: Convertir a SLD:**
```python
# Leer MLD, enviar como SLD
with open('datos.mld', 'r') as f:
    sld = f.read().replace('\n', '~')
    enviar_por_red(sld)
```

---

## Mejores Prácticas

### 1. Un Registro Por Línea (Siempre)

**✅ Bueno:**
```
id[1;nombre[Alicia
id[2;nombre[Roberto
```

### 2. Escapar Todos los Caracteres Especiales

**✅ Bueno:**
```python
def escapar_para_mld(s):
    s = s.replace("^", "^^")
    s = s.replace(";", "^;")
    s = s.replace("[", "^[")
    s = s.replace("{", "^{")
    s = s.replace("\n", "^\n")
    return s
```

### 3. Usar Streaming para Archivos Grandes

**✅ Bueno:**
```python
# Procesar archivo de 1GB con memoria constante
for linea in open('enorme.mld'):
    registro = decodificar_registro(linea.rstrip('\n'))
    if registro['estado'] == 'activo':
        procesar(registro)
```

### 4. Aprovechar Herramientas Unix

**✅ Bueno:**
```bash
# Filtrado rápido sin parsing
grep "nivel\[ERROR" app.mld | wc -l
```

### 5. Validar Terminaciones de Línea

**✅ Bueno:**
```python
# Normalizar terminaciones de línea
with open('datos.mld', 'r') as f:
    for linea in f:
        linea = linea.rstrip('\r\n')  # Manejar \r\n o \r
        # Procesar línea...
```

### 6. Indexar para Acceso Aleatorio

**✅ Bueno:**
```python
# Construir índice de offsets de línea
def construir_indice(archivo):
    indice = []
    with open(archivo, 'rb') as f:
        while True:
            offset = f.tell()
            linea = f.readline()
            if not linea:
                break
            indice.append(offset)
    return indice

# Acceso aleatorio usando índice
def obtener_registro(archivo, indice, num_registro):
    with open(archivo, 'rb') as f:
        f.seek(indice[num_registro])
        linea = f.readline().decode('utf-8')
        return decodificar_registro(linea.rstrip('\n'))
```

### 7. Comprimir para Almacenamiento

**✅ Bueno:**
```bash
# MLD comprime muy bien
gzip datos.mld  # A menudo 80-90% de reducción

# Procesar comprimido directamente
zcat datos.mld.gz | grep "estado\[activo"
```

### 8. Usar Herramientas Apropiadas

**Para filtrado simple:** Usar `grep`  
**Para extracción de campos:** Usar `awk`  
**Para transformaciones:** Usar `sed`  
**Para lógica compleja:** Usar Python/Node.js

---

## Documentos Relacionados

- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Especificación técnica completa
- [REFERENCIA_RAPIDA_MLD.md](REFERENCIA_RAPIDA_MLD.md) - Guía de consulta rápida
- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Variante de línea única
- [MIGRACION.md](MIGRACION.md) - Migración v1.0 a v1.1

---

**Versión:** 1.1  
**Formato:** MLD (Multi Line Data)  
**Última Actualización:** Diciembre 2024
