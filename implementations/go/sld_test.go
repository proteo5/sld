package sld

import (
	"reflect"
	"strings"
	"testing"
)

func TestEscapeValue(t *testing.T) {
	tests := []struct {
		input    string
		expected string
	}{
		{"a;b", "a^;b"},
		{"a~b", "a^~b"},
		{"a[b", "a^[b"},
		{"a{b", "a^{b"},
		{"a^b", "a^^b"},
	}

	for _, tt := range tests {
		result := escapeValue(tt.input)
		if result != tt.expected {
			t.Errorf("escapeValue(%q) = %q, want %q", tt.input, result, tt.expected)
		}
	}
}

func TestUnescapeValue(t *testing.T) {
	tests := []struct {
		input    string
		expected interface{}
	}{
		{"a^;b", "a;b"},
		{"a^;b^~c", "a;b~c"},
		{"^1", true},
		{"^0", false},
		{"Alice", "Alice"},
	}

	for _, tt := range tests {
		result := unescapeValue(tt.input)
		if !reflect.DeepEqual(result, tt.expected) {
			t.Errorf("unescapeValue(%q) = %v, want %v", tt.input, result, tt.expected)
		}
	}
}

func TestEncodeSLD(t *testing.T) {
	t.Run("Single record", func(t *testing.T) {
		data := map[string]interface{}{"name": "Alice", "age": 30}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "name[Alice") {
			t.Errorf("Expected 'name[Alice' in %q", sld)
		}
		if !strings.Contains(sld, "age[30") {
			t.Errorf("Expected 'age[30' in %q", sld)
		}
	})

	t.Run("Multiple records", func(t *testing.T) {
		data := []map[string]interface{}{
			{"name": "Alice"},
			{"name": "Bob"},
		}
		sld := EncodeSLD(data)
		count := strings.Count(sld, "~")
		if count < 2 {
			t.Errorf("Expected at least 2 tildes, got %d", count)
		}
	})

	t.Run("Array encoding", func(t *testing.T) {
		data := map[string]interface{}{"tags": []interface{}{"admin", "user"}}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "tags{admin,user") {
			t.Errorf("Expected 'tags{admin,user' in %q", sld)
		}
	})

	t.Run("Boolean true", func(t *testing.T) {
		data := map[string]interface{}{"verified": true}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "verified[^1") {
			t.Errorf("Expected 'verified[^1' in %q", sld)
		}
	})

	t.Run("Boolean false", func(t *testing.T) {
		data := map[string]interface{}{"active": false}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "active[^0") {
			t.Errorf("Expected 'active[^0' in %q", sld)
		}
	})

	t.Run("Null value", func(t *testing.T) {
		data := map[string]interface{}{"middle": nil}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "middle[") {
			t.Errorf("Expected 'middle[' in %q", sld)
		}
	})

	t.Run("Escaped characters", func(t *testing.T) {
		data := map[string]interface{}{"note": "Price: $5;99"}
		sld := EncodeSLD(data)
		if !strings.Contains(sld, "note[Price: $5^;99") {
			t.Errorf("Expected 'note[Price: $5^;99' in %q", sld)
		}
	})
}

func TestDecodeSLD(t *testing.T) {
	t.Run("Single record", func(t *testing.T) {
		sld := "name[Alice;age[30"
		data := DecodeSLD(sld)
		record, ok := data.(map[string]interface{})
		if !ok {
			t.Fatal("Expected map[string]interface{}")
		}
		if record["name"] != "Alice" {
			t.Errorf("Expected name=Alice, got %v", record["name"])
		}
		if record["age"] != "30" {
			t.Errorf("Expected age=30, got %v", record["age"])
		}
	})

	t.Run("Multiple records", func(t *testing.T) {
		sld := "name[Alice~name[Bob~"
		data := DecodeSLD(sld)
		records, ok := data.([]map[string]interface{})
		if !ok {
			t.Fatal("Expected []map[string]interface{}")
		}
		if len(records) != 2 {
			t.Errorf("Expected 2 records, got %d", len(records))
		}
		if records[0]["name"] != "Alice" {
			t.Errorf("Expected first name=Alice, got %v", records[0]["name"])
		}
		if records[1]["name"] != "Bob" {
			t.Errorf("Expected second name=Bob, got %v", records[1]["name"])
		}
	})

	t.Run("Array decoding", func(t *testing.T) {
		sld := "tags{admin,user"
		data := DecodeSLD(sld)
		record := data.(map[string]interface{})
		tags := record["tags"].([]string)
		if !reflect.DeepEqual(tags, []string{"admin", "user"}) {
			t.Errorf("Expected [admin user], got %v", tags)
		}
	})

	t.Run("Boolean true", func(t *testing.T) {
		sld := "verified[^1"
		data := DecodeSLD(sld)
		record := data.(map[string]interface{})
		if record["verified"] != true {
			t.Errorf("Expected verified=true, got %v", record["verified"])
		}
	})

	t.Run("Boolean false", func(t *testing.T) {
		sld := "active[^0"
		data := DecodeSLD(sld)
		record := data.(map[string]interface{})
		if record["active"] != false {
			t.Errorf("Expected active=false, got %v", record["active"])
		}
	})
}

