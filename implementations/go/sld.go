// Copyright 2025 Alfredo Pinto Molina
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

// Package sld provides SLD/MLD (Single/Multi Line Data) format encoding and decoding.
// A token-efficient data serialization format - v2.0
//
// Breaking changes from v1.0:
// - Field separator changed from | to ; (semicolon)
// - Array marker changed to { (curly brace)
// - Added MLD format support (records separated by newlines)
package sld

import (
	"fmt"
	"strings"
)

// Constants
const (
	FieldSeparator     = ";"
	RecordSeparatorSLD = "~"
	RecordSeparatorMLD = "\n"
	PropertyMarker     = "["
	ArrayMarker        = "{"
	EscapeChar         = "^"
)

// EscapeValue escapes special SLD/MLD characters in a string.
func EscapeValue(text string) string {
	replacer := strings.NewReplacer(
		EscapeChar, EscapeChar+EscapeChar,
		FieldSeparator, EscapeChar+FieldSeparator,
		RecordSeparatorSLD, EscapeChar+RecordSeparatorSLD,
		PropertyMarker, EscapeChar+PropertyMarker,
		ArrayMarker, EscapeChar+ArrayMarker,
	)
	return replacer.Replace(text)
}

// UnescapeValue unescapes SLD/MLD escape sequences.
func UnescapeValue(text string) interface{} {
	var result strings.Builder
	i := 0

	for i < len(text) {
		if text[i] == EscapeChar[0] && i+1 < len(text) {
			nextChar := text[i+1]
			if nextChar == '1' {
				return true // Boolean true
			} else if nextChar == '0' {
				return false // Boolean false
			} else {
				result.WriteByte(nextChar)
			}
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
		if text[i] == EscapeChar[0] && i+1 < len(text) {
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

// EncodeRecord encodes a map to SLD/MLD format.
func EncodeRecord(record map[string]interface{}) string {
	var parts []string

	for key, value := range record {
		escapedKey := EscapeValue(key)

		switch v := value.(type) {
		case map[string]interface{}:
			// Nested object
			nested := EncodeRecord(v)
			parts = append(parts, fmt.Sprintf("%s%s%s", escapedKey, PropertyMarker, nested))
		case []interface{}:
			// Array using { marker
			var nestedItems []string
			for _, item := range v {
				nestedItems = append(nestedItems, EscapeValue(fmt.Sprint(item)))
			}
			parts = append(parts, fmt.Sprintf("%s%s%s", escapedKey, ArrayMarker, strings.Join(nestedItems, ",")))
		case bool:
			// Boolean as ^1 or ^0
			boolVal := "^0"
			if v {
				boolVal = "^1"
			}
			parts = append(parts, fmt.Sprintf("%s%s%s", escapedKey, PropertyMarker, boolVal))
		case nil:
			// Null value as ^_
			parts = append(parts, fmt.Sprintf("%s%s^_", escapedKey, PropertyMarker))
		default:
			// Regular value
			escapedValue := EscapeValue(fmt.Sprint(v))
			parts = append(parts, fmt.Sprintf("%s%s%s", escapedKey, PropertyMarker, escapedValue))
		}
	}

	return strings.Join(parts, FieldSeparator)
}

// EncodeSLD encodes data to SLD format.
func EncodeSLD(data interface{}) string {
	switch v := data.(type) {
	case []map[string]interface{}:
		var records []string
		for _, record := range v {
			records = append(records, EncodeRecord(record))
		}
		return strings.Join(records, RecordSeparatorSLD) + RecordSeparatorSLD
	case map[string]interface{}:
		return EncodeRecord(v)
	default:
		return EscapeValue(fmt.Sprint(v))
	}
}

// EncodeMLD encodes data to MLD format.
func EncodeMLD(data interface{}) string {
	switch v := data.(type) {
	case []map[string]interface{}:
		var records []string
		for _, record := range v {
			records = append(records, EncodeRecord(record))
		}
		return strings.Join(records, RecordSeparatorMLD)
	case map[string]interface{}:
		return EncodeRecord(v)
	default:
		return EscapeValue(fmt.Sprint(v))
	}
}

// DecodeRecord decodes a single record string.
func DecodeRecord(recordStr string) map[string]interface{} {
	record := make(map[string]interface{})
	fields := SplitUnescaped(recordStr, FieldSeparator)

	for _, field := range fields {
		if field == "" {
			continue
		}

		// Check for property marker
		if strings.Contains(field, PropertyMarker) && !strings.Contains(field, EscapeChar+PropertyMarker) {
			parts := strings.SplitN(field, PropertyMarker, 2)
			key := UnescapeValue(parts[0]).(string)
			var value interface{}
			if len(parts) > 1 {
				val := UnescapeValue(parts[1]).(string)
				// Handle null (^_)
				if val == "^_" {
					value = nil
				} else {
					value = val
				}
			} else {
				value = ""
			}
			record[key] = value
		} else if strings.Contains(field, ArrayMarker) && !strings.Contains(field, EscapeChar+ArrayMarker) {
			// Check for array marker
			parts := strings.SplitN(field, ArrayMarker, 2)
			key := UnescapeValue(parts[0]).(string)
			if len(parts) > 1 {
				itemStrs := strings.Split(parts[1], ",")
				items := make([]interface{}, len(itemStrs))
				for i, itemStr := range itemStrs {
					items[i] = UnescapeValue(itemStr)
				}
				record[key] = items
			} else {
				record[key] = []interface{}{}
			}
		}
	}

	return record
}

// DecodeSLD decodes SLD format string to map or slice of maps.
func DecodeSLD(sldString string) interface{} {
	if sldString == "" {
		return map[string]interface{}{}
	}

	// Remove trailing ~
	sldString = strings.TrimRight(sldString, RecordSeparatorSLD)

	var records []map[string]interface{}

	for _, recordStr := range SplitUnescaped(sldString, RecordSeparatorSLD) {
		if recordStr == "" {
			continue
		}
		records = append(records, DecodeRecord(recordStr))
	}

	if len(records) > 1 {
		return records
	} else if len(records) == 1 {
		return records[0]
	}
	return map[string]interface{}{}
}

// DecodeMLD decodes MLD format string to map or slice of maps.
func DecodeMLD(mldString string) interface{} {
	if mldString == "" {
		return map[string]interface{}{}
	}

	var records []map[string]interface{}

	for _, line := range strings.Split(mldString, RecordSeparatorMLD) {
		trimmed := strings.TrimSpace(line)
		if trimmed == "" {
			continue
		}
		records = append(records, DecodeRecord(trimmed))
	}

	if len(records) > 1 {
		return records
	} else if len(records) == 1 {
		return records[0]
	}
	return map[string]interface{}{}
}

// SLDToMLD converts SLD format to MLD format.
func SLDToMLD(sldString string) string {
	return strings.TrimRight(sldString, RecordSeparatorSLD) + RecordSeparatorMLD
}

// MLDToSLD converts MLD format to SLD format.
func MLDToSLD(mldString string) string {
	return strings.ReplaceAll(mldString, RecordSeparatorMLD, RecordSeparatorSLD) + RecordSeparatorSLD
}

// Example demonstrates SLD/MLD usage
func Example() {
	fmt.Println("=== SLD/MLD Go Implementation v2.0 ===")

	// Example 1: Simple records with SLD
	fmt.Println("Example 1: Simple user data (SLD)")
	data1 := []map[string]interface{}{
		{"name": "Alice", "age": 30, "city": "New York"},
		{"name": "Bob", "age": 25, "city": "Los Angeles"},
	}
	sld1 := EncodeSLD(data1)
	fmt.Printf("Encoded SLD: %s\n", sld1)
	fmt.Printf("Decoded: %v\n\n", DecodeSLD(sld1))

	// Example 2: Same data with MLD
	fmt.Println("Example 2: Same data (MLD)")
	mld1 := EncodeMLD(data1)
	fmt.Printf("Encoded MLD:\n%s\n", mld1)
	fmt.Printf("Decoded: %v\n\n", DecodeMLD(mld1))

	// Example 3: Arrays
	fmt.Println("Example 3: Products with tags (arrays)")
	data3 := []map[string]interface{}{
		{"sku": "LAP001", "name": "UltraBook Pro", "tags": []interface{}{"business", "ultrabook"}},
		{"sku": "MOU001", "name": "Wireless Mouse", "tags": []interface{}{"wireless", "ergonomic"}},
	}
	sld3 := EncodeSLD(data3)
	fmt.Printf("Encoded SLD: %s\n", sld3)
	fmt.Printf("Decoded: %v\n\n", DecodeSLD(sld3))

	// Example 4: Booleans
	fmt.Println("Example 4: Boolean values")
	data4 := map[string]interface{}{
		"name":     "Alice",
		"verified": true,
		"active":   false,
	}
	sld4 := EncodeSLD(data4)
	fmt.Printf("Encoded SLD: %s\n", sld4)
	fmt.Printf("Decoded: %v\n\n", DecodeSLD(sld4))

	// Example 5: Conversion SLD ↔ MLD
	fmt.Println("Example 5: Format conversion")
	sld5 := "name[Alice;age[30~name[Bob;age[25~"
	mld5 := SLDToMLD(sld5)
	fmt.Printf("SLD: %s\n", sld5)
	fmt.Printf("MLD:\n%s\n", mld5)
	fmt.Printf("Back to SLD: %s\n\n", MLDToSLD(mld5))

	// Example 6: Escaped characters
	fmt.Println("Example 6: Escaped characters")
	data6 := map[string]interface{}{
		"note": "Price: $5;99",
		"path": "C:\\Users",
	}
	sld6 := EncodeSLD(data6)
	fmt.Printf("Encoded: %s\n", sld6)
	fmt.Printf("Decoded: %v\n", DecodeSLD(sld6))
}
