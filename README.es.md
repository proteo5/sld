# SLD/MLD - Formato de Datos en Línea Simple/Múltiple v2.0

[![Licencia: Apache 2.0](https://img.shields.io/badge/Licencia-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Versión](https://img.shields.io/badge/versión-2.0.0-blue.svg)](https://github.com/proteo5/sld/releases)

> El formato de datos más eficiente en tokens que hace llorar a JSON y deja a CSV con sobrepeso. Ahora con formatos duales: **SLD** para transmisión compacta y **MLD** para streaming nativo de Unix.

---

## 📚 Índice de Documentación

### Documentación Principal

- 🏠 **[Este README](README.es.md)** - Resumen y guía rápida
- 📖 **[RFC Draft](RFC_SLD_MLD.txt)** - Especificación formal estilo IETF v2.0 (inglés)
- 📖 **[Especificación SLD](SPECIFICATION_SLD.md)** - Especificación técnica completa SLD v2.0 (inglés)
- 📖 **[Especificación MLD](SPECIFICATION_MLD.md)** - Especificación técnica completa MLD v2.0 (inglés)
- ⚡ **[Referencia Rápida SLD](REFERENCIA_RAPIDA_SLD.md)** - Guía de consulta rápida para SLD
- ⚡ **[Referencia Rápida MLD](REFERENCIA_RAPIDA_MLD.md)** - Guía de consulta rápida para MLD con herramientas Unix
- 🔄 **[Registro de Cambios](REGISTRO_CAMBIOS.md)** - Historial de versiones y cambios importantes
- 🔀 **[Guía de Migración](MIGRACION.md)** - Guía de actualización v1.0 → v2.0
- ⚠️ **[SPECIFICATION.md](SPECIFICATION.md)** - Especificación v1.0 OBSOLETA

### Documentación en Otros Idiomas

- 🇬🇧 **[README in English](README.md)** - Documentación completa en inglés
- 🇬🇧 **[SLD Quick Reference](QUICK_REFERENCE_SLD.md)** - Referencia rápida SLD en inglés
- 🇬🇧 **[MLD Quick Reference](QUICK_REFERENCE_MLD.md)** - Referencia rápida MLD en inglés
- 🇬🇧 **[SLD Syntax Guide](SYNTAX_GUIDE_SLD.md)** - Guía de sintaxis SLD en inglés
- 🇬🇧 **[MLD Syntax Guide](SYNTAX_GUIDE_MLD.md)** - Guía de sintaxis MLD en inglés
-- 🇬🇧 **[Migration Guide](MIGRATION.md)** - Guía de migración en inglés

### Ejemplos y Código

- 💾 **[Archivos de Ejemplo](examples/)** - Archivos .sld y .mld de ejemplo con README
- 💻 **[Implementaciones](implementations/)** - Código funcional en Python, JavaScript, Go, C#, PHP, Java

---

## Características v2.0

**Core obligatorio:**
- Separador `;` (campos), `~` (registros SLD), `\n` (registros MLD)
- Arrays `{...}`, escapes `^`, booleanos `^1`/`^0`

**Características opcionales v2.0:**
- Perfil de canonicalización (orden estable, NFC, números normalizados)
- Registro de metadatos con claves `!` y negociación `!features{...}`
- Etiquetas de tipo inline antes de `[` o `{`: `!i !f !b !s !n !d !t !ts` (ej. `edad!i[42`, `ids!i{1~2}`)
- Null tipado canónico `!n[`; alternativa legacy `^_` cuando no hay negociación de tipos

Consulta las especificaciones para los detalles normativos.

## ¿Qué es SLD/MLD?

**SLD (Single Line Data)** y **MLD (Multi Line Data)** son formatos revolucionarios de serialización de datos diseñados para minimizar el uso de tokens en contextos LLM.

- **SLD**: Formato de línea única usando tilde `~` como separador de registros. Optimizado para transmisión de red, almacenamiento compacto y conteo mínimo de tokens.
- **MLD**: Formato multilínea usando salto de línea `\n` como separador de registros. Optimizado para archivos de log, procesamiento con herramientas Unix (grep, awk, sed) y datos en streaming.

Ambos formatos usan **punto y coma** `;` como separador de campos (v2.0 cambio desde v1.0 `|` para seguridad en shells). Mientras otros discutían sobre formatos, nosotros creamos DOS que funcionan juntos perfectamente.

---

## Por qué SLD/MLD es Superior

### Comparación de Tokens

Mismo conjunto de datos (100 registros de usuarios), medido con el tokenizador de GPT-4:

| Formato | Tokens Totales | Tokens/Registro | vs JSON |
|---------|----------------|-----------------|---------|
| **SLD** | **2,200** | **22** | **-78%** ✨ |
| **MLD** | **2,300** | **23** | **-77%** |
| JSON (minificado) | 8,500 | 85 | -32% |
| JSON (formateado) | 12,500 | 125 | 0% |

Ahorro de tokens = Ahorro de dinero en APIs de LLM

### La Ventaja de SLD/MLD

```text
🏆 GANADOR: SLD/MLD
├─ 78% menos tokens que JSON
├─ Legible por humanos
├─ Sintaxis mínima
├─ Dos variantes para casos de uso específicos
└─ Conversión sin pérdidas entre SLD ↔ MLD
```

---

## Especificaciones del Formato

### Delimitadores SLD

| Delimitador | Carácter | Unicode | Uso |
|-------------|----------|---------|-----|
| **Campo** | `;` | U+003B | Separa campos dentro de un registro |
| **Registro** | `~` | U+007E | Separa registros en SLD |
| **Propiedad** | `[` | U+005B | Marca clave[valor |
| **Array inicio** | `{` | U+007B | Comienza array: `tags{item1~item2~item3}` |
| **Array cierre** | `}` | U+007D | Termina array: `...}` |
| **Escape** | `^` | U+005E | Escapa caracteres especiales |

### Delimitadores MLD

| Delimitador | Carácter | Unicode | Uso |
|-------------|----------|---------|-----|
| **Campo** | `;` | U+003B | Separa campos dentro de un registro |
| **Registro** | `\n` | U+000A | Separa registros en MLD (un registro por línea) |
| **Propiedad** | `[` | U+005B | Marca clave[valor |
| **Array inicio** | `{` | U+007B | Comienza array: `tags{item1~item2~item3}` |
| **Array cierre** | `}` | U+007D | Termina array: `...}` |
| **Escape** | `^` | U+005E | Escapa caracteres especiales |

**Diferencia clave:** SLD usa `~` para separar registros, MLD usa `\n` (salto de línea).

**Importante:** Arrays usan `{` para abrir y `}` para cerrar (NO `[`). Los corchetes `[` son SOLO para propiedades.

---

## Reglas de Escape

Usa `^` (acento circunflejo) para escapar caracteres especiales:

| Secuencia | Representa | Ejemplo |
|-----------|-----------|---------|
| `^;` | `;` (punto y coma literal) | `note[Price: $5^;99` → `"Price: $5;99"` |
| `^~` | `~` (tilde literal) | `path[home^~user` → `"home~user"` |
| `^[` | `[` (corchete literal) | `tag[^[IMPORTANT^]` → `"[IMPORTANT]"` |
| `^{` | `{` (llave literal) | `code[if (x ^> 5) ^{` → `"if (x > 5) {"` |
| `^}` | `}` (llave literal) | `code[return^; ^}]` → `"return; }"` |
| `^^` | `^` (circunflejo literal) | `math[2^^3=8` → `"2^3=8"` |
| `^1` | `true` (booleano) | `active[^1` → `true` |
| `^0` | `false` (booleano) | `verified[^0` → `false` |
<!-- Removed `^n` newline escape from table; represent newlines as literal `\n` characters inside values. -->

---

## Cuándo Usar SLD vs MLD

### Usa SLD Cuando

✅ **Transmisión de Red**

- Respuestas de API
- Mensajes WebSocket
- Protocolos personalizados
- Carga útil de red

✅ **Almacenamiento Compacto**

- Bases de datos
- Cachés
- Archivos de configuración
- Almacenamiento embebido

✅ **Contextos LLM**

- Ventanas de contexto
- Prompts
- Historiales de chat
- Embeddings

✅ **Minimización de Tokens**

- Uso de API de LLM
- Carga útil de mensajes
- Almacenamiento eficiente
- Optimización de ancho de banda

**Ejemplo SLD:**

```sld
user_id[42;username[alice;email[alice@example.com;verified[^1~user_id[43;username[bob;email[bob@example.com;verified[^0~
```

### Usa MLD Cuando

✅ **Archivos de Log**

- Logs de aplicación
- Logs de acceso
- Rastros de auditoría
- Salida de depuración

✅ **Datos de Streaming**

- Procesamiento de eventos en tiempo real
- Procesamiento de grandes conjuntos de datos
- Análisis línea por línea
- Uso constante de memoria

✅ **Procesamiento con Herramientas Unix**

- Filtrado con grep
- Transformaciones con awk
- Edición con sed
- Muestreo con head/tail

**Ejemplo MLD:**

```mld
user_id[42;username[alice;email[alice@example.com;verified[^1
user_id[43;username[bob;email[bob@example.com;verified[^0
```

### Conversión de Formato

**Conversión bidireccional sin pérdidas:**

```bash
# SLD → MLD
tr '~' '\n' < data.sld > data.mld

# MLD → SLD  
tr '\n' '~' < data.mld > data.sld
```

Ambos formatos preservan el 100% de los datos sin pérdida.

---

## Ejemplos

### Objetos Simples

**Formato SLD:**

```sld
id[1;name[Alice;age[30;city[New York~id[2;name[Bob;age[25;city[Los Angeles~
```

**Formato MLD:**

```mld
id[1;name[Alice;age[30;city[New York
id[2;name[Bob;age[25;city[Los Angeles
```

**Equivalente en JSON:**

```json
[
  {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
  {"id": 2, "name": "Bob", "age": 25, "city": "Los Angeles"}
]
```

**Tokens**: SLD/MLD: ~18 | JSON: ~65 | **Mejora de 3.6x**

---

### Productos con Arrays

**Formato SLD:**

```sld
sku[LAP001;name[UltraBook Pro;price[1299.99;tags{business~ultrabook};inStock[^1~sku[MOU001;name[Wireless Mouse;price[29.99;tags{wireless~ergonomic};inStock[^1
```

**Formato MLD:**

```mld
sku[LAP001;name[UltraBook Pro;price[1299.99;tags{business~ultrabook};inStock[^1
sku[MOU001;name[Wireless Mouse;price[29.99;tags{wireless~ergonomic};inStock[^1
```

**Equivalente en JSON:**

```json
[
  {
    "sku": "LAP001",
    "name": "UltraBook Pro",
    "price": 1299.99,
    "tags": ["business", "ultrabook"],
    "inStock": true
  },
  {
    "sku": "MOU001",
    "name": "Wireless Mouse",
    "price": 29.99,
    "tags": ["wireless", "ergonomic"],
    "inStock": true
  }
]
```

**Tokens**: SLD/MLD: ~35 | JSON: ~110 | **Mejora de 3.1x**

---

### Logs de Aplicación (Optimizado para MLD)

**Formato MLD:**

```mld
timestamp[2024-12-01T08:00:00.123Z;level[INFO;service[auth;message[User login successful;user_id[42
timestamp[2024-12-01T08:01:15.456Z;level[WARN;service[database;message[Query execution slow;duration[1.23s
timestamp[2024-12-01T08:02:30.789Z;level[ERROR;service[payment;message[Payment processing failed;error_code[E_INSUFFICIENT_FUNDS
```

**Uso de herramientas Unix:**

```bash
# Encontrar todos los logs de nivel ERROR
grep "level\[ERROR" app.mld

# Extraer todas las marcas de tiempo
awk -F';' '{print $1}' app.mld | sed 's/timestamp\[//'

# Contar niveles de log
grep -o "level\[[^;]*" app.mld | sort | uniq -c

# Monitorear en tiempo real
tail -f app.mld | grep "level\[ERROR"
```

---

### Datos Escapados

**Formato SLD:**

```sld
id[1;note[Use semicolon^; like this;code[if (x ^> 5) ^{ return^; ^}~
```

**Formato MLD:**

```mld
id[1;note[Use semicolon^; like this;code[if (x ^> 5) ^{ return^; ^}
```

Representa:

- `id`: `1`
- `note`: `Use semicolon; like this`
- `code`: `if (x > 5) { return; }`

---

## 💻 Instalación y Uso

### Python

```bash
pip install sld-format
```

```python
from sld import decode_sld, encode_sld, decode_mld, encode_mld

# Parsear SLD
data = decode_sld("name[Alice;age[30~name[Bob;age[25~")
# Retorna: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

# Parsear MLD
data = decode_mld("name[Alice;age[30\nname[Bob;age[25")
# Retorna: [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

# Generar SLD
sld = encode_sld([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
# Retorna: "name[Alice;age[30~name[Bob;age[25~"

# Generar MLD
mld = encode_mld([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])
# Retorna: "name[Alice;age[30\nname[Bob;age[25"
```

Ver [implementations/python/sld.py](implementations/python/sld.py)

---

### JavaScript/Node.js

```bash
npm install sld-format
```

```javascript
const { decodeSLD, encodeSLD, decodeMLD, encodeMLD } = require('sld-format');

// Parsear SLD
const data = decodeSLD("name[Alice;age[30~name[Bob;age[25~");
// Retorna: [{name: "Alice", age: "30"}, {name: "Bob", age: "25"}]

// Parsear MLD
const data = decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generar SLD
const sld = encodeSLD([{name: "Alice", age: 30}, {name: "Bob", age: 25}]);

// Generar MLD
const mld = encodeMLD([{name: "Alice", age: 30}, {name: "Bob", age: 25}]);
```

Ver [implementations/javascript/sld.js](implementations/javascript/sld.js)

---

### Go

```bash
go get github.com/proteo5/sld-go
```

```go
package main

import (
    "fmt"
    "github.com/proteo5/sld-go"
)

func main() {
    // Parsear SLD
    data, err := sld.DecodeSLD("name[Alice;age[30~name[Bob;age[25~")
    
    // Parsear MLD
    data, err := sld.DecodeMLD("name[Alice;age[30\nname[Bob;age[25")
    
    // Generar SLD
    sldStr, err := sld.EncodeSLD(data)
    
    // Generar MLD
    mldStr, err := sld.EncodeMLD(data)
}
```

Ver [implementations/go/sld.go](implementations/go/sld.go)

---

### C\#

```bash
dotnet add package SLD.Format
```

```csharp
using SLD;

// Parsear SLD
var data = SLDParser.Decode("name[Alice;age[30~name[Bob;age[25~");

// Parsear MLD
var data = SLDParser.DecodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generar SLD
string sld = SLDParser.EncodeSLD(data);

// Generar MLD
string mld = SLDParser.EncodeMLD(data);
```

Ver [implementations/csharp/SLD.cs](implementations/csharp/SLD.cs)

---

### PHP

```bash
composer require proteo5/sld-format
```

```php
<?php
require 'vendor/autoload.php';

use SLD\Parser;

// Parsear SLD
$data = Parser::decodeSLD("name[Alice;age[30~name[Bob;age[25~");

// Parsear MLD
$data = Parser::decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generar SLD
$sld = Parser::encodeSLD($data);

// Generar MLD
$mld = Parser::encodeMLD($data);
?>
```

Ver [implementations/php/sld.php](implementations/php/sld.php)

---

### Java

```xml
<dependency>
    <groupId>io.github.proteo5</groupId>
    <artifactId>sld-format</artifactId>
    <version>1.1.0</version>
</dependency>
```

```java
import io.github.proteo5.sld.*;

// Parsear SLD
List<Map<String, Object>> data = SLDParser.decode("name[Alice;age[30~name[Bob;age[25~");

// Parsear MLD
List<Map<String, Object>> dataMLD = SLDParser.decodeMLD("name[Alice;age[30\nname[Bob;age[25");

// Generar SLD
String sld = SLDParser.encodeSLD(data);

// Generar MLD
String mld = SLDParser.encodeMLD(data);
```

Ver `implementations/java/src/main/java/io/github/proteo5/sld/SLDParser.java`

---

## Ejemplos de Herramientas Unix (MLD)

El formato MLD está diseñado para funcionar perfectamente con herramientas estándar de Unix:

### grep - Filtrar Registros

```bash
# Encontrar todos los logs ERROR
grep "level\[ERROR" logs.mld

# Encontrar usuarios con rol admin
grep "role\[admin" users.mld

# Encontrar productos sin stock
grep "inStock\[^0" products.mld
```

### awk - Extraer y Transformar

```bash
# Extraer todos los nombres de usuario
awk -F';' '{
  for(i=1;i<=NF;i++) {
    if($i ~ /^username\[/) {
      split($i,a,"["); print a[2]
    }
  }
}' users.mld

# Calcular precio promedio
awk -F';' '
{
  for(i=1;i<=NF;i++) {
    if($i ~ /^price\[/) {
      split($i,a,"["); sum+=a[2]; count++
    }
  }
}
END {print "Promedio:", sum/count}' products.mld
```

### sed - Editar Registros

```bash
# Actualizar todos los estados pendientes a activo
sed 's/status\[pending/status[active/g' orders.mld

# Eliminar campo verified
sed 's/;verified\[[^;]*//g' users.mld
```

### head/tail - Muestrear Datos

```bash
# Primeros 10 registros
head -10 users.mld

# Últimas 5 entradas de log
tail -5 logs.mld

# Monitorear logs en tiempo real
tail -f logs.mld
```

### wc - Contar Registros

```bash
# Contar registros totales
wc -l users.mld

# Contar logs ERROR
grep "level\[ERROR" logs.mld | wc -l
```

---

## Benchmarks de Rendimiento

### Eficiencia de Tokens

Medido usando el tokenizador GPT-4 en conjunto de datos idéntico (100 registros de usuarios):

| Formato | Tokens Totales | Tokens/Registro | vs JSON |
|--------|--------------|---------------|---------|
| **SLD** | **2,200** | **22** | **-78%** ✨ |
| **MLD** | **2,300** | **23** | **-77%** |
| CSV | 3,600 | 36 | -71% |
| TOON | 7,000 | 70 | -44% |
| JSON (min) | 8,500 | 85 | -32% |
| JSON (fmt) | 12,500 | 125 | 0% |

### Velocidad de Parseo

Benchmark en 1M de registros (implementación Python):

| Formato | Tiempo de Parseo | Tiempo de Generación | Memoria |
|--------|-----------|---------------|--------|
| **SLD** | **1.2s** | **0.8s** | **45 MB** |
| **MLD** | **1.3s** | **0.9s** | **47 MB** |
| JSON | 2.8s | 1.9s | 89 MB |
| CSV | 0.9s | 0.6s | 38 MB |

Nota: CSV carece de soporte para estructuras anidadas

### Tamaño de Archivo

Mismo conjunto de datos de 100 registros de usuarios:

| Formato | Tamaño | Compresión (gzip) |
|--------|------|-------------------|
| **SLD** | **8.2 KB** | **2.1 KB** |
| **MLD** | **8.4 KB** | **2.2 KB** |
| JSON | 18.5 KB | 4.8 KB |
| CSV | 6.1 KB | 1.9 KB |

---

## Consideraciones de Seguridad

### Validación de Entrada

Siempre valida y sanitiza la entrada antes de parsear:

```python
# Ejemplo en Python
def safe_decode_sld(untrusted_input):
    # Validar longitud
    if len(untrusted_input) > MAX_INPUT_SIZE:
        raise ValueError("Entrada demasiado grande")
    
    # Validar caracteres
    if not all(ord(c) < 128 or c.isprintable() for c in untrusted_input):
        raise ValueError("Caracteres inválidos")
    
    return decode_sld(untrusted_input)
```

### Prevención de Inyección de Escape

Nunca construyas cadenas SLD/MLD con entrada de usuario sin escapar:

```python
# MAL - Vulnerable a inyección
name = user_input  # Podría contener ;~[{^
sld = f"name[{name};age[30~"

# CORRECTO - Usa el codificador
from sld import escape_value
name = escape_value(user_input)  # Escapa caracteres especiales
sld = f"name[{name};age[30~"

# MEJOR - Usa la función de codificación apropiada
data = {"name": user_input, "age": 30}
sld = encode_sld([data])
```

### Límites de Tamaño

Implementa límites razonables:

```python
MAX_INPUT_SIZE = 1_000_000  # 1MB
MAX_RECORDS = 10_000
MAX_FIELD_LENGTH = 10_000
MAX_NESTING_DEPTH = 10
```

---

## Migración desde v1.0

SLD v2.0 usa `;` en lugar de `|` como separador de campos. Ver [MIGRACION.md](MIGRACION.md) para guía completa.

### Migración Rápida

```bash
# Reemplazo simple con sed (¡revisa la salida!)
sed 's/\^|/\x00/g; s/|/;/g; s/\x00/^;/g' old_v1.0.sld > new_v2.0.sld
```

### Validación

```python
# Verificar datos migrados
from sld import decode_sld
import json

# Datos originales v1.0 (usando parser antiguo)
original = decode_sld_v10(old_data)

# Datos migrados v1.1
migrated = decode_sld(new_data)

# Comparar como JSON
assert json.dumps(original, sort_keys=True) == \
       json.dumps(migrated, sort_keys=True)
```

---

## 🤝 Contribuir

¡Damos la bienvenida a contribuciones! Ver [CONTRIBUTING.md](CONTRIBUTING.md) para directrices.

### Configuración de Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/proteo5/sld.git
cd sld

# Instalar dependencias (ejemplo Python)
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/

# Ejecutar linter
pylint sld/
```

### Agregar Nueva Implementación de Lenguaje

1. Crear directorio `implementations/{language}/`
2. Implementar `encode_sld`, `decode_sld`, `encode_mld`, `decode_mld`
3. Agregar tests comprensivos
4. Actualizar [implementations/README.md](implementations/README.md)
5. Enviar pull request

---

## Licencia

Licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.

---

## Agradecimientos

- Agradecimiento especial a [@IceSolst](https://x.com/IceSolst), [@travofoz](https://x.com/travofoz) y [@princessakano](https://x.com/princessakano) por dar el empujón necesario para crear este formato.
- Creado originalmente como una exploración humorística de eficiencia de tokens
- Creado como sátira y optimización seria
- Gracias a todos los contribuidores y primeros adoptantes

---

## FAQ

**P: ¿Debería usar SLD o MLD?**  
R: Usa SLD para almacenamiento de red/compacto, MLD para logs/streaming/herramientas Unix.

**P: ¿Es v2.0 compatible con v1.0?**  
R: No. v2.0 usa `;` en lugar de `|`. Ver [MIGRACION.md](MIGRACION.md).

**P: ¿Puedo mezclar SLD y MLD?**  
R: ¡Sí! Convierte con `tr '~' '\n'` (SLD→MLD) o `tr '\n' '~'` (MLD→SLD).

**P: ¿Cómo manejo datos binarios?**  
R: Codifica con Base64 primero, luego almacena como valor de cadena.

**P: ¿Qué pasa con Unicode?**  
R: Soporte completo UTF-8. Todos los caracteres especiales se pueden escapar.

**P: ¿Listo para producción?**  
R: Sí para v2.0 core. Bien probado, documentado, múltiples implementaciones.

---

## Enlaces

- **GitHub**: [github.com/proteo5/sld](https://github.com/proteo5/sld)
- **Issues**: [github.com/proteo5/sld/issues](https://github.com/proteo5/sld/issues)
- **Discusiones**: [github.com/proteo5/sld/discussions](https://github.com/proteo5/sld/discussions)

---

**¡Dale ⭐ a este repo si SLD/MLD te ahorró tokens!**
