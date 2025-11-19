# Referencia Rápida SLD v2.0

## Single Line Data - Referencia rápida para desarrolladores

---

## Delimitadores (v2.0)

| Símbolo | Propósito | Ejemplo |
|---------|-----------|---------|
| `;` | Separador de campos | `nombre[Alicia;edad[30` |
| `~` | Separador de registros | `registro1~registro2` |
| `[` | Marcador de propiedad | `nombre[valor` |
| `{` | Marcador de array (inicio) | `etiquetas{rojo~azul}` |
| `}` | Marcador de array (fin) | `etiquetas{rojo~azul}` |
| `^` | Carácter de escape | `texto[Hola^; Mundo` |

**⚠️ Cambio importante en v2.0:** El separador de campos cambió de `|` a `;` para mejor compatibilidad con shells.

---

## Secuencias de Escape

| Secuencia | Resultado |
|-----------|-----------|
| `^;` | `;` literal |
| `^~` | `~` literal |
| `^[` | `[` literal |
| `^{` | `{` literal |
| `^}` | `}` literal |
| `^^` | `^` literal |

**Ejemplo:**

```sld
desc[Precio: $100^; incluye impuestos
```

---

## Tipos de Datos

### Cadena (String)

```sld
nombre[Alicia
ciudad[Nueva York
```

### Número

```sld
edad[30
precio[99.99
cientifico[6.022e23
```

### Booleano

```sld
activo[^1         # verdadero
verificado[^0     # falso
```

### Nulo

```sld
segundoNombre[;edad[30    # segundoNombre es nulo
```

### Array

```sld
etiquetas{rojo~verde~azul}
puntuaciones{85~92~78}
```

---
## Extensiones v2.0 (características opcionales)

Estas funciones son aditivas y se negocian con `!features{types}`; los decodificadores sin soporte pueden ignorarlas.

### Etiquetas de tipo inline

- Coloca `!codigo` inmediatamente antes de `[` o `{`.
- Códigos: `!i` int, `!f` float, `!b` bool, `!s` string, `!d` date, `!t` time, `!ts` timestamp.
- Valores null usan secuencia de escape `^_`.

Ejemplos:

```sld
edad!i[42; precio!f[399.90; activo!b[^1; titulo!s[Hola~
ids!i{1~2~3}
creado!ts[2025-11-18T12:00:00Z~
eliminado[^_    # null explícito
```

### Registro de metadatos (primer registro)

```sld
!v[1.2;!features{types~canon}~
id!i[1;nombre!s[Ana~
```

## Ejemplos Básicos

### Objeto Simple

```sld
nombre[Alicia;edad[30;ciudad[NYC~
```

### Múltiples Registros

```sld
id[1;nombre[Alicia~id[2;nombre[Roberto~id[3;nombre[Carlos~
```

### Objeto con Array

```sld
usuario[alicia;etiquetas{admin~usuario};puntuacion[95~
```

### Contenido con Escape

```sld
nota[Usa punto y coma^; no comas;fecha[2024-01-15~
```

---

## Patrones Comunes

### Registro de Usuario

```sld
id[42;usuario[alicia;email[alicia@ejemplo.com;verificado[^1;rol[admin~
```

### Catálogo de Productos

```sld
sku[LAP001;nombre[Laptop;precio[999.99;stock[^1;etiquetas{electronica~computadoras}~
```

### Registro de Transacción

```sld
tx[1234;monto[150.50;moneda[USD;estado[completado;timestamp[2024-12-01T10:30:00Z~
```

### Configuración

```sld
host[localhost;puerto[8080;ssl[^1;timeout[30;reintentos[3~
```

---

## Guía de Codificación

**Python:**

```python
def escapar(s):
    return s.replace("^", "^^").replace(";", "^;").replace("~", "^~").replace("[", "^[").replace("{", "^{")

def codificar_objeto(obj):
    partes = [f"{escapar(k)}[{escapar(str(v))}" for k, v in obj.items()]
    return ";".join(partes[:-1]) + ";" + partes[-1].replace(";", "~") if partes else ""
```

**JavaScript:**