func TestEncodeMLD(t *testing.T) {
	t.Run("Single record", func(t *testing.T) {
		data := map[string]interface{}{"name": "Alice", "age": 30}
		mld := EncodeMLD(data)
		if !strings.Contains(mld, "name[Alice") {
			t.Errorf("Expected 'name[Alice' in %q", mld)
		}
		if !strings.Contains(mld, "age[30") {
			t.Errorf("Expected 'age[30' in %q", mld)
		}
	})

	t.Run("Multiple records", func(t *testing.T) {
		data := []map[string]interface{}{
			{"name": "Alice"},
			{"name": "Bob"},
		}
		mld := EncodeMLD(data)
		if !strings.Contains(mld, "\n") {
			t.Error("Expected newline in MLD")
		}
		lines := strings.Split(mld, "\n")
		if len(lines) != 2 {
			t.Errorf("Expected 2 lines, got %d", len(lines))
		}
	})
}

func TestDecodeMLD(t *testing.T) {
	t.Run("Single record", func(t *testing.T) {
		mld := "name[Alice;age[30"
		data := DecodeMLD(mld)
		record := data.(map[string]interface{})
		if record["name"] != "Alice" {
			t.Errorf("Expected name=Alice, got %v", record["name"])
		}
		if record["age"] != "30" {
			t.Errorf("Expected age=30, got %v", record["age"])
		}
	})

	t.Run("Multiple records", func(t *testing.T) {
		mld := "name[Alice\nname[Bob"
		data := DecodeMLD(mld)
		records := data.([]map[string]interface{})
		if len(records) != 2 {
			t.Errorf("Expected 2 records, got %d", len(records))
		}
	})
}

func TestFormatConversion(t *testing.T) {
	t.Run("SLD to MLD", func(t *testing.T) {
		sld := "name[Alice~name[Bob~"
		mld := SLDToMLD(sld)
		if strings.Contains(mld, "~") {
			t.Error("MLD should not contain tildes")
		}
		if !strings.Contains(mld, "\n") {
			t.Error("MLD should contain newlines")
		}
	})

	t.Run("MLD to SLD", func(t *testing.T) {
		mld := "name[Alice\nname[Bob"
		sld := MLDToSLD(mld)
		if strings.Contains(sld, "\n") {
			t.Error("SLD should not contain newlines")
		}
		if !strings.Contains(sld, "~") {
			t.Error("SLD should contain tildes")
		}
	})

	t.Run("Round trip SLD->MLD->SLD", func(t *testing.T) {
		original := "name[Alice;age[30~name[Bob;age[25~"
		mld := SLDToMLD(original)
		backToSLD := MLDToSLD(mld)
		if backToSLD != original {
			t.Errorf("Round trip failed: %q != %q", backToSLD, original)
		}
	})

	t.Run("Round trip MLD->SLD->MLD", func(t *testing.T) {
		original := "name[Alice;age[30\nname[Bob;age[25"
		sld := MLDToSLD(original)
		backToMLD := SLDToMLD(sld)
		if backToMLD != original {
			t.Errorf("Round trip failed: %q != %q", backToMLD, original)
		}
	})
}

func TestEdgeCases(t *testing.T) {
	t.Run("Empty string SLD", func(t *testing.T) {
		data := DecodeSLD("")
		record := data.(map[string]interface{})
		if len(record) != 0 {
			t.Errorf("Expected empty map, got %v", record)
		}
	})

	t.Run("Empty string MLD", func(t *testing.T) {
		data := DecodeMLD("")
		record := data.(map[string]interface{})
		if len(record) != 0 {
			t.Errorf("Expected empty map, got %v", record)
		}
	})

	t.Run("Empty object encoding", func(t *testing.T) {
		sld := EncodeSLD(map[string]interface{}{})
		if sld != "" {
			t.Errorf("Expected empty string, got %q", sld)
		}
	})

	t.Run("Special characters preserved", func(t *testing.T) {
		data := map[string]interface{}{"path": "C:\\Users\\Alice"}
		sld := EncodeSLD(data)
		decoded := DecodeSLD(sld)
		record := decoded.(map[string]interface{})
		if record["path"] != "C:\\Users\\Alice" {
			t.Errorf("Expected path preserved, got %v", record["path"])
		}
	})
}

func TestComplexData(t *testing.T) {
	data := map[string]interface{}{
		"name":     "Alice",
		"age":      30,
		"verified": true,
		"tags":     []interface{}{"admin", "user"},
		"middle":   nil,
	}
	sld := EncodeSLD(data)
	decoded := DecodeSLD(sld)
	record := decoded.(map[string]interface{})

	if record["name"] != "Alice" {
		t.Errorf("Expected name=Alice, got %v", record["name"])
	}
	if record["verified"] != true {
		t.Errorf("Expected verified=true, got %v", record["verified"])
	}
	tags := record["tags"].([]string)
	if !reflect.DeepEqual(tags, []string{"admin", "user"}) {
		t.Errorf("Expected tags=[admin user], got %v", tags)
	}
}
