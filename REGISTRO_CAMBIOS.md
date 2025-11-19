# Registro de Cambios
## [1.2.0] - 2025-11-18

### Agregado

- Perfil de Canonicalización: orden estable de campos, arrays sin `~` final, normalización NFC, formato numérico normalizado.
- Registro de metadatos (claves reservadas con `!`): `!v`, `!schema`, `!ts`, `!source`, `!features{...}`.
- Tipos explícitos opcionales con sufijo `@i @f @b @s @null @d @t @ts`.
- Token opcional de null `^_` (requiere negociación `!features{null}`).
- Tabla de códigos de error E01–E10 para decodificadores.

### Compatibilidad

- Cambios aditivos y compatibles hacia atrás cuando los productores negocian mediante `!features`. Los decodificadores v1.1 pueden ignorar claves `!` y sufijos de tipo desconocidos. Los productores DEBEN evitar `^_` salvo que la contraparte anuncie soporte.

---

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

---

## [1.1] - 2025-11-16

### Cambiado
- **Sintaxis de Booleanos:** Cambio de `true`/`false` a `^1`/`^0` para mayor consistencia con caracteres de escape y eficiencia de tokens
- **Sintaxis de Arrays:** Cambio del marcador de inicio de array de `arrayNombre[` a `arrayNombre{` para mejor diferenciación visual del marcador de valores `[`
- **Formato de Tabla:** Clarificado que la primera fila debe contener los encabezados
- **Ejemplos de Tipos Primitivos:** Actualizados todos los ejemplos para mostrar el uso correcto de separadores

### Corregido
- **Terminación de Arrays:** Clarificado que el último objeto en un array NO debe tener un `~` al final (separador, no terminador)
- **Ejemplos en Documentación:** Corregidos todos los ejemplos de arrays para eliminar el `~` incorrecto al final
- **Sintaxis de Objetos Anidados:** Removidos ejemplos imposibles de parsear, reemplazados con notación aplanada o codificación de arrays
- **Diagramas Visuales:** Actualizados para reflejar las reglas de terminación de arrays correctas

### Agregado
- **CONSISTENCY_REVIEW.md:** Documento completo que detalla todas las correcciones realizadas durante la revisión de consistencia
- **Secuencias de Escape:** Agregado `^{` para escapar el marcador de inicio de array
- **Sección de Validación:** Agregada lista de validación en SYNTAX_GUIDE.md

---

## [1.0] - 2025-11-15

### Agregado
# Registro de Cambios

Todos los cambios notables al formato SLD/MLD serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-12-01

### Cambios Incompatibles

⚠️ **Esta versión NO es compatible con v1.0**

- **Cambio del separador de campos de `|` a `;`**
  - Razón: El carácter pipe (`|`) requiere escape en shells Unix (bash, zsh) y causa conflictos en uso de terminal
  - El punto y coma (`;`) es estadísticamente más raro en texto natural y causa menos conflictos en shell
  - Migración: Reemplazar todos los `|` sin escape con `;` y `^|` con `^;`

### Agregado

- **Formato MLD (Multi Line Data) introducido**
  - Nueva variante usando salto de línea (`\n`) como separador de registros en lugar de tilde (`~`)
  - Extensión de archivo: `.mld`
  - Tipo MIME: `text/mld`
  - Optimizado para:
    - Archivos de log y datos en streaming
    - Procesamiento con herramientas Unix (grep, awk, sed, head, tail)
    - Procesamiento línea por línea con memoria constante
    - Depuración e inspección humana
  
- **Conversión bidireccional entre SLD y MLD**
  - SLD → MLD: `tr '~' '\n' < archivo.sld > archivo.mld`
  - MLD → SLD: `tr '\n' '~' < archivo.mld > archivo.sld`
  - Conversión sin pérdidas en ambas direcciones

- **Documentación completa**
  - SPECIFICATION_SLD.md - Especificación técnica completa de SLD
  - SPECIFICATION_MLD.md - Especificación técnica completa de MLD
  - QUICK_REFERENCE_SLD.md - Guía de referencia rápida SLD
  - QUICK_REFERENCE_MLD.md - Guía de referencia rápida MLD con herramientas Unix
  - SYNTAX_GUIDE_SLD.md - Ejemplos detallados de sintaxis SLD
  - SYNTAX_GUIDE_MLD.md - Sintaxis detallada MLD con patrones de streaming
  - Versiones en español: REFERENCIA_RAPIDA_*.md, GUIA_SINTAXIS_*.md