```javascript
const escapar = s => s.replace(/\^/g, '^^').replace(/;/g, '^;').replace(/~/g, '^~').replace(/\[/g, '^[').replace(/\{/g, '^{');

const codificarObjeto = obj => {
  const pares = Object.entries(obj).map(([k, v]) => `${escapar(k)}[${escapar(String(v))}`);
  return pares.join(';').replace(/;([^;]*)$/, '~$1');
};
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

def decodificar(sld):
    registros = []
    for registro_str in sld.split('~'):
        props = registro_str.split(';')
        obj = {}
        for prop in props:
            if '[' in prop:
                clave, valor = prop.split('[', 1)
                obj[desescape(clave)] = desescape(valor)
        registros.append(obj)
    return registros
```

---

## Conversión (SLD ↔ MLD)

**SLD a MLD:**

```bash
tr '~' '\n' < datos.sld > datos.mld
```

**MLD a SLD:**

```bash
tr '\n' '~' < datos.mld > datos.sld
```

---

## Errores Comunes

### ❌ Incorrecto: Usar `|` (delimitador v1.0)

```sld
nombre|Alicia|edad|30
```

### ✅ Correcto: Usar `;` (delimitador v2.0)

```sld
nombre[Alicia;edad[30~
```

---

### ❌ Incorrecto: No escapar caracteres especiales

```sld
nota[Costo: $50; impuestos incluidos
```

### ✅ Correcto: Escapar punto y coma

```sld
nota[Costo: $50^; impuestos incluidos~
```

---

### ❌ Incorrecto: Usar cadenas "true"/"false"

```sld
activo[true
```

### ✅ Correcto: Usar booleano `^1`

```sld
activo[^1~
```

---

### ❌ Incorrecto: Múltiples líneas

```sld
nombre[Alicia
edad[30
```

### ✅ Correcto: Una sola línea con separador

```sld
nombre[Alicia;edad[30~
```

---

## Consejos de Rendimiento

1. **Usa SLD para:** Transmisión de red, datos embebidos, envíos en un solo paquete
2. **Usa MLD para:** Logs, streaming, filtrado con grep
3. **Eficiencia de tokens:** 78% más pequeño que JSON
4. **Eficiencia de bytes:** 40-60% más pequeño que JSON formateado
5. **Parsing:** O(n) escaneo lineal, sin retroceso

---

## Uso en Shell

### Extraer valor de propiedad (básico)

```bash
echo "nombre[Alicia;edad[30~" | grep -oP 'nombre\[\K[^;~]*'
# Salida: Alicia
```

### Filtrar registros por propiedad

```bash
# Convertir a MLD primero para filtrado más fácil
tr '~' '\n' < datos.sld | grep "estado\[activo"
```

### Contar registros

```bash
echo "rec1~rec2~rec3~" | tr '~' '\n' | grep -c '^'
# Salida: 3
```

---

## Migración desde v1.0

**Buscar y reemplazar:**

- Reemplazar todos los separadores `|` con `;`
- Actualizar secuencias de escape: `^|` → `^;`
- Actualizar parsers para dividir por `;` en lugar de `|`

**Ejemplo:**

```diff
- nombre[Alicia|edad[30|ciudad[NYC~
+ nombre[Alicia;edad[30;ciudad[NYC~
```

Ver [MIGRACION.md](MIGRACION.md) para guía completa.

---

## Documentos Relacionados

- [SPECIFICATION_SLD.md](SPECIFICATION_SLD.md) - Especificación técnica completa
- [GUIA_SINTAXIS_SLD.md](GUIA_SINTAXIS_SLD.md) - Ejemplos detallados de sintaxis
- [SPECIFICATION_MLD.md](SPECIFICATION_MLD.md) - Variante multi-línea
- [MIGRACION.md](MIGRACION.md) - Guía de migración v1.0 a v2.0

---

## Solución Rápida de Problemas

**Problema:** Parser falla con punto y coma en datos  
**Solución:** Escaparlos con `^;`

**Problema:** Valores booleanos parseados como cadenas  
**Solución:** Usar `^1` (verdadero) o `^0` (falso), no "true"/"false"

**Problema:** Falta la última propiedad  
**Solución:** Asegurar que el registro termina con `~`

**Problema:** Shell interpreta punto y coma  
**Solución:** Entrecomillar la cadena SLD: `"nombre[Alicia;edad[30~"`

---

**Versión:** 1.1  
**Formato:** SLD (Single Line Data)  
**Última Actualización:** Diciembre 2024
