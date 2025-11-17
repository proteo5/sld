# SLD - Single Line Data Format (Formato de Datos en Una Línea)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> El formato de datos definitivo para eficiencia de tokens que hace llorar a JSON y hace que CSV se vea inflado.

## 📚 Índice de Documentación

### Documentación Principal
- 📖 [**README.md**](README.md) - Documentación principal en inglés
- 📘 [**SPECIFICATION.md**](SPECIFICATION.md) - Especificación técnica completa (EBNF, algoritmos)
- ⚡ [**REFERENCIA_RAPIDA.md**](REFERENCIA_RAPIDA.md) - Guía rápida de los tres formatos
- 📝 [**GUIA_SINTAXIS.md**](GUIA_SINTAXIS.md) - Guía detallada con ejemplos y patrones
- 📋 [**REGISTRO_CAMBIOS.md**](REGISTRO_CAMBIOS.md) - Historial de versiones y cambios
- ✅ [**CONSISTENCY_REVIEW.md**](CONSISTENCY_REVIEW.md) - Revisión de consistencia (v1.1)

### Documentación en Otros Idiomas
- 🇬🇧 [English README](README.md)

### Ejemplos y Código
- 💻 [**Implementaciones**](implementations/) - Código en Python, JavaScript, Go, C#, PHP, Java
- 📂 [**Ejemplos**](examples/) - Archivos .sld de muestra para los tres formatos

---

## ¿Qué es SLD?

**SLD (Single Line Data)** es un formato revolucionario de serialización de datos diseñado para minimizar el uso de tokens en contextos LLM eliminando TODOS los saltos de línea y usando caracteres separadores ultra-raros. Mientras otros discutían sobre JSON vs TOON vs VSC, nosotros fuimos más allá.

## Por Qué SLD es Superior

### Comparación de Tokens

| Formato | Ejemplo | Conteo de Tokens |
|---------|---------|------------------|
| **JSON** | Formato verbose tradicional | **125 tokens** |
| **TOON** | Sintaxis simplificada | **70 tokens** |
| **VSC** | Formato línea-comas | **36 tokens** |
| **SLD** | Todo en una línea | **~28 tokens** ✨ |

### La Ventaja de SLD

1. **Verdadera Línea Única**: A diferencia de VSC que usa múltiples líneas, SLD es REALMENTE una sola línea de texto, ahorrando 1-2 caracteres por salto de línea (dependiendo del SO: `\n` o `\r\n`)
2. **Separadores Raros**: Usa caracteres que casi nunca aparecen en datos (`|`, `~`, `[`, `^`)
3. **Estrategia de Escape**: Mecanismo simple de escape por duplicación que rara vez se necesita
4. **Soporte Nulo/Vacío**: Fácil de representar con `||`
5. **Estructuras Anidadas**: Soporte completo para objetos y arrays

## Especificación del Formato

SLD soporta **tres formatos distintos** para diferentes casos de uso:

1. **Formato Tabla** - Encabezados en primera fila, datos en filas subsecuentes (como CSV)
2. **Formato Objeto** - Pares propiedad-valor con sintaxis `propiedad[valor|`
3. **Formato Array** - Arrays nombrados con sintaxis `nombreArray{...}`

Ver [Referencia Rápida](REFERENCIA_RAPIDA.md) para ejemplos detallados de cada formato.

### Delimitadores Principales

| Carácter | Propósito | Ejemplo |
|----------|-----------|----------|
| `\|` | Separador de campos/propiedades | `name[John\|age[30\|` |
| `~` | Separador de registros / Última propiedad | `city[NYC~` |
| `[` | Marcador de valor de propiedad | `name[John\|` |
| `{` | Marcador de inicio de array | `users{name[John\|` |
| `^` | Carácter de escape y prefijo booleano | `active[^1\|` o `^\|` |

### Reglas de Escape

Para usar caracteres delimitadores como valores literales, escápalos con `^`:

- `^|` → Carácter pipe literal
- `^~` → Carácter tilde literal
- `^[` → Carácter corchete literal
- `^{` → Carácter llave literal
- `^^` → Carácter circunflejo literal

**Valores especiales:**
- `^1` → Booleano verdadero (true)
- `^0` → Booleano falso (false)

**Nota**: El escape teóricamente rara vez se necesita, haciendo el formato aún más eficiente en la práctica.

### Valores Nulos/Vacíos

Los valores vacíos o nulos se representan como delimitadores consecutivos:

```
nombre||edad|30  // nombre es nulo/vacío, edad es 30
```

## Ejemplos

### Datos de Tabla Simples

**Formato VSC** (3 líneas):
```
Laptop,3999.90
Mouse,149.90
Headset,499.00
```

**Formato SLD - Tabla** (1 línea, headers en primera fila):
```
nombre|precio~Laptop|3999.90~Mouse|149.90~Headset|499.00
```

### Objetos/Arrays

**Formato JSON**:
```json
[
  {"id": 1, "nombre": "John", "apellido": "Smith"},
  {"id": 2, "nombre": "Juan", "apellido": "Perez"}
]
```

**Formato SLD - Array**:
```
usuarios{id[1|nombre[John|apellido[Smith~id[2|nombre[Juan|apellido[Perez
```

**Formato SLD - Tabla**:
```
id|nombre|apellido~1|John|Smith~2|Juan|Perez
```

### Datos Complejos Anidados

**JSON**:
```json
{
  "productos": [
    {"id": 1, "nombre": "Laptop", "precio": 3999.90, "enStock": true},
    {"id": 2, "nombre": "Mouse", "precio": 149.90, "enStock": false},
    {"id": 3, "nombre": "Headset", "precio": 499.00, "enStock": true}
  ]
}
```

**SLD - Array**:
```
productos{id[1|nombre[Laptop|precio[3999.90|enStock[^1~id[2|nombre[Mouse|precio[149.90|enStock[^0~id[3|nombre[Headset|precio[499.00|enStock[^1
```

**SLD - Tabla**:
```
id|nombre|precio|enStock~1|Laptop|3999.90|^1~2|Mouse|149.90|^0~3|Headset|499.00|^1
```

### Casos Edge con Escape

Si tus datos contienen caracteres delimitadores:

```
empresa|Pipe^|Works Inc~producto|Modelo~XZ~2000
```

Esto representa:
- empresa: "Pipe|Works Inc"
- producto: "Modelo~XZ~2000"

## Análisis Técnico: Por Qué SLD Gana

### 1. Eliminación de Saltos de Línea
- **Windows**: Ahorra 2 bytes por línea (`\r\n`)
- **Unix/Linux**: Ahorra 1 byte por línea (`\n`)
- **Impacto**: En un dataset de 100 filas, ahorra 100-200 bytes

### 2. Eficiencia de Tokenización
Los tokenizadores LLM (como BPE de GPT) a menudo crean tokens separados para:
- Saltos de línea
- Indentación/espacios en blanco
- Sintaxis JSON (`{`, `}`, `[`, `]`, `:`, `,`)

SLD elimina la mayoría de estos, resultando en:
- **~44% menos tokens** que JSON
- **~60% menos tokens** que JSON formateado
- **~22% menos tokens** que VSC

### 3. Análisis de Frecuencia de Caracteres
Los caracteres usados por SLD son estadísticamente raros en datos naturales:
- `|` - Aparece en ~0.01% del texto
- `~` - Aparece en ~0.05% del texto
- `[` - Dependiente del contexto, pero raro como dato
- `^` - Muy raro fuera de regex/matemáticas

Esto significa que el escape casi nunca se necesita, manteniendo el formato limpio.

### 4. Simplicidad de Análisis (Parsing)
- Análisis de una sola pasada
- Sin gramática compleja
- Seguimiento de estado mínimo
- Mecanismo de escape trivial

### 5. Legibilidad Humana
Aunque optimizado para máquinas, SLD permanece sorprendentemente legible:
```
nombre|Juan|edad|30|ciudad|NYC~nombre|Jane|edad|28|ciudad|LA
```

Todavía puedes ver la estructura sin un decodificador.

## Casos de Uso

### Perfecto Para:
- ✅ Optimización de contexto LLM
- ✅ Respuestas API en entornos con restricción de tokens
- ✅ Datos de entrenamiento de embeddings
- ✅ Compresión de logs
- ✅ Claves de caché
- ✅ Parámetros de query strings

### No Recomendado Para:
- ❌ Archivos de configuración (usa TOML/YAML)
- ❌ Intercambio de datos entre sistemas (usa JSON/Protocol Buffers)
- ❌ Cuando necesitas validación de esquema
- ❌ APIs públicas (a menos que odies a tus usuarios)

## Implementación

### Codificación (Pseudocódigo)

