package io.github.proteo5.sld;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;

public class SLDTest {

    // Escaping Tests
    @Test
    public void testEscapeSemicolon() {
        assertEquals("a^;b", SLDParser.escapeValue("a;b"));
    }

    @Test
    public void testEscapeTilde() {
        assertEquals("a^~b", SLDParser.escapeValue("a~b"));
    }

    @Test
    public void testEscapeBracket() {
        assertEquals("a^[b", SLDParser.escapeValue("a[b"));
    }

    @Test
    public void testEscapeBrace() {
        assertEquals("a^{b", SLDParser.escapeValue("a{b"));
    }

    @Test
    public void testEscapeCaret() {
        assertEquals("a^^b", SLDParser.escapeValue("a^b"));
    }

    @Test
    public void testUnescapeSemicolon() {
        assertEquals("a;b", SLDParser.unescapeValue("a^;b"));
    }

    @Test
    public void testUnescapeMultiple() {
        assertEquals("a;b~c", SLDParser.unescapeValue("a^;b^~c"));
    }

    // SLD Encoding Tests
    @Test
    public void testSingleRecord() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("name", "Alice");
        data.put("age", 30);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("name[Alice"));
        assertTrue(sld.contains("age[30"));
    }

    @Test
    public void testMultipleRecords() {
        List<Map<String, Object>> data = new ArrayList<>();
        Map<String, Object> record1 = new LinkedHashMap<>();
        record1.put("name", "Alice");
        Map<String, Object> record2 = new LinkedHashMap<>();
        record2.put("name", "Bob");
        data.add(record1);
        data.add(record2);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("~"));
        int count = sld.length() - sld.replace("~", "").length();
        assertTrue(count >= 2);
    }

    @Test
    public void testArrayEncoding() {
        Map<String, Object> data = new LinkedHashMap<>();
        List<String> tags = Arrays.asList("admin", "user");
        data.put("tags", tags);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("tags{admin,user"));
    }

    @Test
    public void testBooleanTrue() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("verified", true);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("verified[^1"));
    }

    @Test
    public void testBooleanFalse() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("active", false);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("active[^0"));
    }

    @Test
    public void testNullValue() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("middle", null);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("middle["));
    }

    @Test
    public void testEscapedCharacters() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("note", "Price: $5;99");
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("note[Price: $5^;99"));
    }

    // SLD Decoding Tests
    @Test
    public void testDecodeSingleRecord() {
        String sld = "name[Alice;age[30";
        Object result = SLDParser.decodeSLD(sld);
        assertTrue(result instanceof Map);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertEquals("Alice", data.get("name"));
        assertEquals("30", data.get("age"));
    }

    @Test
    public void testDecodeMultipleRecords() {
        String sld = "name[Alice~name[Bob~";
        Object result = SLDParser.decodeSLD(sld);
        assertTrue(result instanceof List);
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> data = (List<Map<String, Object>>) result;
        assertEquals(2, data.size());
        assertEquals("Alice", data.get(0).get("name"));
        assertEquals("Bob", data.get(1).get("name"));
    }

    @Test
    public void testDecodeArray() {
        String sld = "tags{admin,user";
        Object result = SLDParser.decodeSLD(sld);
        assertTrue(result instanceof Map);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        @SuppressWarnings("unchecked")
        List<String> tags = (List<String>) data.get("tags");
        assertEquals(Arrays.asList("admin", "user"), tags);
    }

    @Test
    public void testDecodeBooleanTrue() {
        String sld = "verified[^1";
        Object result = SLDParser.decodeSLD(sld);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertEquals(true, data.get("verified"));
    }

    @Test
    public void testDecodeBooleanFalse() {
        String sld = "active[^0";
        Object result = SLDParser.decodeSLD(sld);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertEquals(false, data.get("active"));
    }

    // MLD Encoding Tests
    @Test
    public void testMLDSingleRecord() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("name", "Alice");
        data.put("age", 30);
        String mld = SLDParser.encodeMLD(data);
        assertTrue(mld.contains("name[Alice"));
        assertTrue(mld.contains("age[30"));
    }

    @Test
    public void testMLDMultipleRecords() {
        List<Map<String, Object>> data = new ArrayList<>();
        Map<String, Object> record1 = new LinkedHashMap<>();
        record1.put("name", "Alice");
        Map<String, Object> record2 = new LinkedHashMap<>();
        record2.put("name", "Bob");
        data.add(record1);
        data.add(record2);
        String mld = SLDParser.encodeMLD(data);
        assertTrue(mld.contains("\n"));
        String[] lines = mld.split("\n");
        assertEquals(2, lines.length);
    }

    // MLD Decoding Tests
    @Test
    public void testDecodeMLDSingleRecord() {
        String mld = "name[Alice;age[30";
        Object result = SLDParser.decodeMLD(mld);
        assertTrue(result instanceof Map);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertEquals("Alice", data.get("name"));
        assertEquals("30", data.get("age"));
    }

    @Test
    public void testDecodeMLDMultipleRecords() {
        String mld = "name[Alice\nname[Bob";
        Object result = SLDParser.decodeMLD(mld);
        assertTrue(result instanceof List);
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> data = (List<Map<String, Object>>) result;
        assertEquals(2, data.size());
    }

    // Format Conversion Tests
    @Test
    public void testSLDToMLD() {
        String sld = "name[Alice~name[Bob~";
        String mld = SLDParser.sldToMLD(sld);
        assertFalse(mld.contains("~"));
        assertTrue(mld.contains("\n"));
    }

    @Test
    public void testMLDToSLD() {
        String mld = "name[Alice\nname[Bob";
        String sld = SLDParser.mldToSLD(mld);
        assertFalse(sld.contains("\n"));
        assertTrue(sld.contains("~"));
    }

    @Test
    public void testRoundTripSLDMLDSLD() {
        String original = "name[Alice;age[30~name[Bob;age[25~";
        String mld = SLDParser.sldToMLD(original);
        String backToSLD = SLDParser.mldToSLD(mld);
        assertEquals(original, backToSLD);
    }

    @Test
    public void testRoundTripMLDSLDMLD() {
        String original = "name[Alice;age[30\nname[Bob;age[25";
        String sld = SLDParser.mldToSLD(original);
        String backToMLD = SLDParser.sldToMLD(sld);
        assertEquals(original, backToMLD);
    }

    // Edge Case Tests
    @Test
    public void testEmptyStringSLD() {
        Object result = SLDParser.decodeSLD("");
        assertTrue(result instanceof Map);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertTrue(data.isEmpty());
    }

    @Test
    public void testEmptyStringMLD() {
        Object result = SLDParser.decodeMLD("");
        assertTrue(result instanceof Map);
        @SuppressWarnings("unchecked")
        Map<String, Object> data = (Map<String, Object>) result;
        assertTrue(data.isEmpty());
    }

    @Test
    public void testEmptyObjectEncoding() {
        Map<String, Object> data = new LinkedHashMap<>();
        String sld = SLDParser.encodeSLD(data);
        assertEquals("", sld);
    }

    @Test
    public void testSpecialCharactersPreserved() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("path", "C:\\Users\\Alice");
        String sld = SLDParser.encodeSLD(data);
        Object result = SLDParser.decodeSLD(sld);
        @SuppressWarnings("unchecked")
        Map<String, Object> decoded = (Map<String, Object>) result;
        assertEquals("C:\\Users\\Alice", decoded.get("path"));
    }

    // Complex Data Test
    @Test
    public void testMixedTypes() {
        Map<String, Object> data = new LinkedHashMap<>();
        data.put("name", "Alice");
        data.put("age", 30);
        data.put("verified", true);
        data.put("tags", Arrays.asList("admin", "user"));
        data.put("middle", null);
        String sld = SLDParser.encodeSLD(data);
        Object result = SLDParser.decodeSLD(sld);
        @SuppressWarnings("unchecked")
        Map<String, Object> decoded = (Map<String, Object>) result;
        assertEquals("Alice", decoded.get("name"));
        assertEquals(true, decoded.get("verified"));
        @SuppressWarnings("unchecked")
        List<String> tags = (List<String>) decoded.get("tags");
        assertEquals(Arrays.asList("admin", "user"), tags);
    }
}
