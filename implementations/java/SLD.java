import java.util.*;
import java.util.stream.Collectors;

/**
 * SLD (Single Line Data) Format - Java Implementation
 * A token-efficient data serialization format
 */
public class SLD {
    
    /**
     * Escape special SLD characters in a string
     * 
     * @param text The text to escape
     * @return Escaped text safe for SLD format
     */
    public static String escape(String text) {
        if (text == null) {
            return "";
        }
        
        return text
            .replace("^", "^^")
            .replace("|", "^|")
            .replace("~", "^~")
            .replace("[", "^[");
    }
    
    /**
     * Unescape SLD escape sequences
     * 
     * @param text The escaped text
     * @return Unescaped original text
     */
    public static String unescape(String text) {
        StringBuilder result = new StringBuilder();
        int i = 0;
        
        while (i < text.length()) {
            if (text.charAt(i) == '^' && i + 1 < text.length()) {
                result.append(text.charAt(i + 1));
                i += 2;
            } else {
                result.append(text.charAt(i));
                i += 1;
            }
        }
        
        return result.toString();
    }
    
    /**
     * Split text by delimiter, respecting escape sequences
     * 
     * @param text The text to split
     * @param delimiter The delimiter character
     * @return List of split parts
     */
    public static List<String> splitUnescaped(String text, char delimiter) {
        List<String> parts = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        int i = 0;
        
        while (i < text.length()) {
            if (text.charAt(i) == '^' && i + 1 < text.length()) {
                current.append(text, i, i + 2);
                i += 2;
            } else if (text.charAt(i) == delimiter) {
                parts.add(current.toString());
                current = new StringBuilder();
                i += 1;
            } else {
                current.append(text.charAt(i));
                i += 1;
            }
        }
        
        if (current.length() > 0 || text.endsWith(String.valueOf(delimiter))) {
            parts.add(current.toString());
        }
        
        return parts;
    }
    
    /**
     * Encode a single record (Map) to SLD format
     * 
     * @param record Map to encode
     * @return SLD-formatted string for the record
     */
    public static String encodeRecord(Map<String, Object> record) {
        List<String> parts = new ArrayList<>();
        
        for (Map.Entry<String, Object> entry : record.entrySet()) {
            String escapedKey = escape(entry.getKey());
            Object value = entry.getValue();
            
            if (value instanceof Map) {
                @SuppressWarnings("unchecked")
                String nested = encodeRecord((Map<String, Object>) value);
                parts.add(escapedKey + "[" + nested);
            } else if (value instanceof List) {
                @SuppressWarnings("unchecked")
                List<Object> list = (List<Object>) value;
                List<String> nestedItems = list.stream()
                    .map(item -> {
                        if (item instanceof Map) {
                            @SuppressWarnings("unchecked")
                            Map<String, Object> itemMap = (Map<String, Object>) item;
                            return encodeRecord(itemMap);
                        } else {
                            return escape(String.valueOf(item));
                        }
                    })
                    .collect(Collectors.toList());
                parts.add(escapedKey + "[" + String.join("~", nestedItems));
            } else if (value == null) {
                parts.add(escapedKey + "|");
            } else {
                String escapedValue = escape(String.valueOf(value));
                parts.add(escapedKey + "|" + escapedValue);
            }
        }
        
        return String.join("|", parts);
    }
    
    /**
     * Encode data to SLD format
     * 
     * @param data Data to encode (Map or List of Maps)
     * @return SLD-formatted string
     */
    public static String encode(Object data) {
        if (data instanceof List) {
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> list = (List<Map<String, Object>>) data;
            return list.stream()
                .map(SLD::encodeRecord)
                .collect(Collectors.joining("~"));
        } else if (data instanceof Map) {
            @SuppressWarnings("unchecked")
            Map<String, Object> map = (Map<String, Object>) data;
            return encodeRecord(map);
        } else {
            return escape(String.valueOf(data));
        }
    }
    
    /**
     * Decode SLD format string to Maps
     * 
     * @param sldString SLD-formatted string
     * @return Decoded data (Map or List of Maps)
     */
    public static Object decode(String sldString) {
        if (sldString == null || sldString.isEmpty()) {
            return new HashMap<String, Object>();
        }
        
        List<Map<String, Object>> records = new ArrayList<>();
        
        for (String recordStr : splitUnescaped(sldString, '~')) {
            if (recordStr.isEmpty()) {
                continue;
            }
            
            Map<String, Object> record = new HashMap<>();
            List<String> fields = splitUnescaped(recordStr, '|');
            
            int i = 0;
            while (i < fields.size()) {
                if (i >= fields.size()) {
                    break;
                }
                
                String key = unescape(fields.get(i));
                
                // Check if this is a nested structure
                if (fields.get(i).contains("[") && !fields.get(i).contains("^[")) {
                    key = key.replace("[", "");
                    if (i + 1 < fields.size()) {
                        String nestedValue = unescape(fields.get(i + 1));
                        record.put(key, nestedValue);
                        i += 2;
                    } else {
                        i += 1;
                    }
                } else {
                    if (i + 1 < fields.size()) {
                        String value = unescape(fields.get(i + 1));
                        record.put(key, value.isEmpty() ? null : value);
                        i += 2;
                    } else {
                        record.put(key, null);
                        i += 1;
                    }
                }
            }
            
            records.add(record);
        }
        
        return records.size() > 1 ? records : (records.isEmpty() ? new HashMap<String, Object>() : records.get(0));
    }
    
    /**
     * Example usage
     */
    public static void main(String[] args) {
        System.out.println("=== SLD Java Implementation ===\n");
        
        // Example 1: Simple records
        System.out.println("Example 1: Simple product data");
        List<Map<String, Object>> data1 = Arrays.asList(
            new HashMap<String, Object>() {{ put("name", "Laptop"); put("price", "3999.90"); }},
            new HashMap<String, Object>() {{ put("name", "Mouse"); put("price", "149.90"); }},
            new HashMap<String, Object>() {{ put("name", "Headset"); put("price", "499.00"); }}
        );
        String sld1 = encode(data1);
        System.out.println("Encoded: " + sld1);
        System.out.println("Decoded: " + decode(sld1) + "\n");
        
        // Example 2: Objects with IDs
        System.out.println("Example 2: User records");
        List<Map<String, Object>> data2 = Arrays.asList(
            new HashMap<String, Object>() {{ put("id", "1"); put("name", "John"); put("lastname", "Smith"); }},
            new HashMap<String, Object>() {{ put("id", "2"); put("name", "Juan"); put("lastname", "Perez"); }}
        );
        String sld2 = encode(data2);
        System.out.println("Encoded: " + sld2);
        System.out.println("Decoded: " + decode(sld2) + "\n");
        
        // Example 3: Data with special characters
        System.out.println("Example 3: Escaped characters");
        List<Map<String, Object>> data3 = Arrays.asList(
            new HashMap<String, Object>() {{ put("company", "Pipe|Works Inc"); }},
            new HashMap<String, Object>() {{ put("product", "Model~XZ~2000"); }}
        );
        String sld3 = encode(data3);
        System.out.println("Encoded: " + sld3);
        System.out.println("Decoded: " + decode(sld3) + "\n");
        
        // Example 4: Null values
        System.out.println("Example 4: Null/empty values");
        Map<String, Object> data4 = new HashMap<String, Object>() {{
            put("name", "John");
            put("middle", null);
            put("lastname", "Doe");
        }};
        String sld4 = encode(data4);
        System.out.println("Encoded: " + sld4);
        System.out.println("Decoded: " + decode(sld4));
    }
}
