package io.github.proteo5.sld;

import java.util.*;

/**
 * SLD/MLD (Single/Multi Line Data) Format - Java Implementation v2.0
 * A token-efficient data serialization format
 *
 * Changes in v2.0:
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

    /**
     * Escape special SLD/MLD characters
     */
    public static String escapeValue(String text) {
        if (text == null || text.isEmpty()) {
            return "";
        }

        return text
            .replace("^", "^^")
            .replace(";", "^;")
            .replace("~", "^~")
            .replace("[", "^[")
            .replace("{", "^{");
    }

    /**
     * Unescape SLD/MLD escape sequences
     */
    public static Object unescapeValue(String text) {
        StringBuilder result = new StringBuilder();
        int i = 0;

        while (i < text.length()) {
            if (text.charAt(i) == ESCAPE_CHAR && i + 1 < text.length()) {
                char nextChar = text.charAt(i + 1);
                if (nextChar == '1') {
                    return true; // Boolean true
                } else if (nextChar == '0') {
                    return false; // Boolean false
                } else {
                    result.append(nextChar);
                }
                i += 2;
            } else {
                result.append(text.charAt(i));
                i++;
            }
        }

        return result.toString();
    }

    /**
     * Split text by delimiter, respecting escape sequences
     */
    private static List<String> splitUnescaped(String text, char delimiter) {
        List<String> parts = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        int i = 0;

        while (i < text.length()) {
            if (text.charAt(i) == ESCAPE_CHAR && i + 1 < text.length()) {
                current.append(text.substring(i, i + 2));
                i += 2;
            } else if (text.charAt(i) == delimiter) {
                parts.add(current.toString());
                current = new StringBuilder();
                i++;
            } else {
                current.append(text.charAt(i));
                i++;
            }
        }

        if (current.length() > 0 || text.endsWith(String.valueOf(delimiter))) {
            parts.add(current.toString());
        }

        return parts;
    }

    /**
     * Encode record to string
     */
    private static String encodeRecord(Map<String, Object> record) {
        List<String> parts = new ArrayList<>();

        for (Map.Entry<String, Object> entry : record.entrySet()) {
            String escapedKey = escapeValue(entry.getKey());
            Object value = entry.getValue();

            if (value instanceof Map) {
                // Nested object
                @SuppressWarnings("unchecked")
                String nested = encodeRecord((Map<String, Object>) value);
                parts.add(escapedKey + PROPERTY_MARKER + nested);
            } else if (value instanceof List) {
                // Array
                @SuppressWarnings("unchecked")
                List<Object> list = (List<Object>) value;
                List<String> nestedItems = new ArrayList<>();
                for (Object item : list) {
                    nestedItems.add(escapeValue(item.toString()));
                }
                parts.add(escapedKey + ARRAY_MARKER + String.join(",", nestedItems));
            } else if (value instanceof Boolean) {
                // Boolean
                String boolVal = (Boolean) value ? "^1" : "^0";
                parts.add(escapedKey + PROPERTY_MARKER + boolVal);
            } else if (value == null) {
                // Null as ^_
                parts.add(escapedKey + PROPERTY_MARKER + "^_");
            } else {
                // Regular value
                String escapedValue = escapeValue(value.toString());
                parts.add(escapedKey + PROPERTY_MARKER + escapedValue);
            }
        }

        return String.join(String.valueOf(FIELD_SEPARATOR), parts);
    }

    /**
     * Encode data to SLD format
     */
    public static String encodeSLD(List<Map<String, Object>> data) {
        List<String> records = new ArrayList<>();
        for (Map<String, Object> record : data) {
            records.add(encodeRecord(record));
        }
        return String.join(String.valueOf(RECORD_SEPARATOR_SLD), records) + RECORD_SEPARATOR_SLD;
    }

    /**
     * Encode single record to SLD format
     */
    public static String encodeSLD(Map<String, Object> data) {
        return encodeRecord(data);
    }

    /**
     * Encode data to MLD format
     */
    public static String encodeMLD(List<Map<String, Object>> data) {
        List<String> records = new ArrayList<>();
        for (Map<String, Object> record : data) {
            records.add(encodeRecord(record));
        }
        return String.join(String.valueOf(RECORD_SEPARATOR_MLD), records);
    }

    /**
     * Encode single record to MLD format
     */
    public static String encodeMLD(Map<String, Object> data) {
        return encodeRecord(data);
    }

    /**
     * Decode record string
     */
    private static Map<String, Object> decodeRecord(String recordStr) {
        Map<String, Object> record = new LinkedHashMap<>();
        List<String> fields = splitUnescaped(recordStr, FIELD_SEPARATOR);

        for (String field : fields) {
            if (field.isEmpty()) {
                continue;
            }

            // Check for property marker
            if (field.contains(String.valueOf(PROPERTY_MARKER)) && 
                !field.contains(ESCAPE_CHAR + String.valueOf(PROPERTY_MARKER))) {
                String[] parts = field.split("\\\\" + PROPERTY_MARKER, 2);
                String key = unescapeValue(parts[0]).toString();
                String value = parts.length > 1 ? unescapeValue(parts[1]).toString() : "";
                
                // Handle null (^_)
                if ("^_".equals(value)) {
                    record.put(key, null);
                } else {
                    record.put(key, value);
                }
            }
            // Check for array marker
            else if (field.contains(String.valueOf(ARRAY_MARKER)) && 
                     !field.contains(ESCAPE_CHAR + String.valueOf(ARRAY_MARKER))) {
                String[] parts = field.split("\\" + ARRAY_MARKER, 2);
                String key = unescapeValue(parts[0]).toString();
                if (parts.length > 1) {
                    List<Object> items = new ArrayList<>();
                    for (String item : parts[1].split(",")) {
                        items.add(unescapeValue(item));
                    }
                    record.put(key, items);
                } else {
                    record.put(key, new ArrayList<>());
                }
            }
        }

        return record;
    }

    /**
     * Decode SLD format string
     */
    public static Object decodeSLD(String sldString) {
        if (sldString == null || sldString.isEmpty()) {
            return new LinkedHashMap<String, Object>();
        }

        sldString = sldString.replaceAll("~+$", "");
        List<Map<String, Object>> records = new ArrayList<>();

        for (String recordStr : splitUnescaped(sldString, RECORD_SEPARATOR_SLD)) {
            if (!recordStr.isEmpty()) {
                records.add(decodeRecord(recordStr));
            }
        }

        return records.size() > 1 ? records : (records.size() == 1 ? records.get(0) : new LinkedHashMap<String, Object>());
    }

    /**
     * Decode MLD format string
     */
    public static Object decodeMLD(String mldString) {
        if (mldString == null || mldString.isEmpty()) {
            return new LinkedHashMap<String, Object>();
        }

        List<Map<String, Object>> records = new ArrayList<>();
        String[] lines = mldString.split("\n");

        for (String line : lines) {
            String trimmed = line.trim();
            if (!trimmed.isEmpty()) {
                records.add(decodeRecord(trimmed));
            }
        }

        return records.size() > 1 ? records : (records.size() == 1 ? records.get(0) : new LinkedHashMap<String, Object>());
    }

    /**
     * Convert SLD to MLD
     */
    public static String sldToMLD(String sldString) {
        return sldString.replaceAll("~+$", "").replace('~', '\n');
    }

    /**
     * Convert MLD to SLD
     */
    public static String mldToSLD(String mldString) {
        return mldString.replace('\n', '~') + '~';
    }

    // Example usage
    public static void main(String[] args) {
        System.out.println("=== SLD/MLD Java Implementation v2.0 ===\n");

        // Example 1: Simple records with SLD
        System.out.println("Example 1: Simple user data (SLD)");
        List<Map<String, Object>> data1 = new ArrayList<>();
        Map<String, Object> user1 = new LinkedHashMap<>();
        user1.put("name", "Alice");
        user1.put("age", 30);
        user1.put("city", "New York");
        Map<String, Object> user2 = new LinkedHashMap<>();
        user2.put("name", "Bob");
        user2.put("age", 25);
        user2.put("city", "Los Angeles");
        data1.add(user1);
        data1.add(user2);

        String sld1 = encodeSLD(data1);
        System.out.println("Encoded SLD: " + sld1);
        System.out.println("Decoded: " + decodeSLD(sld1) + "\n");

        // Example 2: Booleans
        System.out.println("Example 2: Boolean values");
        Map<String, Object> data2 = new LinkedHashMap<>();
        data2.put("name", "Alice");
        data2.put("verified", true);
        data2.put("active", false);

        String sld2 = encodeSLD(data2);
        System.out.println("Encoded SLD: " + sld2);
        System.out.println("Decoded: " + decodeSLD(sld2) + "\n");

        // Example 3: Format conversion
        System.out.println("Example 3: Format conversion");
        String sld3 = "name[Alice;age[30~name[Bob;age[25~";
        String mld3 = sldToMLD(sld3);
        System.out.println("SLD: " + sld3);
        System.out.println("MLD:\n" + mld3);
        System.out.println("Back to SLD: " + mldToSLD(mld3));
    }
}
