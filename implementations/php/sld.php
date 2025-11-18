<?php
/**
 * SLD/MLD (Single/Multi Line Data) Format - PHP Implementation v1.1
 * A token-efficient data serialization format
 * 
 * Changes in v1.1:
 * - Field separator changed from | to ; (semicolon)
 * - Added MLD format support (records separated by newlines)
 * - Array marker changed to { (curly brace)
 * - Property marker remains [ (square bracket)
 */

namespace SLD;

class Parser
{
    // Constants
    const FIELD_SEPARATOR = ';';
    const RECORD_SEPARATOR_SLD = '~';
    const RECORD_SEPARATOR_MLD = "\n";
    const PROPERTY_MARKER = '[';
    const ARRAY_MARKER = '{';
    const ESCAPE_CHAR = '^';

    /**
     * Escape special SLD/MLD characters
     */
    public static function escapeValue($text)
    {
        if ($text === null || $text === '') {
            return '';
        }

        $text = (string)$text;
        return str_replace(
            ['^', ';', '~', '[', '{'],
            ['^^', '^;', '^~', '^[', '^{'],
            $text
        );
    }

    /**
     * Unescape SLD/MLD escape sequences
     */
    public static function unescapeValue($text)
    {
        $result = '';
        $i = 0;
        $len = strlen($text);

        while ($i < $len) {
            if ($text[$i] === self::ESCAPE_CHAR && $i + 1 < $len) {
                $nextChar = $text[$i + 1];
                if ($nextChar === '1') {
                    return true; // Boolean true
                } elseif ($nextChar === '0') {
                    return false; // Boolean false
                } else {
                    $result .= $nextChar;
                }
                $i += 2;
            } else {
                $result .= $text[$i];
                $i++;
            }
        }

        return $result;
    }

    /**
     * Split text by delimiter, respecting escape sequences
     */
    private static function splitUnescaped($text, $delimiter)
    {
        $parts = [];
        $current = '';
        $i = 0;
        $len = strlen($text);

        while ($i < $len) {
            if ($text[$i] === self::ESCAPE_CHAR && $i + 1 < $len) {
                $current .= substr($text, $i, 2);
                $i += 2;
            } elseif ($text[$i] === $delimiter) {
                $parts[] = $current;
                $current = '';
                $i++;
            } else {
                $current .= $text[$i];
                $i++;
            }
        }

        if ($current !== '' || substr($text, -1) === $delimiter) {
            $parts[] = $current;
        }

        return $parts;
    }

    /**
     * Encode record to string
     */
    private static function encodeRecord($record)
    {
        $parts = [];

        foreach ($record as $key => $value) {
            $escapedKey = self::escapeValue($key);

            if (is_array($value) && array_keys($value) !== range(0, count($value) - 1)) {
                // Associative array (object)
                $nested = self::encodeRecord($value);
                $parts[] = $escapedKey . self::PROPERTY_MARKER . $nested;
            } elseif (is_array($value)) {
                // Indexed array
                $nestedItems = array_map([self::class, 'escapeValue'], $value);
                $parts[] = $escapedKey . self::ARRAY_MARKER . implode(',', $nestedItems);
            } elseif (is_bool($value)) {
                // Boolean
                $boolVal = $value ? '^1' : '^0';
                $parts[] = $escapedKey . self::PROPERTY_MARKER . $boolVal;
            } elseif ($value === null) {
                // Null
                $parts[] = $escapedKey . self::PROPERTY_MARKER;
            } else {
                // Regular value
                $escapedValue = self::escapeValue($value);
                $parts[] = $escapedKey . self::PROPERTY_MARKER . $escapedValue;
            }
        }

        return implode(self::FIELD_SEPARATOR, $parts);
    }

    /**
     * Encode data to SLD format
     */
    public static function encodeSLD($data)
    {
        if (is_array($data) && isset($data[0]) && is_array($data[0])) {
            // Array of records
            $records = array_map([self::class, 'encodeRecord'], $data);
            return implode(self::RECORD_SEPARATOR_SLD, $records) . self::RECORD_SEPARATOR_SLD;
        } elseif (is_array($data)) {
            // Single record
            return self::encodeRecord($data);
        } else {
            return self::escapeValue($data);
        }
    }

    /**
     * Encode data to MLD format
     */
    public static function encodeMLD($data)
    {
        if (is_array($data) && isset($data[0]) && is_array($data[0])) {
            // Array of records
            $records = array_map([self::class, 'encodeRecord'], $data);
            return implode(self::RECORD_SEPARATOR_MLD, $records);
        } elseif (is_array($data)) {
            // Single record
            return self::encodeRecord($data);
        } else {
            return self::escapeValue($data);
        }
    }

