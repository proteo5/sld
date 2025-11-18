using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SLD
{
    /// <summary>
    /// SLD/MLD (Single/Multi Line Data) Format - C# Implementation v1.1
    /// A token-efficient data serialization format
    /// 
    /// Changes in v1.1:
    /// - Field separator changed from | to ; (semicolon)
    /// - Added MLD format support (records separated by newlines)
    /// - Array marker changed to { (curly brace)
    /// - Property marker remains [ (square bracket)
    /// </summary>
    public static class SLDParser
    {
        // Constants
        private const char FIELD_SEPARATOR = ';';
        private const char RECORD_SEPARATOR_SLD = '~';
        private const char RECORD_SEPARATOR_MLD = '\n';
        private const char PROPERTY_MARKER = '[';
        private const char ARRAY_MARKER = '{';
        private const char ESCAPE_CHAR = '^';

        /// <summary>
        /// Escape special SLD/MLD characters in a string
        /// </summary>
        public static string EscapeValue(string text)
        {
            if (string.IsNullOrEmpty(text))
                return string.Empty;

            return text
                .Replace("^", "^^")
                .Replace(";", "^;")
                .Replace("~", "^~")
                .Replace("[", "^[")
                .Replace("{", "^{");
        }

        /// <summary>
        /// Unescape SLD/MLD escape sequences
        /// </summary>
        public static object UnescapeValue(string text)
        {
            var result = new StringBuilder();
            int i = 0;

            while (i < text.Length)
            {
                if (text[i] == ESCAPE_CHAR && i + 1 < text.Length)
                {
                    char nextChar = text[i + 1];
                    if (nextChar == '1')
                        return true; // Boolean true
                    else if (nextChar == '0')
                        return false; // Boolean false
                    else
                        result.Append(nextChar);
                    i += 2;
                }
                else
                {
                    result.Append(text[i]);
                    i++;
                }
            }

            return result.ToString();
        }

        /// <summary>
        /// Encode data to SLD format
        /// </summary>
        public static string EncodeSLD(List<Dictionary<string, object>> data)
        {
            var records = data.Select(record => EncodeRecord(record));
            return string.Join(RECORD_SEPARATOR_SLD.ToString(), records) + RECORD_SEPARATOR_SLD;
        }

        /// <summary>
        /// Encode single dictionary to SLD format
        /// </summary>
        public static string EncodeSLD(Dictionary<string, object> data)
        {
            return EncodeRecord(data);
        }

        /// <summary>
        /// Encode data to MLD format
        /// </summary>
        public static string EncodeMLD(List<Dictionary<string, object>> data)
        {
            var records = data.Select(record => EncodeRecord(record));
            return string.Join(RECORD_SEPARATOR_MLD.ToString(), records);
        }

        /// <summary>
        /// Encode single dictionary to MLD format
        /// </summary>
        public static string EncodeMLD(Dictionary<string, object> data)
        {
            return EncodeRecord(data);
        }

        private static string EncodeRecord(Dictionary<string, object> record)
        {
            var parts = new List<string>();

            foreach (var kvp in record)
            {
                string escapedKey = EscapeValue(kvp.Key);
                object value = kvp.Value;

                if (value is Dictionary<string, object> dict)
                {
                    // Nested object
                    string nested = EncodeRecord(dict);
                    parts.Add($"{escapedKey}{PROPERTY_MARKER}{nested}");
                }
                else if (value is List<object> list)
                {
                    // Array using { marker
                    var nestedItems = list.Select(item => EscapeValue(item.ToString()));
                    parts.Add($"{escapedKey}{ARRAY_MARKER}{string.Join(",", nestedItems)}");
                }
                else if (value is bool boolValue)
                {
                    // Boolean as ^1 or ^0
                    string boolVal = boolValue ? "^1" : "^0";
                    parts.Add($"{escapedKey}{PROPERTY_MARKER}{boolVal}");
                }
                else if (value == null)
                {
                    // Null value
                    parts.Add($"{escapedKey}{PROPERTY_MARKER}");
                }
                else
                {
                    // Regular value
                    string escapedValue = EscapeValue(value.ToString());
                    parts.Add($"{escapedKey}{PROPERTY_MARKER}{escapedValue}");
                }
            }

            return string.Join(FIELD_SEPARATOR.ToString(), parts);
        }

        /// <summary>
        /// Decode SLD format string
        /// </summary>
        public static object DecodeSLD(string sldString)
        {
            if (string.IsNullOrEmpty(sldString))
                return new Dictionary<string, object>();

            sldString = sldString.TrimEnd(RECORD_SEPARATOR_SLD);

            var records = new List<Dictionary<string, object>>();
            var recordStrings = SplitUnescaped(sldString, RECORD_SEPARATOR_SLD);

            foreach (var recordStr in recordStrings)
            {
                if (!string.IsNullOrEmpty(recordStr))
                    records.Add(DecodeRecord(recordStr));
            }

            return records.Count > 1 ? (object)records : (records.Count == 1 ? records[0] : new Dictionary<string, object>());
        }

        /// <summary>
        /// Decode MLD format string
        /// </summary>
        public static object DecodeMLD(string mldString)
        {
            if (string.IsNullOrEmpty(mldString))
                return new Dictionary<string, object>();

            var records = new List<Dictionary<string, object>>();
            var lines = mldString.Split(new[] { RECORD_SEPARATOR_MLD }, StringSplitOptions.RemoveEmptyEntries);

            foreach (var line in lines)
            {
                if (!string.IsNullOrWhiteSpace(line))
                    records.Add(DecodeRecord(line));
            }

            return records.Count > 1 ? (object)records : (records.Count == 1 ? records[0] : new Dictionary<string, object>());
        }

        private static Dictionary<string, object> DecodeRecord(string recordStr)
        {
            var record = new Dictionary<string, object>();
            var fields = SplitUnescaped(recordStr, FIELD_SEPARATOR);

            foreach (var field in fields)
            {
                if (string.IsNullOrEmpty(field))
                    continue;

                // Check for property marker
                if (field.Contains(PROPERTY_MARKER) && !field.Contains($"{ESCAPE_CHAR}{PROPERTY_MARKER}"))
                {
                    var parts = field.Split(new[] { PROPERTY_MARKER }, 2);
                    string key = UnescapeValue(parts[0]).ToString();
                    object value = parts.Length > 1 ? UnescapeValue(parts[1]) : null;
                    record[key] = value;
                }
                // Check for array marker
                else if (field.Contains(ARRAY_MARKER) && !field.Contains($"{ESCAPE_CHAR}{ARRAY_MARKER}"))
                {
                    var parts = field.Split(new[] { ARRAY_MARKER }, 2);
                    string key = UnescapeValue(parts[0]).ToString();
                    if (parts.Length > 1)
                    {
                        var items = parts[1].Split(',').Select(item => UnescapeValue(item)).ToList();
                        record[key] = items;
                    }
                    else
                    {
                        record[key] = new List<object>();
                    }
                }
            }

            return record;
        }

        private static List<string> SplitUnescaped(string text, char delimiter)
        {
            var parts = new List<string>();
            var current = new StringBuilder();
            int i = 0;

            while (i < text.Length)
            {
                if (text[i] == ESCAPE_CHAR && i + 1 < text.Length)
                {
                    current.Append(text[i]);
                    current.Append(text[i + 1]);
                    i += 2;
                }
                else if (text[i] == delimiter)
                {
                    parts.Add(current.ToString());
                    current.Clear();
                    i++;
                }
                else
                {
                    current.Append(text[i]);
                    i++;
                }
            }

            if (current.Length > 0 || text.EndsWith(delimiter.ToString()))
            {
                parts.Add(current.ToString());
            }

            return parts;
        }

        /// <summary>
        /// Convert SLD to MLD format
        /// </summary>
        public static string SLDToMLD(string sldString)
        {
            return sldString.TrimEnd(RECORD_SEPARATOR_SLD).Replace(RECORD_SEPARATOR_SLD, RECORD_SEPARATOR_MLD);
        }

        /// <summary>
        /// Convert MLD to SLD format
        /// </summary>
        public static string MLDToSLD(string mldString)
        {
            return mldString.Replace(RECORD_SEPARATOR_MLD, RECORD_SEPARATOR_SLD) + RECORD_SEPARATOR_SLD;
        }
    }

    // Example usage class
    public class Program
    {
        public static void Main(string[] args)
        {
            Console.WriteLine("=== SLD/MLD C# Implementation v1.1 ===\n");

            // Example 1: Simple records with SLD
            Console.WriteLine("Example 1: Simple user data (SLD)");
            var data1 = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { {"name", "Alice"}, {"age", 30}, {"city", "New York"} },
                new Dictionary<string, object> { {"name", "Bob"}, {"age", 25}, {"city", "Los Angeles"} }
            };
            string sld1 = SLDParser.EncodeSLD(data1);
            Console.WriteLine($"Encoded SLD: {sld1}");
            Console.WriteLine($"Decoded: {SLDParser.DecodeSLD(sld1)}\n");

            // Example 2: Booleans
            Console.WriteLine("Example 2: Boolean values");
            var data2 = new Dictionary<string, object>
            {
                {"name", "Alice"},
                {"verified", true},
                {"active", false}
            };
            string sld2 = SLDParser.EncodeSLD(data2);
            Console.WriteLine($"Encoded SLD: {sld2}");
            Console.WriteLine($"Decoded: {SLDParser.DecodeSLD(sld2)}\n");

            // Example 3: Format conversion
            Console.WriteLine("Example 3: Format conversion");
            string sld3 = "name[Alice;age[30~name[Bob;age[25~";
            string mld3 = SLDParser.SLDToMLD(sld3);
            Console.WriteLine($"SLD: {sld3}");
            Console.WriteLine($"MLD:\n{mld3}");
            Console.WriteLine($"Back to SLD: {SLDParser.MLDToSLD(mld3)}");
        }
    }
}
