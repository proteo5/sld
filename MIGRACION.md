# Guía de Migración: SLD v1.0 → v1.1

Esta guía te ayuda a migrar de SLD v1.0 (usando delimitador `|`) a v1.1 (usando delimitador `;`) y elegir entre los formatos SLD y MLD.

## Tabla de Contenidos

- [Cambios Incompatibles](#cambios-incompatibles)
- [¿Por qué Migrar?](#por-qué-migrar)
- [Pasos de Migración](#pasos-de-migración)
- [Selección de Formato](#selección-de-formato)
- [Herramientas de Conversión](#herramientas-de-conversión)
- [Validación](#validación)
- [Actualización de Implementaciones](#actualización-de-implementaciones)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## Cambios Incompatibles

### ⚠️ v1.1 NO es compatible con v1.0

**Cambio Principal: Separador de Campos**
- v1.0: `|` (pipe, U+007C)
- v1.1: `;` (punto y coma, U+003B)

**Secuencias de Escape Actualizadas:**
- v1.0: `^|` para pipe literal
- v1.1: `^;` para punto y coma literal

**Nuevo Formato Agregado:**
- MLD (Multi Line Data) con salto de línea como separador de registros

## ¿Por qué Migrar?

### 1. Seguridad en Shell
El carácter pipe `|` es un separador de comandos en shells Unix:

```bash
# v1.0 - PELIGROSO
echo "name[Alice|age[30~" | grep age  # ¡Crea pipeline!

# v1.1 - SEGURO
echo "name[Alice;age[30~" | grep age  # Funciona correctamente
```

### 2. Compatibilidad con Terminal
El punto y coma requiere menos escapes en shells interactivos:

```bash
# v1.0
DATA="name[Alice\|age[30~"  # Debe escaparse el pipe

# v1.1
DATA="name[Alice;age[30~"   # No requiere escape en la mayoría de shells
```

### 3. Integración con Herramientas Unix
El formato MLD permite uso poderoso de herramientas Unix:

```bash
# Filtrar archivos de log
grep "level[ERROR" app.mld

# Contar registros
wc -l users.mld

# Monitorear en tiempo real
tail -f logs.mld
```

### 4. Soporte para Streaming
MLD permite procesamiento con memoria constante:

```bash
# Procesar archivo de millones de líneas con memoria constante
while IFS= read -r record; do
  # Procesar cada registro
  echo "$record"
done < huge_dataset.mld
```

## Pasos de Migración

### Paso 1: Respaldar Tus Datos

```bash
# Crear respaldo
cp data.sld data.sld.v1.0.backup
```

### Paso 2: Conversión Manual

**⚠️ La conversión automática NO es recomendada** debido a ambigüedad entre delimitadores escapados y no escapados.

**Cambios requeridos:**

1. Reemplazar `|` sin escape → `;`
2. Reemplazar `^|` → `^;`

**Ejemplo:**

```
# v1.0
name[John Doe|email[john@example.com|note[Use | symbol here: ^|~

# v1.1
name[John Doe;email[john@example.com;note[Use ; symbol here: ^;~
```

### Paso 3: Elegir Formato (SLD o MLD)

Ver sección [Selección de Formato](#selección-de-formato) más abajo.

### Paso 4: Validar

Parsear con decodificador v1.1 y verificar:

```python
# Validación en Python
from sld import decode_sld

try:
    data = decode_sld(tu_cadena_convertida)
    print("✓ SLD v1.1 válido")
except Exception as e:
    print(f"✗ Inválido: {e}")
```

## Selección de Formato

### Usar SLD Cuando:

✅ **Transmisión de Red**
- Respuestas de API
- Mensajes WebSocket
- Payloads de colas de mensajes

✅ **Almacenamiento Compacto**
- Sistemas embebidos
- Entornos con memoria limitada
- Contextos LLM con límite de tokens

✅ **Procesamiento de Registro Único**
- Archivos de configuración
- Datasets pequeños
- Serialización rápida

**Ejemplo:**
```
user_id[42;username[alice;email[alice@example.com;verified[^1~
```

### Usar MLD Cuando:

✅ **Archivos de Log**
- Logs de aplicación
- Logs de acceso
- Trails de auditoría

✅ **Datos en Streaming**
- Procesamiento de eventos en tiempo real
- Procesamiento de datasets grandes
- Análisis línea por línea

✅ **Procesamiento con Herramientas Unix**
- Filtrado con grep
- Transformaciones con awk
- Edición con sed
- Muestreo con head/tail

**Ejemplo:**
```
timestamp[2024-12-01T10:00:00Z;level[INFO;message[User login
timestamp[2024-12-01T10:01:00Z;level[ERROR;message[Auth failed
timestamp[2024-12-01T10:02:00Z;level[INFO;message[User logout
```

### Conversión Entre SLD y MLD

**Conversión bidireccional sin pérdidas:**

```bash
# SLD → MLD
tr '~' '\n' < data.sld > data.mld

# MLD → SLD
tr '\n' '~' < data.mld > data.sld
```

**Nota:** Ambos comandos preservan todos los datos sin pérdida.

## Herramientas de Conversión

### Script Bash

```bash
#!/bin/bash
# convert_v10_to_v11.sh

if [ $# -ne 2 ]; then
  echo "Uso: $0 <entrada_v1.0.sld> <salida_v1.1.sld>"
  exit 1
fi

INPUT="$1"
OUTPUT="$2"

# ADVERTENCIA: Este reemplazo simple puede no manejar todos los casos extremos
# Revisión manual es FUERTEMENTE recomendada

sed 's/\^|/\x00/g' "$INPUT" | \  # Reemplazar temporalmente ^|
  sed 's/|/;/g' | \                # Reemplazar todos los | restantes
  sed 's/\x00/^;/g' \              # Restaurar como ^;
  > "$OUTPUT"

echo "Conversión completa. ¡REVISA MANUALMENTE $OUTPUT antes de usar!"
```

### Script Python

```python
#!/usr/bin/env python3
# convert_v10_to_v11.py

import re
import sys

def convert_v10_to_v11(v10_string):
    """Convertir SLD v1.0 a formato v1.1."""
    # Esta es una conversión SIMPLISTA
    # Revisión manual requerida para datos de producción
    
    result = []
    i = 0
    while i < len(v10_string):
        if v10_string[i:i+2] == '^|':
            # Pipe escapado se convierte en punto y coma escapado
            result.append('^;')
            i += 2
        elif v10_string[i] == '|':
            # Pipe sin escape se convierte en punto y coma
            result.append(';')
            i += 1
        else:
            result.append(v10_string[i])
            i += 1
    
    return ''.join(result)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python3 convert_v10_to_v11.py <entrada.sld> <salida.sld>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        v10_data = f.read()
    
    v11_data = convert_v10_to_v11(v10_data)
    
    with open(sys.argv[2], 'w', encoding='utf-8') as f:
        f.write(v11_data)
    
    print(f"Convertido {sys.argv[1]} → {sys.argv[2]}")
    print("⚠️  ¡REVISA MANUALMENTE la salida antes de uso en producción!")
```

## Validación

### Lista de Verificación Pre-Migración

- [ ] Respaldados todos los datos v1.0
- [ ] Identificados todos los archivos SLD en el proyecto
- [ ] Revisadas secuencias de escape en los datos
- [ ] Probada conversión en datos de muestra
- [ ] Actualizadas librerías de parseo a v1.1

### Validación Post-Migración

```python
# Validar integridad de datos
import json
from sld_v10 import decode_sld as decode_v10
from sld_v11 import decode_sld as decode_v11

# Leer original y convertido
with open('data.v1.0.sld') as f:
    original = decode_v10(f.read())

with open('data.v1.1.sld') as f:
    converted = decode_v11(f.read())

# Comparar como JSON
assert json.dumps(original, sort_keys=True) == \
       json.dumps(converted, sort_keys=True), \
       "¡Discrepancia de datos después de conversión!"

print("✓ Validación exitosa - integridad de datos preservada")
```

### Problemas Comunes

**Problema 1: Puntos y coma en los datos**
```
# v1.0
text[Hello; World|author[Alice~

# v1.1 - INCORRECTO
text[Hello; World;author[Alice~  # ¡El punto y coma rompe el parseo!

# v1.1 - CORRECTO
text[Hello^; World;author[Alice~  # Escapar el punto y coma
```

**Problema 2: Escapes en shell**
```bash
# v1.1 - Puede necesitar escape en algunos contextos
echo 'data[value;next[value'  # Comillas simples = seguro
echo "data[value;next[value"  # Comillas dobles = seguro
echo data[value;next[value    # Sin comillas = puede necesitar escape
```

**Problema 3: Formatos mezclados**
```
# No mezclar delimitadores SLD y MLD
name[Alice;age[30~next[Bob  # SLD - OK (usa ~)
name[Alice;age[30           # MLD - OK (salto de línea termina registro)
name[Alice;age[30~          # Mezclado - INCORRECTO
```

## Actualización de Implementaciones

### Actualizar Constante de Separador de Campos

```python
# v1.0
FIELD_SEPARATOR = '|'

# v1.1
FIELD_SEPARATOR = ';'
```

```javascript
// v1.0
const FIELD_SEPARATOR = '|';

// v1.1
const FIELD_SEPARATOR = ';';
```

### Agregar Soporte MLD

```python
# Nuevas funciones MLD
def encode_mld(records):
    """Codificar registros a formato MLD (separados por salto de línea)."""
    return '\n'.join(encode_sld_record(r) for r in records)

def decode_mld(mld_string):
    """Decodificar formato MLD."""
    return [decode_sld_record(line) for line in mld_string.split('\n') if line]
```

### Actualizar Tests

```python
# Actualizar todos los casos de prueba
def test_encode_object_v11():
    data = {"name": "Alice", "age": 30}
    result = encode_sld(data)
    assert result == "name[Alice;age[30~"  # No name[Alice|age[30~
```

## Preguntas Frecuentes

### P: ¿Puedo convertir automáticamente v1.0 a v1.1?

**R:** No de manera segura. Los scripts de conversión provistos son **solo ayudas**. La revisión manual es esencial porque:

1. Los datos pueden contener puntos y coma sin escape que necesitan escaparse
2. Pipes escapados (`^|`) deben convertirse a puntos y coma escapados (`^;`)
3. Existen casos extremos dependientes del contexto

### P: ¿Debería usar SLD o MLD para mi caso de uso?

**R:** 
- **SLD**: APIs de red, almacenamiento compacto, configuraciones de registro único
- **MLD**: Archivos de log, datos en streaming, procesamiento con herramientas Unix

Ambos son interconvertibles, así que puedes usar ambos en diferentes contextos.

### P: ¿Los parsers v1.0 funcionarán con datos v1.1?

**R:** No. Los parsers v1.0 esperan delimitadores `|` y fallarán con delimitadores `;`.

### P: ¿Los parsers v1.1 funcionarán con datos v1.0?

**R:** No. Los parsers v1.1 esperan delimitadores `;` y fallarán con delimitadores `|`.

### P: ¿Cómo manejo APIs existentes usando v1.0?

**R:** Tres estrategias:

1. **Cambio incompatible**: Actualizar API a v1.1, versionar endpoint (ej., `/api/v2/`)
2. **Soporte dual**: Aceptar ambos formatos, detectar versión, deprecar v1.0
3. **Conversión en gateway**: Convertir v1.0→v1.1 en el límite de la API

### P: ¿Qué impacto tiene en el rendimiento?

**R:** Negligible. Punto y coma vs pipe no tiene diferencia de rendimiento. MLD puede ser ligeramente más lento para parseo de registro único pero mucho más rápido para streaming.

### P: ¿Puedo mezclar SLD y MLD en la misma aplicación?

**R:** ¡Sí! Patrón común:
- **Recibir**: SLD por red
- **Procesar**: Convertir a MLD para procesamiento
- **Almacenar**: MLD en archivos de log
- **Transmitir**: Convertir de vuelta a SLD para respuestas

## Recursos

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Especificación completa SLD v1.1
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Especificación completa MLD v1.1  
- [REGISTRO_CAMBIOS.md](REGISTRO_CAMBIOS.md) - Historial detallado de versiones
- [examples/](examples/) - Archivos de ejemplo en ambos formatos
- [implementations/](implementations/) - Implementaciones de referencia

## Soporte

- **Issues**: [GitHub Issues](https://github.com/proteo5/sld/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/proteo5/sld/discussions)

---

**Lista de Verificación de Migración:**

- [ ] Leer esta guía completa
- [ ] Respaldar todos los datos v1.0
- [ ] Elegir SLD o MLD para cada caso de uso
- [ ] Convertir datos (¡revisar manualmente!)
- [ ] Actualizar librerías de parseo
- [ ] Actualizar código de aplicación
- [ ] Actualizar tests
- [ ] Validar integridad de datos
- [ ] Desplegar con endpoints de API versionados
- [ ] Monitorear problemas
- [ ] Deprecar soporte v1.0

**¡Feliz migración! 🚀**
