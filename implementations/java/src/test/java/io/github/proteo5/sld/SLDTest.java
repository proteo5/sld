package io.github.proteo5.sld;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.*;

public class SLDTest {
    @Test public void testEscapeSemicolon() { assertEquals("a^;b", SLDParser.escapeValue("a;b")); }
    @Test public void testEscapeTilde() { assertEquals("a^~b", SLDParser.escapeValue("a~b")); }
    @Test public void testEscapeBracket() { assertEquals("a^[b", SLDParser.escapeValue("a[b")); }
    @Test public void testEscapeBrace() { assertEquals("a^{b", SLDParser.escapeValue("a{b")); }
    @Test public void testEscapeCaret() { assertEquals("a^^b", SLDParser.escapeValue("a^b")); }
    @Test public void testUnescapeSemicolon() { assertEquals("a;b", SLDParser.unescapeValue("a^;b")); }
    @Test public void testUnescapeMultiple() { assertEquals("a;b~c", SLDParser.unescapeValue("a^;b^~c")); }

    @Test public void testSingleRecord() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("name","Alice"); data.put("age",30);
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("name[Alice")); assertTrue(sld.contains("age[30"));
    }

    @Test public void testMultipleRecords() {
        List<Map<String,Object>> data = new ArrayList<>();
        Map<String,Object> r1 = new LinkedHashMap<>(); r1.put("name","Alice");
        Map<String,Object> r2 = new LinkedHashMap<>(); r2.put("name","Bob");
        data.add(r1); data.add(r2);
        String sld = SLDParser.encodeSLD(data);
        int count = sld.length() - sld.replace("~",""").length();
        assertTrue(count >= 2);
    }

    @Test public void testArrayEncoding() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("tags", Arrays.asList("admin","user"));
        String sld = SLDParser.encodeSLD(data);
        assertTrue(sld.contains("tags{admin,user"));
    }

    @Test public void testBooleanTrue() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("verified", true);
        String sld = SLDParser.encodeSLD(data); assertTrue(sld.contains("verified[^1"));
    }

    @Test public void testBooleanFalse() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("active", false);
        String sld = SLDParser.encodeSLD(data); assertTrue(sld.contains("active[^0"));
    }

    @Test public void testNullValue() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("middle", null);
        String sld = SLDParser.encodeSLD(data); assertTrue(sld.contains("middle["));
    }

    @Test public void testEscapedCharacters() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("note","Price: $5;99");
        String sld = SLDParser.encodeSLD(data); assertTrue(sld.contains("note[Price: $5^;99"));
    }

    @Test public void testDecodeSingleRecord() {
        Object result = SLDParser.decodeSLD("name[Alice;age[30");
        assertTrue(result instanceof Map); Map<?,?> m = (Map<?,?>) result;
        assertEquals("Alice", m.get("name")); assertEquals("30", m.get("age"));
    }

    @Test public void testDecodeMultipleRecords() {
        Object result = SLDParser.decodeSLD("name[Alice~name[Bob~");
        assertTrue(result instanceof List); List<?> list = (List<?>) result; assertEquals(2, list.size());
    }

    @Test public void testDecodeArray() {
        Object result = SLDParser.decodeSLD("tags{admin,user");
        Map<?,?> m = (Map<?,?>) result; @SuppressWarnings("unchecked") List<String> tags = (List<String>) m.get("tags");
        assertEquals(Arrays.asList("admin","user"), tags);
    }

    @Test public void testDecodeBooleanTrue() {
        Map<?,?> m = (Map<?,?>) SLDParser.decodeSLD("verified[^1"); assertEquals(true, m.get("verified"));
    }

    @Test public void testDecodeBooleanFalse() {
        Map<?,?> m = (Map<?,?>) SLDParser.decodeSLD("active[^0"); assertEquals(false, m.get("active"));
    }

    @Test public void testMLDSingleRecord() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("name","Alice"); data.put("age",30);
        String mld = SLDParser.encodeMLD(data); assertTrue(mld.contains("name[Alice")); assertTrue(mld.contains("age[30"));
    }

    @Test public void testMLDMultipleRecords() {
        List<Map<String,Object>> data = new ArrayList<>();
        Map<String,Object> r1 = new LinkedHashMap<>(); r1.put("name","Alice");
        Map<String,Object> r2 = new LinkedHashMap<>(); r2.put("name","Bob");
        data.add(r1); data.add(r2); String mld = SLDParser.encodeMLD(data);
        assertTrue(mld.contains("\n")); assertEquals(2, mld.split("\n").length);
    }

    @Test public void testDecodeMLDSingleRecord() {
        Map<?,?> m = (Map<?,?>) SLDParser.decodeMLD("name[Alice;age[30");
        assertEquals("Alice", m.get("name")); assertEquals("30", m.get("age"));
    }

    @Test public void testDecodeMLDMultipleRecords() {
        Object result = SLDParser.decodeMLD("name[Alice\nname[Bob");
        assertTrue(result instanceof List); List<?> list = (List<?>) result; assertEquals(2, list.size());
    }

    @Test public void testSLDToMLD() { String mld = SLDParser.sldToMLD("name[Alice~name[Bob~"); assertFalse(mld.contains("~")); assertTrue(mld.contains("\n")); }
    @Test public void testMLDToSLD() { String sld = SLDParser.mldToSLD("name[Alice\nname[Bob"); assertFalse(sld.contains("\n")); assertTrue(sld.contains("~")); }

    @Test public void testRoundTripSLDMLDSLD() {
        String original = "name[Alice;age[30~name[Bob;age[25~";
        String mld = SLDParser.sldToMLD(original); String back = SLDParser.mldToSLD(mld);
        assertEquals(original, back);
    }

    @Test public void testRoundTripMLDSLDMLD() {
        String original = "name[Alice;age[30\nname[Bob;age[25";
        String sld = SLDParser.mldToSLD(original); String back = SLDParser.sldToMLD(sld);
        assertEquals(original, back);
    }

    @Test public void testEmptyStringSLD() { Map<?,?> m = (Map<?,?>) SLDParser.decodeSLD(""); assertTrue(m.isEmpty()); }
    @Test public void testEmptyStringMLD() { Map<?,?> m = (Map<?,?>) SLDParser.decodeMLD(""); assertTrue(m.isEmpty()); }
    @Test public void testEmptyObjectEncoding() { String sld = SLDParser.encodeSLD(new LinkedHashMap<>()); assertEquals("", sld); }
    @Test public void testSpecialCharactersPreserved() {
        Map<String,Object> data = new LinkedHashMap<>(); data.put("path","C:\\Users\\Alice");
        String sld = SLDParser.encodeSLD(data); Map<?,?> m = (Map<?,?>) SLDParser.decodeSLD(sld);
        assertEquals("C:\\Users\\Alice", m.get("path"));
    }

    @Test public void testMixedTypes() {
        Map<String,Object> data = new LinkedHashMap<>();
        data.put("name","Alice"); data.put("age",30); data.put("verified",true); data.put("tags", Arrays.asList("admin","user")); data.put("middle", null);
        Map<?,?> m = (Map<?,?>) SLDParser.decodeSLD(SLDParser.encodeSLD(data));
        assertEquals("Alice", m.get("name")); assertEquals(true, m.get("verified"));
        @SuppressWarnings("unchecked") List<String> tags = (List<String>) m.get("tags"); assertEquals(Arrays.asList("admin","user"), tags);
    }
}