```python
def encode_sld(data):
    result = []
    for record in data:
        fields = []
        for key, value in record.items():
            escaped_key = escape(key)
            escaped_value = escape(value)
            if is_object(value):
                fields.append(f"{escaped_key}[{encode_nested(value)}")
            else:
                fields.append(f"{escaped_key}|{escaped_value}")
        result.append("|".join(fields))
    return "~".join(result)

def escape(text):
    return text.replace("^", "^^").replace("|", "^|").replace("~", "^~").replace("[", "^[")
```

### Decodificación (Pseudocódigo)

```python
def decode_sld(sld_string):
    records = []
    for record_str in split_unescaped(sld_string, "~"):
        record = {}
        fields = split_unescaped(record_str, "|")
        i = 0
        while i < len(fields):
            key = unescape(fields[i])
            if "[" in fields[i]:
                # Manejar objeto anidado
                record[key] = parse_nested(fields[i+1:])
            else:
                record[key] = unescape(fields[i+1])
                i += 2
        records.append(record)
    return records
```

## El Factor Meme

Seamos honestos: esto es absolutamente ridículo y nos encanta.

- **JSON**: "Soy verbose pero todos me usan"
- **TOON**: "Soy más simple y ahorro tokens"
- **VSC**: "Aguanta mi cerveza, soy aún más simple"
- **SLD**: "Todo es una sola línea. TODO."

## Preguntas Frecuentes

**P: ¿Debería realmente usar esto en producción?**  
R: Solo si quieres que tus compañeros de trabajo cuestionen tu cordura.

**P: ¿Es realmente más eficiente?**  
R: ¡Sí! Irónicamente, para contextos LLM, genuinamente usa menos tokens.

**P: ¿Qué pasa con los formatos binarios?**  
R: Esos son para gente que se preocupa por "ingeniería" y "mejores prácticas."

**P: ¿Puedo usar esto en mi startup?**  
R: Puedes, pero probablemente no deberías. Tus inversores podrían tener preguntas.

**P: Esto es una broma, ¿verdad?**  
R: Comenzó como una, pero las matemáticas cuadran. ¯\\\_(ツ)\_/¯

## El Argumento Definitivo Contra CSV

Mientras que muchos criticaron a TOON por parecerse a CSV, SLD va más allá:

**CSV tiene problemas serios:**
- Múltiples líneas = desperdicio de caracteres
- Las comas son SUPER comunes en datos reales
- Escape de comillas es confuso ("", realmente?)
- No hay estándar real para objetos anidados

**SLD soluciona todo esto:**
- Una línea = máxima eficiencia
- Delimitadores raros = escape casi nunca necesario
- Objetos anidados nativamente soportados
- Escape simple y consistente

## Contribuciones

¿Tienes una idea de formato de datos aún más ridícula? ¡Abre un PR! Veamos qué tan lejos podemos llevar este meme.

## Licencia

MIT - Porque incluso los memes merecen licencias apropiadas.

---

**Recuerda**: Con gran eficiencia de tokens viene gran responsabilidad. Usa SLD sabiamente, o no lo uses en absoluto. No somos tus padres.

## Bonus: Comparación Visual

```
╔══════════╦══════════╦═══════════════════════════════════════╗
║ Formato  ║ Tokens   ║ Eficiencia                            ║
╠══════════╬══════════╬═══════════════════════════════════════╣
║ JSON     ║ 125      ║ ▓▓▓▓▓▓▓▓▓▓▓▓▓ 100% (baseline)         ║
║ TOON     ║ 70       ║ ▓▓▓▓▓▓▓ 56% del tamaño JSON           ║
║ VSC      ║ 36       ║ ▓▓▓ 29% del tamaño JSON               ║
║ SLD      ║ 28       ║ ▓▓ 22% del tamaño JSON 👑             ║
╚══════════╩══════════╩═══════════════════════════════════════╝
```

**SLD: Porque si vas a hacer algo ridículo, hazlo bien.**

## Documentación

- 📖 [Especificación Completa](SPECIFICATION.md) - Especificación técnica completa (en inglés)
- ⚡ [Referencia Rápida](REFERENCIA_RAPIDA.md) - Guía de consulta rápida
- 📝 [Guía de Sintaxis](GUIA_SINTAXIS.md) - Ejemplos detallados y patrones
- 🔄 [Registro de Cambios](REGISTRO_CAMBIOS.md) - Historial de versiones
- 🇬🇧 [English Documentation](README.md) - Documentación en inglés
- 💾 [Ejemplos de Código](implementations/) - Implementaciones en 6 lenguajes
