using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SLD
{
    /// <summary>
    /// SLD (Single Line Data) Format - C# Implementation
    /// A token-efficient data serialization format
    /// </summary>
    public static class SLDFormat
    {
        /// <summary>
        /// Escape special SLD characters in a string
        /// </summary>
        public static string Escape(string text)
        {
            if (text == null)
                return string.Empty;

            return text
                .Replace("^", "^^")
                .Replace("|", "^|")
                .Replace("~", "^~")
                .Replace("[", "^[");
        }

        /// <summary>
        /// Unescape SLD escape sequences
        /// </summary>
        public static string Unescape(string text)
        {
            var result = new StringBuilder();
            int i = 0;

            while (i < text.Length)
            {
                if (text[i] == '^' && i + 1 < text.Length)
                {
                    result.Append(text[i + 1]);
                    i += 2;
                }
                else
                {
                    result.Append(text[i]);
                    i += 1;
                }
            }

            return result.ToString();
        }

        /// <summary>
        /// Split text by delimiter, respecting escape sequences
        /// </summary>
        public static List<string> SplitUnescaped(string text, char delimiter)
        {
            var parts = new List<string>();
            var current = new StringBuilder();
            int i = 0;

            while (i < text.Length)
            {
                if (text[i] == '^' && i + 1 < text.Length)
                {
                    current.Append(text.Substring(i, 2));
                    i += 2;
                }
                else if (text[i] == delimiter)
                {
                    parts.Add(current.ToString());
                    current.Clear();
                    i += 1;
                }
                else
                {
                    current.Append(text[i]);
                    i += 1;
                }
            }

            if (current.Length > 0 || text.EndsWith(delimiter.ToString()))
            {
                parts.Add(current.ToString());
            }

            return parts;
        }

        /// <summary>
        /// Encode a dictionary to SLD format
        /// </summary>
        public static string EncodeRecord(Dictionary<string, object> record)
        {
            var parts = new List<string>();

            foreach (var kvp in record)
            {
                var escapedKey = Escape(kvp.Key);

                if (kvp.Value == null)
                {
                    parts.Add($"{escapedKey}|");
                }
                else if (kvp.Value is Dictionary<string, object> dict)
                {
                    var nested = EncodeRecord(dict);
                    parts.Add($"{escapedKey}[{nested}");
                }
                else if (kvp.Value is List<object> list)
                {
                    var nestedItems = list.Select(item =>
                        item is Dictionary<string, object> d
                            ? EncodeRecord(d)
                            : Escape(item?.ToString() ?? string.Empty)
                    );
                    parts.Add($"{escapedKey}[{string.Join("~", nestedItems)}");
                }
                else
                {
                    var escapedValue = Escape(kvp.Value.ToString());
                    parts.Add($"{escapedKey}|{escapedValue}");
                }
            }

            return string.Join("|", parts);
        }

        /// <summary>
        /// Encode data to SLD format
        /// </summary>
        public static string Encode(object data)
        {
            if (data is List<Dictionary<string, object>> list)
            {
                return string.Join("~", list.Select(EncodeRecord));
            }
            else if (data is Dictionary<string, object> dict)
            {
                return EncodeRecord(dict);
            }
            else
            {
                return Escape(data?.ToString() ?? string.Empty);
            }
        }

        /// <summary>
        /// Decode SLD format string to dictionaries
        /// </summary>
        public static object Decode(string sldString)
        {
            if (string.IsNullOrEmpty(sldString))
                return new Dictionary<string, object>();

            var records = new List<Dictionary<string, object>>();

            foreach (var recordStr in SplitUnescaped(sldString, '~'))
            {
                if (string.IsNullOrEmpty(recordStr))
                    continue;

                var record = new Dictionary<string, object>();
                var fields = SplitUnescaped(recordStr, '|');

                int i = 0;
                while (i < fields.Count)
                {
                    if (i >= fields.Count)
                        break;

                    var key = Unescape(fields[i]);

                    // Check if this is a nested structure
                    if (fields[i].Contains("[") && !fields[i].Contains("^["))
                    {
                        key = key.Replace("[", "");
                        if (i + 1 < fields.Count)
                        {
                            var nestedValue = Unescape(fields[i + 1]);
                            record[key] = nestedValue;
                            i += 2;
                        }
                        else
                        {
                            i += 1;
                        }
                    }
                    else
                    {
                        if (i + 1 < fields.Count)
                        {
                            var value = Unescape(fields[i + 1]);
                            record[key] = string.IsNullOrEmpty(value) ? null : value;
                            i += 2;
                        }
                        else
                        {
                            record[key] = null;
                            i += 1;
                        }
                    }
                }

                records.Add(record);
            }

            return records.Count > 1 ? (object)records : (records.FirstOrDefault() ?? new Dictionary<string, object>());
        }
    }

    /// <summary>
    /// Example usage of SLD format
    /// </summary>
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== SLD C# Implementation ===\n");

            // Example 1: Simple records
            Console.WriteLine("Example 1: Simple product data");
            var data1 = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { { "name", "Laptop" }, { "price", "3999.90" } },
                new Dictionary<string, object> { { "name", "Mouse" }, { "price", "149.90" } },
                new Dictionary<string, object> { { "name", "Headset" }, { "price", "499.00" } }
            };
            var sld1 = SLDFormat.Encode(data1);
            Console.WriteLine($"Encoded: {sld1}");
            Console.WriteLine($"Decoded: {SLDFormat.Decode(sld1)}\n");

            // Example 2: Objects with IDs
            Console.WriteLine("Example 2: User records");
            var data2 = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { { "id", "1" }, { "name", "John" }, { "lastname", "Smith" } },
                new Dictionary<string, object> { { "id", "2" }, { "name", "Juan" }, { "lastname", "Perez" } }
            };
            var sld2 = SLDFormat.Encode(data2);
            Console.WriteLine($"Encoded: {sld2}");
            Console.WriteLine($"Decoded: {SLDFormat.Decode(sld2)}\n");

            // Example 3: Data with special characters
            Console.WriteLine("Example 3: Escaped characters");
            var data3 = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { { "company", "Pipe|Works Inc" } },
                new Dictionary<string, object> { { "product", "Model~XZ~2000" } }
            };
            var sld3 = SLDFormat.Encode(data3);
            Console.WriteLine($"Encoded: {sld3}");
            Console.WriteLine($"Decoded: {SLDFormat.Decode(sld3)}\n");

            // Example 4: Null values
            Console.WriteLine("Example 4: Null/empty values");
            var data4 = new Dictionary<string, object>
            {
                { "name", "John" },
                { "middle", null },
                { "lastname", "Doe" }
            };
            var sld4 = SLDFormat.Encode(data4);
            Console.WriteLine($"Encoded: {sld4}");
            Console.WriteLine($"Decoded: {SLDFormat.Decode(sld4)}");
        }
    }
}
