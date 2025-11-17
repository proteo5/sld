<?php
/**
 * SLD (Single Line Data) Format - PHP Implementation
 * A token-efficient data serialization format
 */

class SLD {
    /**
     * Escape special SLD characters in a string
     * 
     * @param mixed $text The text to escape
     * @return string Escaped text safe for SLD format
     */
    public static function escape($text) {
        if ($text === null) {
            return '';
        }
        
        $str = (string)$text;
        return str_replace(
            ['^', '|', '~', '['],
            ['^^', '^|', '^~', '^['],
            $str
        );
    }
    
    /**
     * Unescape SLD escape sequences
     * 
     * @param string $text The escaped text
     * @return string Unescaped original text
     */
    public static function unescape($text) {
        $result = '';
        $i = 0;
        $len = strlen($text);
        
        while ($i < $len) {
            if ($text[$i] === '^' && $i + 1 < $len) {
                $result .= $text[$i + 1];
                $i += 2;
            } else {
                $result .= $text[$i];
                $i += 1;
            }
        }
        
        return $result;
    }
    
    /**
     * Split text by delimiter, respecting escape sequences
     * 
     * @param string $text The text to split
     * @param string $delimiter The delimiter character
     * @return array List of split parts
     */
    public static function splitUnescaped($text, $delimiter) {
        $parts = [];
        $current = '';
        $i = 0;
        $len = strlen($text);
        
        while ($i < $len) {
            if ($text[$i] === '^' && $i + 1 < $len) {
                $current .= substr($text, $i, 2);
                $i += 2;
            } elseif ($text[$i] === $delimiter) {
                $parts[] = $current;
                $current = '';
                $i += 1;
            } else {
                $current .= $text[$i];
                $i += 1;
            }
        }
        
        if (strlen($current) > 0 || substr($text, -1) === $delimiter) {
            $parts[] = $current;
        }
        
        return $parts;
    }
    
    /**
     * Encode a single record (array) to SLD format
     * 
     * @param array $record Array to encode
     * @return string SLD-formatted string for the record
     */
    public static function encodeRecord($record) {
        $parts = [];
        
        foreach ($record as $key => $value) {
            $escapedKey = self::escape($key);
            
            if (is_array($value) && self::isAssoc($value)) {
                $nested = self::encodeRecord($value);
                $parts[] = "{$escapedKey}[{$nested}";
            } elseif (is_array($value)) {
                $nestedItems = array_map(function($item) {
                    return is_array($item) ? self::encodeRecord($item) : self::escape($item);
                }, $value);
                $parts[] = "{$escapedKey}[" . implode('~', $nestedItems);
            } elseif ($value === null) {
                $parts[] = "{$escapedKey}|";
            } else {
                $escapedValue = self::escape($value);
                $parts[] = "{$escapedKey}|{$escapedValue}";
            }
        }
        
        return implode('|', $parts);
    }
    
    /**
     * Check if array is associative
     * 
     * @param array $arr Array to check
     * @return bool True if associative
     */
    private static function isAssoc($arr) {
        if (!is_array($arr) || empty($arr)) {
            return false;
        }
        return array_keys($arr) !== range(0, count($arr) - 1);
    }
    
    /**
     * Encode data to SLD format
     * 
     * @param mixed $data Data to encode
     * @return string SLD-formatted string
     */
    public static function encode($data) {
        if (is_array($data) && !self::isAssoc($data)) {
            return implode('~', array_map([self::class, 'encodeRecord'], $data));
        } elseif (is_array($data)) {
            return self::encodeRecord($data);
        } else {
            return self::escape($data);
        }
    }
    
    /**
     * Decode SLD format string to PHP arrays
     * 
     * @param string $sldString SLD-formatted string
     * @return array|mixed Decoded data
     */
    public static function decode($sldString) {
        if (empty($sldString)) {
            return [];
        }
        
        $records = [];
        
        foreach (self::splitUnescaped($sldString, '~') as $recordStr) {
            if (empty($recordStr)) {
                continue;
            }
            
            $record = [];
            $fields = self::splitUnescaped($recordStr, '|');
            
            $i = 0;
            while ($i < count($fields)) {
                if ($i >= count($fields)) {
                    break;
                }
                
                $key = self::unescape($fields[$i]);
                
                // Check if this is a nested structure
                if (strpos($fields[$i], '[') !== false && strpos($fields[$i], '^[') === false) {
                    $key = str_replace('[', '', $key);
                    if ($i + 1 < count($fields)) {
                        $nestedValue = self::unescape($fields[$i + 1]);
                        $record[$key] = $nestedValue;
                        $i += 2;
                    } else {
                        $i += 1;
                    }
                } else {
                    if ($i + 1 < count($fields)) {
                        $value = self::unescape($fields[$i + 1]);
                        $record[$key] = ($value !== '') ? $value : null;
                        $i += 2;
                    } else {
                        $record[$key] = null;
                        $i += 1;
                    }
                }
            }
            
            $records[] = $record;
        }
        
        return count($records) > 1 ? $records : (isset($records[0]) ? $records[0] : []);
    }
}

// Example usage
if (php_sapi_name() === 'cli') {
    echo "=== SLD PHP Implementation ===\n\n";
    
    // Example 1: Simple records
    echo "Example 1: Simple product data\n";
    $data1 = [
        ['name' => 'Laptop', 'price' => '3999.90'],
        ['name' => 'Mouse', 'price' => '149.90'],
        ['name' => 'Headset', 'price' => '499.00']
    ];
    $sld1 = SLD::encode($data1);
    echo "Encoded: {$sld1}\n";
    echo "Decoded: " . print_r(SLD::decode($sld1), true) . "\n";
    
    // Example 2: Objects with IDs
    echo "Example 2: User records\n";
    $data2 = [
        ['id' => '1', 'name' => 'John', 'lastname' => 'Smith'],
        ['id' => '2', 'name' => 'Juan', 'lastname' => 'Perez']
    ];
    $sld2 = SLD::encode($data2);
    echo "Encoded: {$sld2}\n";
    echo "Decoded: " . print_r(SLD::decode($sld2), true) . "\n";
    
    // Example 3: Data with special characters
    echo "Example 3: Escaped characters\n";
    $data3 = [
        ['company' => 'Pipe|Works Inc'],
        ['product' => 'Model~XZ~2000']
    ];
    $sld3 = SLD::encode($data3);
    echo "Encoded: {$sld3}\n";
    echo "Decoded: " . print_r(SLD::decode($sld3), true) . "\n";
    
    // Example 4: Null values
    echo "Example 4: Null/empty values\n";
    $data4 = ['name' => 'John', 'middle' => null, 'lastname' => 'Doe'];
    $sld4 = SLD::encode($data4);
    echo "Encoded: {$sld4}\n";
    echo "Decoded: " . print_r(SLD::decode($sld4), true) . "\n";
}
?>
