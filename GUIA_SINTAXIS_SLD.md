# Guía de Sintaxis SLD v1.1

**Ejemplos completos y patrones para Single Line Data**

---

## Tabla de Contenidos

1. [Sintaxis Básica](#sintaxis-básica)
2. [Tipos de Datos en Detalle](#tipos-de-datos-en-detalle)
3. [Secuencias de Escape](#secuencias-de-escape)
4. [Arrays](#arrays)
5. [Estructuras Complejas](#estructuras-complejas)
6. [Ejemplos del Mundo Real](#ejemplos-del-mundo-real)
7. [Anti-Patrones](#anti-patrones)
8. [Mejores Prácticas](#mejores-prácticas)

---

## Sintaxis Básica

### Propiedad Única
```
nombre[Alicia~
```
**Resultado:** `{"nombre": "Alicia"}`

### Múltiples Propiedades
```
nombre[Alicia;edad[30;ciudad[NYC~
```
**Resultado:** `{"nombre": "Alicia", "edad": 30, "ciudad": "NYC"}`

### Múltiples Registros
```
id[1;nombre[Alicia~id[2;nombre[Roberto~id[3;nombre[Carlos~
```
**Resultado:**
```json
[
  {"id": 1, "nombre": "Alicia"},
  {"id": 2, "nombre": "Roberto"},
  {"id": 3, "nombre": "Carlos"}
]
```

---

## Tipos de Datos en Detalle

### Cadenas

**Cadena simple:**
```
saludo[Hola Mundo~
```

**Cadena vacía:**
```
valor[;otro[dato~
```
Nota: Vacío entre `[` y `;`

**Cadena con espacios:**
```
direccion[Calle Principal 123, Apto 4B~
```

**Multi-palabra con puntuación:**
```
cita[Ser o no ser: esa es la cuestión.~
```

### Números

**Entero:**
```
cantidad[42~
edad[30~
año[2024~
```

**Decimal:**
```
precio[99.99~
temperatura[23.5~
```

**Negativo:**
```
balance[-150.50~
celsius[-10~
```

**Notación científica:**
```
avogadro[6.022e23~
planck[6.626e-34~
```

**Cero:**
```
offset[0~
```

### Booleanos

**Verdadero:**
```
activo[^1~
habilitado[^1~
verificado[^1~
```

**Falso:**
```
eliminado[^0~
publico[^0~
archivado[^0~
```

**Ejemplo mezclado:**
```
id[100;activo[^1;verificado[^0;premium[^1~
```

### Valores Nulos

**Un solo nulo:**
```
segundoNombre[;apellido[García~
```

**Múltiples nulos:**
```
nombre[Alicia;telefono[;email[;direccion[Calle Principal 123~
```

**Todos nulos:**
```
campo1[;campo2[;campo3[~
```

---

## Secuencias de Escape

### Escapar Punto y Coma

**Datos con punto y coma:**
```
instrucciones[Primero, mezcla ingredientes^; segundo, hornea a 180°C~
```

**Múltiples punto y coma:**
```
lista[Item 1^; Item 2^; Item 3^; Item 4~
```

### Escapar Tildes

**Nombres de archivo:**
```
respaldo[archivo^~respaldo.txt se convierte en archivo^^~respaldo.txt~
```

**URLs:**
```
permalink[http://ejemplo.com/pagina^~version~
```

### Escapar Corchetes

**Expresiones matemáticas:**
```
formula[x^[0^] + y^[1^] = z~
```

**Notación de array en texto:**
```
codigo[array^{0^} = valor~
```

### Escapar Circunflejos

**Texto con circunflejos:**
```
simbolo[Busca ^^ para más información~
exponente[x^^2 significa x^{circunflejo}2~
```

### Escape Complejo

**Todos los caracteres especiales:**
```
texto[Usa ^; para campos^, ^~ para registros^, ^[ para propiedades^, ^{ para arrays^, y ^^ para circunflejos~
```

**Ejemplo real - fragmento de código:**
```
codigo[if (x ^> 5 ^&^& y ^< 10) ^{ return true^; ^}~
```

---

## Arrays

### Arrays Simples

**Cadenas:**
```
etiquetas{rojo,verde,azul~
```

**Números:**
```
puntuaciones{85,92,78,95,88~
```

**Mezclado (tratado como cadenas):**
```
datos{Alicia,30,verdadero,nulo~
```

### Arrays Vacíos

```
items{~
```
Nota: `{` seguido directamente por `~`

### Un Solo Elemento

```
singleton{valor~
```

### Arrays con Contenido Escapado

**Elementos con comas:**
```
items{Item 1^, Parte A,Item 2,Item 3^, Parte B~
```

**Elementos con punto y coma:**
```
notas{Primera nota^; detalles aquí,Segunda nota,Tercera nota^; más info~
```

### Múltiples Arrays en Registro

```
id[1;etiquetas{rojo,azul;puntuaciones{85,90;estado[activo~
```

---

## Estructuras Complejas

### Objetos Anidados (Aplanados)

**Enfoque 1: Notación con guión bajo**
```
usuario_id[42;usuario_nombre[Alicia;usuario_direccion_calle[Calle Principal;usuario_direccion_ciudad[NYC;usuario_direccion_cp[10001~
```

**Enfoque 2: Notación con punto**
```
usuario.id[42;usuario.nombre[Alicia;usuario.direccion.calle[Calle Principal;usuario.direccion.ciudad[NYC~
```

### Objeto con Múltiples Arrays

```
usuario_id[42;nombreusuario[alicia;roles{admin,editor,viewer;permisos{leer,escribir,eliminar;grupos{dev,ops~
```

### Formato de Tabla

**Encabezados + Datos:**
```
id;nombre;precio;stock~1;Laptop;999.99;^1~2;Mouse;29.99;^1~3;Teclado;79.99;^0~
```

**Interpretación:**
- Primer registro: encabezados
- Registros subsecuentes: filas de datos

### Registros con Marca de Tiempo

```
ts[2024-12-01T08:00:00Z;evento[login;usuario[alicia;ip[192.168.1.100~ts[2024-12-01T08:05:00Z;evento[logout;usuario[alicia;duracion[300~
```

---

## Ejemplos del Mundo Real

### Perfil de Usuario

```
usuario_id[u_4892;nombreusuario[alicia_garcia;email[alicia@ejemplo.com;nombre_mostrar[Alicia García;bio[Desarrolladora de software y entusiasta del café;verificado[^1;creado_en[2023-05-15T10:30:00Z;avatar_url[https://cdn.ejemplo.com/avatares/alicia.jpg;contador_seguidores[1523;contador_siguiendo[342;contador_posts[89~
```

### Producto E-commerce

```
producto_id[prod_8821;sku[LAPTOP-X1;nombre[UltraBook Pro 15;descripcion[Laptop ligera con pantalla de 15 pulgadas^, 16GB RAM^, y 512GB SSD;precio[1299.99;moneda[USD;en_stock[^1;cantidad_stock[45;categorias{electronica,computadoras,laptops;etiquetas{ultrabook,negocios,portatil;calificacion[4.5;contador_resenas[234;fabricante[TechCorp;meses_garantia[24~
```

### Respuesta de API

```
estado[200;exito[^1;mensaje[Datos recuperados exitosamente;timestamp[2024-12-01T14:22:33Z;contador_datos[3;registros{id[1;nombre[Alicia,id[2;nombre[Roberto,id[3;nombre[Carlos;meta_pagina[1;meta_por_pagina[20;meta_total[156~
```

### Entrada de Log

```
timestamp[2024-12-01T09:15:42.523Z;nivel[ERROR;servicio[payment-api;mensaje[Procesamiento de pago falló: fondos insuficientes;usuario_id[u_9923;transaccion_id[tx_44821;monto[250.00;moneda[USD;codigo_error[E_FONDOS_INSUFICIENTES;contador_reintentos[3;stack_trace[at procesarPago (pago.js:145)~
```

### Archivo de Configuración

```
nombre_app[MiApp;version[2.1.0;ambiente[produccion;servidor_host[api.ejemplo.com;servidor_puerto[8443;servidor_ssl[^1;bd_host[bd.ejemplo.com;bd_puerto[5432;bd_nombre[miapp_prod;bd_tamano_pool[20;cache_habilitado[^1;cache_ttl[3600;nivel_log[info;origenes_permitidos{https://ejemplo.com,https://app.ejemplo.com;banderas_caracteristicas{nueva_ui,caracteristicas_beta,analitica_avanzada~
```

### Exportación tipo CSV

```
empleado_id;primer_nombre;apellido;departamento;salario;fecha_contratacion;activo~E001;Juan;Pérez;Ingeniería;95000;2020-03-15;^1~E002;Juana;García;Marketing;87000;2019-07-22;^1~E003;Roberto;López;Ventas;78000;2021-01-10;^1~E004;Alicia;Martínez;Ingeniería;102000;2018-11-05;^1~
```

---

## Anti-Patrones

### ❌ No hacer: Usar delimitadores incorrectos (sintaxis v1.0)

```
nombre|Alicia|edad|30
```

**Por qué:** v1.1 usa `;` no `|` para campos

**✅ Hacer:**
```
nombre[Alicia;edad[30~
```

---

### ❌ No hacer: Olvidar escapar caracteres especiales

```
nota[Costo: $50; incluye impuestos
```

**Por qué:** `;` sin escapar rompe el parsing

**✅ Hacer:**
```
nota[Costo: $50^; incluye impuestos~
```

---

### ❌ No hacer: Usar literales de cadena para booleanos

```
activo[verdadero;verificado[falso
```

**Por qué:** Parseado como cadenas, no booleanos

**✅ Hacer:**
```
activo[^1;verificado[^0~
```

---

### ❌ No hacer: Agregar saltos de línea

```
nombre[Alicia
edad[30
ciudad[NYC
```

**Por qué:** SLD debe ser de una sola línea

**✅ Hacer:**
```
nombre[Alicia;edad[30;ciudad[NYC~
```
O usar formato MLD para multi-línea

---

### ❌ No hacer: Usar corchetes/llaves de cierre

```
etiquetas[{rojo,verde,azul}]
```

**Por qué:** No hay delimitadores de cierre en SLD

**✅ Hacer:**
```
etiquetas{rojo,verde,azul~
```

---

### ❌ No hacer: Mezclar formatos de propiedad y tabla

```
nombre[Alicia;edad[30|ciudad|NYC
```

**Por qué:** Estructura inconsistente

**✅ Hacer (formato de propiedad):**
```
nombre[Alicia;edad[30;ciudad[NYC~
```

**✅ Hacer (formato de tabla):**
```
nombre;edad;ciudad~Alicia;30;NYC~
```

---

### ❌ No hacer: Usar sintaxis de array anidado

```
matriz[[1,2],[3,4]]
```

**Por qué:** Los arrays no pueden contener arrays en SLD simple

**✅ Hacer (aplanar):**
```
fila1{1,2;fila2{3,4~
```

---

## Mejores Prácticas

### 1. Nomenclatura Consistente de Propiedades

**✅ Bueno:**
```
usuario_id[42;usuario_nombre[Alicia;usuario_email[alicia@ejemplo.com~
```

**❌ Inconsistente:**
```
usuarioId[42;usuario_nombre[Alicia;UsuarioEmail[alicia@ejemplo.com~
```

### 2. Booleanos Explícitos

**✅ Bueno:**
```
activo[^1;verificado[^0~
```

**❌ Ambiguo:**
```
activo[1;verificado[0~
```
(Podría ser números o booleanos)

### 3. Usar Nulo para Datos Faltantes

**✅ Bueno:**
```
nombre[Alicia;segundoNombre[;apellido[García~
```

**❌ Malo:**
```
nombre[Alicia;segundoNombre[nulo;apellido[García~
```
(Cadena "nulo" en lugar de nulo real)

### 4. Ordenar Propiedades Lógicamente

**✅ Bueno (campos relacionados juntos):**
```
id[42;nombreusuario[alicia;email[alicia@ejemplo.com;creado[2024-01-01;activo[^1~
```

**❌ Pobre (orden aleatorio):**
```
activo[^1;nombreusuario[alicia;id[42;creado[2024-01-01;email[alicia@ejemplo.com~
```

### 5. Entrecomillar en Scripts de Shell

**✅ Bueno:**
```bash
datos="nombre[Alicia;edad[30~"
echo "$datos"
```

**❌ Malo:**
```bash
datos=nombre[Alicia;edad[30~  # ¡El shell interpreta punto y coma!
```

### 6. Validar Antes de Codificar

**✅ Bueno:**
```python
def codificar_seguro(valor):
    if valor is None:
        return ""
    if isinstance(valor, bool):
        return "^1" if valor else "^0"
    return escapar(str(valor))
```

### 7. Usar Escape Consistente

**✅ Bueno:**
```python
# Escapar en orden consistente
s = s.replace("^", "^^")  # ¡Siempre escapar ^ primero!
s = s.replace(";", "^;")
s = s.replace("~", "^~")
s = s.replace("[", "^[")
s = s.replace("{", "^{")
```

### 8. Documentar tu Esquema

**✅ Bueno:**
```
# Esquema de usuario: id, nombreusuario, email, verificado, creado_en
id[42;nombreusuario[alicia;email[alicia@ejemplo.com;verificado[^1;creado_en[2024-01-15T10:00:00Z~
```

### 9. Usar SLD/MLD Apropiadamente

**Usar SLD para:**
- Transmisión de red
- Datos en un solo paquete
- Configuraciones embebidas
- Ambientes con memoria limitada

**Usar MLD para:**
- Archivos de log
- Datos en streaming
- Procesamiento con grep
- Depuración humana

### 10. Versionar tus Datos

**✅ Bueno:**
```
version[1.1;formato[sld;datos{id[1;nombre[Alicia~
```

---

## Comparación de Sintaxis

### SLD vs JSON

**JSON:**
```json
{"nombre": "Alicia", "edad": 30, "etiquetas": ["admin", "usuario"]}
```

**SLD:**
```
nombre[Alicia;edad[30;etiquetas{admin,usuario~
```

**Ahorro:** 53 bytes → 32 bytes (40% de reducción)

---

### SLD vs CSV

**CSV:**
```
nombre,edad,ciudad
Alicia,30,NYC
Roberto,25,LA
```

**SLD (formato tabla):**
```
nombre;edad;ciudad~Alicia;30;NYC~Roberto;25;LA~
```

**SLD (formato objeto):**
```
nombre[Alicia;edad[30;ciudad[NYC~nombre[Roberto;edad[25;ciudad[LA~
```

---

### SLD vs XML

**XML:**
```xml
<usuario>
  <nombre>Alicia</nombre>
  <edad>30</edad>
</usuario>
```

**SLD:**
```
nombre[Alicia;edad[30~
```

**Ahorro:** 58 bytes → 19 bytes (67% de reducción)

---

## Patrones Avanzados

### Propiedades Condicionales

**Incluir propiedad solo si el valor existe:**
```python
def codificar_con_opcional(obj):
    partes = []
    for k, v in obj.items():
        if v is not None and v != "":
            partes.append(f"{escapar(k)}[{escapar(str(v))}")
    return ";".join(partes) + "~"
```

### Codificador en Streaming

**Generar SLD incrementalmente:**
```python
def codificar_stream(objetos):
    for obj in objetos:
        yield codificar_objeto(obj)
```

### Parsing por Bloques

**Parsear SLD grande en bloques:**
```python
def parsear_bloques(cadena_sld, tamano_bloque=1000):
    registros = cadena_sld.split('~')
    for i in range(0, len(registros), tamano_bloque):
        bloque = registros[i:i+tamano_bloque]
        yield [decodificar_registro(r) for r in bloque if r]
```

---

## Documentos Relacionados

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Especificación técnica completa
- [REFERENCIA_RAPIDA_SLD.md](REFERENCIA_RAPIDA_SLD.md) - Guía de consulta rápida
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Variante multi-línea
- [MIGRACION.md](MIGRACION.md) - Migración v1.0 a v1.1

---

**Versión:** 1.1  
**Formato:** SLD (Single Line Data)  
**Última Actualización:** Diciembre 2024