- **Archivos de ejemplo**
  - 7 ejemplos SLD: simple, productos, usuarios, escaped, complejo, logs, config
  - 7 ejemplos MLD: mismo contenido en formato multi-línea
  - README completo con patrones de uso y ejemplos de herramientas Unix

### Cambiado

- **Tabla de delimitadores actualizada**
  - Separador de campos: `|` (U+007C) → `;` (U+003B)
  - Todas las secuencias de escape actualizadas: `^|` → `^;`
  - Separador de registros: `~` (U+007E) - sin cambios para SLD, `\n` para MLD
  - Marcador de propiedad: `[` (U+005B) - sin cambios
  - Marcador de array: `{` (U+007B) - sin cambios
  - Carácter de escape: `^` (U+005E) - sin cambios

- **Extensiones de archivo clarificadas**
  - `.sld` - Single Line Data (formato SLD)
  - `.mld` - Multi Line Data (formato MLD)

- **Tipos MIME definidos**
  - `application/sld+compact` - formato SLD
  - `text/mld` - formato MLD

### Obsoleto

- **Formato v1.0 usando `|` como separador de campos**
  - SPECIFICATION.md marcado como obsoleto
  - No se proporciona ruta de migración - ruptura limpia
  - Las implementaciones legacy deberían actualizar a v1.1

### Seguridad

- Seguridad en shell mejorada al usar punto y coma en lugar de pipe
- Riesgo reducido de inyección de comandos en contextos de shell
- Mismas propiedades de seguridad del mecanismo de escape mantenidas

### Rendimiento

- Eficiencia de tokens sin cambios: 78% de reducción vs JSON
- Eficiencia de bytes sin cambios para SLD
- MLD agrega compatibilidad con herramientas Unix con overhead mínimo

## [1.0.0] - 2024-11-16

### Agregado

- Especificación inicial del formato SLD
- Separador de campos: `|` (U+007C)
- Separador de registros: `~` (U+007E)
- Marcador de propiedad: `[` (U+005B)
- Marcador de array: `{` (U+007B)
- Carácter de escape: `^` (U+005E)
- Valores booleanos: `^1` (verdadero), `^0` (falso)
- Formato de una sola línea optimizado para eficiencia de tokens
- 78% de reducción de tokens comparado con JSON
- Documentación básica y ejemplos

### Notas

- Creado como respuesta satírica a las tendencias de minimalismo de formatos
- Funcional pero principalmente educativo/experimental

---

## Notas de Migración

### Actualizar de v1.0 a v1.1

**La conversión automática NO es posible** debido a ambigüedad en las secuencias de escape.

**Pasos manuales requeridos:**

1. **Reemplazar separadores de campos:**
   - Buscar: `|` (pipes sin escape)
   - Reemplazar: `;`

2. **Actualizar secuencias de escape:**
   - Buscar: `^|` (pipes con escape)
   - Reemplazar: `^;`

3. **Validar datos:**
   - Parsear con decodificador v1.1
   - Verificar que todos los registros cargan correctamente
   - Verificar integridad de datos

4. **Elegir formato:**
   - Usar SLD (`.sld`) para transmisión de red, almacenamiento compacto
   - Usar MLD (`.mld`) para logs, streaming, procesamiento con herramientas Unix

5. **Actualizar implementaciones:**
   - Actualizar parsers a v1.1
   - Actualizar constante de separador de campos
   - Agregar soporte MLD si es necesario

### Guía de Selección de Formato

**Usar SLD cuando:**
- Se envía datos por red
- Se minimiza conteo de tokens para LLMs
- Se almacena en entornos con memoria limitada
- Procesamiento de registro único

**Usar MLD cuando:**
- Se escriben archivos de log
- Se procesa con grep/awk/sed
- Se transmiten datasets grandes en streaming
- Se necesita procesamiento línea por línea
- Depuración/inspección humana

Ambos formatos son interconvertibles sin pérdida de datos.

---

## Comparación con Otros Formatos

### Eficiencia de Tokens (v1.1)

