// Package sld provides SLD (Single Line Data) format encoding and decoding.
// A token-efficient data serialization format.
package sld

import (
	"fmt"
	"strings"
)

// Escape escapes special SLD characters in a string.
func Escape(text string) string {
	replacer := strings.NewReplacer(
		"^", "^^",
		"|", "^|",
		"~", "^~",
		"[", "^[",
	)
	return replacer.Replace(text)
}

// Unescape unescapes SLD escape sequences.
func Unescape(text string) string {
	var result strings.Builder
	i := 0

	for i < len(text) {
		if text[i] == '^' && i+1 < len(text) {
			result.WriteByte(text[i+1])
			i += 2
		} else {
			result.WriteByte(text[i])
			i++
		}
	}

	return result.String()
}

// SplitUnescaped splits text by delimiter, respecting escape sequences.
func SplitUnescaped(text, delimiter string) []string {
	var parts []string
	var current strings.Builder
	i := 0
	delimByte := delimiter[0]

	for i < len(text) {
		if text[i] == '^' && i+1 < len(text) {
			current.WriteString(text[i : i+2])
			i += 2
		} else if text[i] == delimByte {
			parts = append(parts, current.String())
			current.Reset()
			i++
		} else {
			current.WriteByte(text[i])
			i++
		}
	}

	if current.Len() > 0 || strings.HasSuffix(text, delimiter) {
		parts = append(parts, current.String())
	}

	return parts
}

// EncodeRecord encodes a map to SLD format.
func EncodeRecord(record map[string]interface{}) string {
	var parts []string

	for key, value := range record {
		escapedKey := Escape(key)

		switch v := value.(type) {
		case map[string]interface{}:
			nested := EncodeRecord(v)
			parts = append(parts, fmt.Sprintf("%s[%s", escapedKey, nested))
		case []interface{}:
			var nestedItems []string
			for _, item := range v {
				if itemMap, ok := item.(map[string]interface{}); ok {
					nestedItems = append(nestedItems, EncodeRecord(itemMap))
				} else {
					nestedItems = append(nestedItems, Escape(fmt.Sprint(item)))
				}
			}
			parts = append(parts, fmt.Sprintf("%s[%s", escapedKey, strings.Join(nestedItems, "~")))
		case nil:
			parts = append(parts, fmt.Sprintf("%s|", escapedKey))
		default:
			escapedValue := Escape(fmt.Sprint(v))
			parts = append(parts, fmt.Sprintf("%s|%s", escapedKey, escapedValue))
		}
	}

	return strings.Join(parts, "|")
}

// Encode encodes data to SLD format.
func Encode(data interface{}) string {
	switch v := data.(type) {
	case []map[string]interface{}:
		var records []string
		for _, record := range v {
			records = append(records, EncodeRecord(record))
		}
		return strings.Join(records, "~")
	case map[string]interface{}:
		return EncodeRecord(v)
	default:
		return Escape(fmt.Sprint(v))
	}
}

// Decode decodes SLD format string to map or slice of maps.
func Decode(sldString string) interface{} {
	if sldString == "" {
		return map[string]interface{}{}
	}

	var records []map[string]interface{}

	for _, recordStr := range SplitUnescaped(sldString, "~") {
		if recordStr == "" {
			continue
		}

		record := make(map[string]interface{})
		fields := SplitUnescaped(recordStr, "|")

		i := 0
		for i < len(fields) {
			if i >= len(fields) {
				break
			}

			key := Unescape(fields[i])

			// Check if this is a nested structure
			if strings.Contains(fields[i], "[") && !strings.Contains(fields[i], "^[") {
				key = strings.Replace(key, "[", "", -1)
				if i+1 < len(fields) {
					nestedValue := Unescape(fields[i+1])
					record[key] = nestedValue
					i += 2
				} else {
					i++
				}
			} else {
				if i+1 < len(fields) {
					value := Unescape(fields[i+1])
					if value != "" {
						record[key] = value
					} else {
						record[key] = nil
					}
					i += 2
				} else {
					record[key] = nil
					i++
				}
			}
		}

		records = append(records, record)
	}

	if len(records) > 1 {
		return records
	} else if len(records) == 1 {
		return records[0]
	}
	return map[string]interface{}{}
}

// Example demonstrates SLD usage
func Example() {
	fmt.Println("=== SLD Go Implementation ===\n")

	// Example 1: Simple records
	fmt.Println("Example 1: Simple product data")
	data1 := []map[string]interface{}{
		{"name": "Laptop", "price": "3999.90"},
		{"name": "Mouse", "price": "149.90"},
		{"name": "Headset", "price": "499.00"},
	}
	sld1 := Encode(data1)
	fmt.Printf("Encoded: %s\n", sld1)
	fmt.Printf("Decoded: %v\n\n", Decode(sld1))

	// Example 2: Objects with IDs
	fmt.Println("Example 2: User records")
	data2 := []map[string]interface{}{
		{"id": "1", "name": "John", "lastname": "Smith"},
		{"id": "2", "name": "Juan", "lastname": "Perez"},
	}
	sld2 := Encode(data2)
	fmt.Printf("Encoded: %s\n", sld2)
	fmt.Printf("Decoded: %v\n\n", Decode(sld2))

	// Example 3: Data with special characters
	fmt.Println("Example 3: Escaped characters")
	data3 := []map[string]interface{}{
		{"company": "Pipe|Works Inc"},
		{"product": "Model~XZ~2000"},
	}
	sld3 := Encode(data3)
	fmt.Printf("Encoded: %s\n", sld3)
	fmt.Printf("Decoded: %v\n\n", Decode(sld3))

	// Example 4: Null values
	fmt.Println("Example 4: Null/empty values")
	data4 := map[string]interface{}{
		"name":     "John",
		"middle":   nil,
		"lastname": "Doe",
	}
	sld4 := Encode(data4)
	fmt.Printf("Encoded: %s\n", sld4)
	fmt.Printf("Decoded: %v\n", Decode(sld4))
}