    /**
     * Decode record string
     */
    private static function decodeRecord($recordStr)
    {
        $record = [];
        $fields = self::splitUnescaped($recordStr, self::FIELD_SEPARATOR);

        foreach ($fields as $field) {
            if (empty($field)) {
                continue;
            }

            // Check for property marker
            if (strpos($field, self::PROPERTY_MARKER) !== false && 
                strpos($field, self::ESCAPE_CHAR . self::PROPERTY_MARKER) === false) {
                $parts = explode(self::PROPERTY_MARKER, $field, 2);
                $key = self::unescapeValue($parts[0]);
                $value = isset($parts[1]) ? self::unescapeValue($parts[1]) : null;
                $record[$key] = $value;
            }
            // Check for array marker
            elseif (strpos($field, self::ARRAY_MARKER) !== false && 
                    strpos($field, self::ESCAPE_CHAR . self::ARRAY_MARKER) === false) {
                $parts = explode(self::ARRAY_MARKER, $field, 2);
                $key = self::unescapeValue($parts[0]);
                if (isset($parts[1])) {
                    $items = array_map([self::class, 'unescapeValue'], explode(',', $parts[1]));
                    $record[$key] = $items;
                } else {
                    $record[$key] = [];
                }
            }
        }

        return $record;
    }

    /**
     * Decode SLD format string
     */
    public static function decodeSLD($sldString)
    {
        if (empty($sldString)) {
            return [];
        }

        $sldString = rtrim($sldString, self::RECORD_SEPARATOR_SLD);
        $records = [];

        foreach (self::splitUnescaped($sldString, self::RECORD_SEPARATOR_SLD) as $recordStr) {
            if (!empty($recordStr)) {
                $records[] = self::decodeRecord($recordStr);
            }
        }

        return count($records) > 1 ? $records : (count($records) == 1 ? $records[0] : []);
    }

    /**
     * Decode MLD format string
     */
    public static function decodeMLD($mldString)
    {
        if (empty($mldString)) {
            return [];
        }

        $records = [];

        foreach (explode(self::RECORD_SEPARATOR_MLD, $mldString) as $line) {
            $trimmed = trim($line);
            if (!empty($trimmed)) {
                $records[] = self::decodeRecord($trimmed);
            }
        }

        return count($records) > 1 ? $records : (count($records) == 1 ? $records[0] : []);
    }

    /**
     * Convert SLD to MLD
     */
    public static function sldToMLD($sldString)
    {
        return str_replace(self::RECORD_SEPARATOR_SLD, self::RECORD_SEPARATOR_MLD, rtrim($sldString, self::RECORD_SEPARATOR_SLD));
    }

    /**
     * Convert MLD to SLD
     */
    public static function mldToSLD($mldString)
    {
        return str_replace(self::RECORD_SEPARATOR_MLD, self::RECORD_SEPARATOR_SLD, $mldString) . self::RECORD_SEPARATOR_SLD;
    }
}

// Example usage
if (php_sapi_name() === 'cli') {
    echo "=== SLD/MLD PHP Implementation v1.1 ===\n\n";

    // Example 1: Simple records with SLD
    echo "Example 1: Simple user data (SLD)\n";
    $data1 = [
        ['name' => 'Alice', 'age' => 30, 'city' => 'New York'],
        ['name' => 'Bob', 'age' => 25, 'city' => 'Los Angeles']
    ];
    $sld1 = Parser::encodeSLD($data1);
    echo "Encoded SLD: $sld1\n";
    print_r(Parser::decodeSLD($sld1));
    echo "\n";

    // Example 2: Booleans
    echo "Example 2: Boolean values\n";
    $data2 = ['name' => 'Alice', 'verified' => true, 'active' => false];
    $sld2 = Parser::encodeSLD($data2);
    echo "Encoded SLD: $sld2\n";
    print_r(Parser::decodeSLD($sld2));
    echo "\n";

    // Example 3: Format conversion
    echo "Example 3: Format conversion\n";
    $sld3 = "name[Alice;age[30~name[Bob;age[25~";
    $mld3 = Parser::sldToMLD($sld3);
    echo "SLD: $sld3\n";
    echo "MLD:\n$mld3\n";
    echo "Back to SLD: " . Parser::mldToSLD($mld3) . "\n";
}
