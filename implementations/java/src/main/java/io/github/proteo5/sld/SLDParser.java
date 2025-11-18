package io.github.proteo5.sld;

import java.util.*;

/**
 * SLD/MLD (Single/Multi Line Data) Format - Java Implementation v1.1
 * A token-efficient data serialization format
 *
 * Changes in v1.1:
 * - Field separator changed from | to ; (semicolon)
 * - Added MLD format support (records separated by newlines)
 * - Array marker changed to { (curly brace)
 * - Property marker remains [ (square bracket)
 */
public class SLDParser {
    // Constants
    private static final char FIELD_SEPARATOR = ';';
    private static final char RECORD_SEPARATOR_SLD = '~';
    private static final char RECORD_SEPARATOR_MLD = '\n';
    private static final char PROPERTY_MARKER = '[';
    private static final char ARRAY_MARKER = '{';
    private static final char ESCAPE_CHAR = '^';

    public static String escapeValue(String text) {
        if (text == null || text.isEmpty()) return "";
        return text
            .replace("^", "^^")
            .replace(";", "^;")
            .replace("~", "^~")
            .replace("[", "^[")
            .replace("{", "^{");
    }

    public static Object unescapeValue(String text) {
        StringBuilder result = new StringBuilder();
        int i = 0;
        while (i < text.length()) {
            if (text.charAt(i) == ESCAPE_CHAR && i + 1 < text.length()) {
                char nextChar = text.charAt(i + 1);
                if (nextChar == '1') return true;
                else if (nextChar == '0') return false;
                else result.append(nextChar);
                i += 2;
            } else {
                result.append(text.charAt(i));
                i++;
            }
        }
        return result.toString();
    }

    private static List<String> splitUnescaped(String text, char delimiter) {
        List<String> parts = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        int i = 0;
        while (i < text.length()) {
            if (text.charAt(i) == ESCAPE_CHAR && i + 1 < text.length()) {
                current.append(text, i, i + 2);
                i += 2;
            } else if (text.charAt(i) == delimiter) {
                parts.add(current.toString());
                current.setLength(0);
                i++;
            } else {
                current.append(text.charAt(i));
                i++;
            }
        }
        if (current.length() > 0 || text.endsWith(String.valueOf(delimiter))) parts.add(current.toString());
        return parts;
    }

    private static String encodeRecord(Map<String, Object> record) {
        List<String> parts = new ArrayList<>();
        for (Map.Entry<String, Object> entry : record.entrySet()) {
            String escapedKey = escapeValue(entry.getKey());
            Object value = entry.getValue();
            if (value instanceof Map) {
                @SuppressWarnings("unchecked")
                String nested = encodeRecord((Map<String, Object>) value);
                parts.add(escapedKey + PROPERTY_MARKER + nested);
            } else if (value instanceof List) {
                @SuppressWarnings("unchecked")
                List<Object> list = (List<Object>) value;
                List<String> nestedItems = new ArrayList<>();
                for (Object item : list) nestedItems.add(escapeValue(String.valueOf(item)));
                parts.add(escapedKey + ARRAY_MARKER + String.join(",", nestedItems));
            } else if (value instanceof Boolean) {
                parts.add(escapedKey + PROPERTY_MARKER + (((Boolean) value) ? "^1" : "^0"));
            } else if (value == null) {
                parts.add(escapedKey + PROPERTY_MARKER);
            } else {
                parts.add(escapedKey + PROPERTY_MARKER + escapeValue(String.valueOf(value)));
            }
        }
        return String.join(String.valueOf(FIELD_SEPARATOR), parts);
    }

    public static String encodeSLD(List<Map<String, Object>> data) {
        List<String> records = new ArrayList<>();
        for (Map<String, Object> rec : data) records.add(encodeRecord(rec));
        return String.join(String.valueOf(RECORD_SEPARATOR_SLD), records) + RECORD_SEPARATOR_SLD;
    }

    public static String encodeSLD(Map<String, Object> data) { return encodeRecord(data); }

    public static String encodeMLD(List<Map<String, Object>> data) {
        List<String> records = new ArrayList<>();
        for (Map<String, Object> rec : data) records.add(encodeRecord(rec));
        return String.join(String.valueOf(RECORD_SEPARATOR_MLD), records);
    }

    public static String encodeMLD(Map<String, Object> data) { return encodeRecord(data); }

    private static Map<String, Object> decodeRecord(String recordStr) {
        Map<String, Object> record = new LinkedHashMap<>();
        List<String> fields = splitUnescaped(recordStr, FIELD_SEPARATOR);
        for (String field : fields) {
            if (field.isEmpty()) continue;
            if (field.contains(String.valueOf(PROPERTY_MARKER)) && !field.contains(ESCAPE_CHAR + String.valueOf(PROPERTY_MARKER))) {
                String[] parts = field.split("\\" + PROPERTY_MARKER, 2);
                String key = unescapeValue(parts[0]).toString();
                Object value = parts.length > 1 ? unescapeValue(parts[1]) : null;
                record.put(key, value);
            } else if (field.contains(String.valueOf(ARRAY_MARKER)) && !field.contains(ESCAPE_CHAR + String.valueOf(ARRAY_MARKER))) {
                String[] parts = field.split("\\" + ARRAY_MARKER, 2);
                String key = unescapeValue(parts[0]).toString();
                if (parts.length > 1) {
                    List<Object> items = new ArrayList<>();
                    for (String item : parts[1].split(",")) items.add(unescapeValue(item));
                    record.put(key, items);
                } else {
                    record.put(key, new ArrayList<>());
                }
            }
        }
        return record;
    }

    public static Object decodeSLD(String sldString) {
        if (sldString == null || sldString.isEmpty()) return new LinkedHashMap<String, Object>();
        sldString = sldString.replaceAll("~+$", "");
        List<Map<String, Object>> records = new ArrayList<>();
        for (String rec : splitUnescaped(sldString, RECORD_SEPARATOR_SLD)) if (!rec.isEmpty()) records.add(decodeRecord(rec));
        return records.size() > 1 ? records : (records.size() == 1 ? records.get(0) : new LinkedHashMap<String, Object>());
    }

    public static Object decodeMLD(String mldString) {
        if (mldString == null || mldString.isEmpty()) return new LinkedHashMap<String, Object>();
        List<Map<String, Object>> records = new ArrayList<>();
        for (String line : mldString.split("\n")) { String trimmed = line.trim(); if (!trimmed.isEmpty()) records.add(decodeRecord(trimmed)); }
        return records.size() > 1 ? records : (records.size() == 1 ? records.get(0) : new LinkedHashMap<String, Object>());
    }

    public static String sldToMLD(String sldString) { return sldString.replaceAll("~+$", "").replace('~', '\n'); }
    public static String mldToSLD(String mldString) { return mldString.replace('\n', '~') + '~'; }
}