| Formato | Tokens | Reducción vs JSON |
|--------|--------|-------------------|
| JSON (formateado) | 100 | 0% |
| JSON (minificado) | 68 | 32% |
| CSV | 29 | 71% |
| **SLD/MLD** | **22** | **78%** |

### Comparación de Casos de Uso

| Característica | SLD | MLD | JSON | CSV |
|---------|-----|-----|------|-----|
| Eficiencia de tokens | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Legibilidad humana | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Soporte herramientas Unix | ⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| Estructuras anidadas | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Streaming | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Transmisión de red | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

[1.1.0]: https://github.com/proteo5/sld/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/proteo5/sld/releases/tag/v1.0.0
- Tres formatos primarios: Tabla, Objeto y Array
- Delimitadores del núcleo: `|` (campo), `~` (registro), `[` (propiedad)
- Secuencias de escape: `^|`, `^~`, `^[`, `^^`
- Codificación UTF-8 con validación
- Gramática EBNF completa
- Algoritmos de codificación y decodificación
- Sección de análisis técnico y eficiencia de tokens
- Documentación en inglés y español
- Implementaciones en 6 lenguajes:
  - Python (sld.py)
  - JavaScript (sld.js)
  - Go (sld.go)
  - C# (SLD.cs)
  - PHP (sld.php)
  - Java (SLD.java)
- Archivos de ejemplo:
  - simple.sld (formato tabla)
  - objects.sld (formato array)
  - complex.sld (array con booleanos)
  - escaped.sld (caracteres especiales)
- QUICK_REFERENCE.md para consulta rápida
- SYNTAX_GUIDE.md con ejemplos detallados
- Documentación de comparación con JSON, CSV y TOON

### Soporte de Tipos de Datos
- Cadenas (con soporte completo UTF-8)
- Números (enteros y decimales)
- Booleanos (sintaxis inicial `true`/`false`)
- Valores nulos/vacíos
- Arrays de objetos
- Objetos anidados (via aplanamiento con guiones bajos)

### Características de Eficiencia
- Reducción de 78% en tokens vs JSON (28 tokens vs 125 tokens)
- Reducción de 22% en tokens vs TOON (28 tokens vs 36 tokens)
- Codificación de una sola línea para contextos de LLM
- Auto-documentación via nombres de propiedades explícitas
- Sin caracteres de comillas redundantes

---

## [Futuro] - Planeado

### Posibles Mejoras
- Soporte para tipos de datos adicionales (fechas nativas, binarios)
- Herramientas de validación de esquema
- Compresión optimizada para grandes conjuntos de datos
- Herramientas de conversión (JSON↔SLD, CSV↔SLD)
- Validador en línea y visualizador
- Plugins para editores (VS Code, Sublime Text)
- Benchmarks de rendimiento vs otros formatos

### En Consideración
- Sintaxis opcional para comentarios
- Soporte de espacios en blanco multi-línea (para legibilidad humana)
- Extensiones para casos de uso específicos (configuración, logs, API)

---

## Notas de Migración

### Migración de v1.0 a v1.1

Si estás usando SLD v1.0, necesitas actualizar:

1. **Booleanos:**
   ```
   Antes (v1.0): activo[true|verificado[false~
   Ahora (v1.1):  activo[^1|verificado[^0~
   ```

2. **Inicio de Arrays:**
   ```
   Antes (v1.0): usuarios[id[1|nombre[Ana~id[2|nombre[Bob~
   Ahora (v1.1):  usuarios{id[1|nombre[Ana~id[2|nombre[Bob
   ```

3. **Terminación de Arrays:**
   ```
   Antes (v1.0): usuarios{id[1|nombre[Ana~id[2|nombre[Bob~
   Ahora (v1.1):  usuarios{id[1|nombre[Ana~id[2|nombre[Bob
                                                        ^
                                                   Sin ~ al final
   ```

**Herramientas de Migración:** Las implementaciones de código v1.1 incluyen compatibilidad con formatos v1.0 para facilitar la transición.

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Reporta bugs via GitHub Issues
2. Propón mejoras con casos de uso claros
3. Envía pull requests con tests
4. Actualiza documentación para nuevas características

---

## Licencia

Este proyecto está bajo licencia MIT - ver archivo [LICENSE](LICENSE) para detalles.
