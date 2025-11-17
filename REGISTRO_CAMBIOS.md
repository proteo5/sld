# Registro de Cambios

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
- Especificación inicial de SLD (Single Line Data)
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
