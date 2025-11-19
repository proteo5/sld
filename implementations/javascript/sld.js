/**
 * Copyright 2025 Alfredo Pinto Molina
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * SLD/MLD (Single/Multi Line Data) Format - JavaScript Implementation v2.0
 * A token-efficient data serialization format
 *
 * Breaking changes from v1.0:
 * - Field separator changed from | to ; (semicolon)
 * - Array marker changed to { (curly brace)
 * - Added MLD format support (records separated by newlines)
 */

// Constants
const FIELD_SEPARATOR = ';';
const RECORD_SEPARATOR_SLD = '~';
const RECORD_SEPARATOR_MLD = '\n';
const PROPERTY_MARKER = '[';
const ARRAY_MARKER = '{';
const ESCAPE_CHAR = '^';

/**
 * Escape special SLD/MLD characters in a string
 * @param {string|any} text - The text to escape
 * @returns {string} Escaped text safe for SLD/MLD format
 */
function escapeValue(text) {
    if (text === null || text === undefined) {
        return '';
    }

    const str = String(text);
    return str
        .replace(/\^/g, '^^')
        .replace(/;/g, '^;')
        .replace(/~/g, '^~')
        .replace(/\[/g, '^[')
        .replace(/\{/g, '^{');
}

/**
 * Unescape SLD/MLD escape sequences
 * @param {string} text - The escaped text
 * @returns {string|boolean} Unescaped original text or boolean
 */
function unescapeValue(text) {
    const result = [];
    let i = 0;

    while (i < text.length) {
        if (text[i] === ESCAPE_CHAR && i + 1 < text.length) {
            const nextChar = text[i + 1];
            if (nextChar === '1') {
                return true;  // Boolean true
            } else if (nextChar === '0') {
                return false; // Boolean false
            } else {
                result.push(nextChar);
            }
            i += 2;
        } else {
            result.push(text[i]);
            i += 1;
        }
    }

    return result.join('');
}

/**
 * Split text by delimiter, respecting escape sequences
 * @param {string} text - The text to split
 * @param {string} delimiter - The delimiter character
 * @returns {Array<string>} List of split parts
 */
function splitUnescaped(text, delimiter) {
    const parts = [];
    const current = [];
    let i = 0;

    while (i < text.length) {
        if (text[i] === ESCAPE_CHAR && i + 1 < text.length) {
            current.push(text.slice(i, i + 2));
            i += 2;
        } else if (text[i] === delimiter) {
            parts.push(current.join(''));
            current.length = 0;
            i += 1;
        } else {
            current.push(text[i]);
            i += 1;
        }
    }

    if (current.length > 0 || text.endsWith(delimiter)) {
        parts.push(current.join(''));
    }

    return parts;
}

/**
 * Encode a single record (object) to SLD/MLD format
 * @param {Object} record - Object to encode
 * @returns {string} Encoded string for the record
 */
function encodeRecord(record) {
    const parts = [];

    for (const [key, value] of Object.entries(record)) {
        const escapedKey = escapeValue(key);

        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            // Nested object - not fully implemented yet
            const nested = encodeRecord(value);
            parts.push(`${escapedKey}${PROPERTY_MARKER}${nested}`);
        } else if (Array.isArray(value)) {
            // Array using { marker
            const nestedItems = value.map(item => escapeValue(item));
            parts.push(`${escapedKey}${ARRAY_MARKER}${nestedItems.join(',')}`);
        } else if (typeof value === 'boolean') {
            // Boolean as ^1 or ^0
            const boolVal = value ? '^1' : '^0';
            parts.push(`${escapedKey}${PROPERTY_MARKER}${boolVal}`);
        } else if (value === null || value === undefined) {
            // Null value as ^_
            parts.push(`${escapedKey}${PROPERTY_MARKER}^_`);
        } else {
            // Regular value
            const escapedValue = escapeValue(value);
            parts.push(`${escapedKey}${PROPERTY_MARKER}${escapedValue}`);
        }
    }

    return parts.join(FIELD_SEPARATOR);
}

/**
 * Encode data to SLD format
 * @param {Object|Array|any} data - Data to encode
 * @returns {string} SLD-formatted string (single line with ~ separators)
 */
function encodeSLD(data) {
    if (Array.isArray(data)) {
        const records = data.map(record => encodeRecord(record));
        return records.join(RECORD_SEPARATOR_SLD) + RECORD_SEPARATOR_SLD;
    } else if (typeof data === 'object' && data !== null) {
        return encodeRecord(data);
    } else {
        return escapeValue(data);
    }
}

/**
 * Encode data to MLD format
 * @param {Object|Array|any} data - Data to encode
 * @returns {string} MLD-formatted string (one record per line)
 */
function encodeMLD(data) {
    if (Array.isArray(data)) {
        const records = data.map(record => encodeRecord(record));
        return records.join(RECORD_SEPARATOR_MLD);
    } else if (typeof data === 'object' && data !== null) {
        return encodeRecord(data);
    } else {
        return escapeValue(data);
    }
}

/**
 * Decode a single record string
 * @param {string} recordStr - Single record string
 * @returns {Object} Decoded object
 */
function decodeRecord(recordStr) {
    const record = {};
    const fields = splitUnescaped(recordStr, FIELD_SEPARATOR);

    for (const field of fields) {
        if (!field) continue;

        // Check for property marker
        if (field.includes(PROPERTY_MARKER) && !field.includes(ESCAPE_CHAR + PROPERTY_MARKER)) {
            const parts = field.split(PROPERTY_MARKER, 2);
            const key = unescapeValue(parts[0]);
            const value = parts.length > 1 ? unescapeValue(parts[1]) : '';

            // Handle null (^_)
            if (value === '^_') {
                record[key] = null;
            } else {
                record[key] = value;
            }
        }
        // Check for array marker
        else if (field.includes(ARRAY_MARKER) && !field.includes(ESCAPE_CHAR + ARRAY_MARKER)) {
            const parts = field.split(ARRAY_MARKER, 2);
            const key = unescapeValue(parts[0]);
            if (parts.length > 1) {
                const items = parts[1].split(',').map(item => unescapeValue(item));
                record[key] = items;
            } else {
                record[key] = [];
            }
        }
    }

    return record;
}

/**
 * Decode SLD format string to JavaScript objects
 * @param {string} sldString - SLD-formatted string
 * @returns {Object|Array<Object>} Decoded data
 */
function decodeSLD(sldString) {
    if (!sldString) {
        return {};
    }

    // Remove trailing ~ if present
    sldString = sldString.replace(/~+$/, '');

    const records = [];

    for (const recordStr of splitUnescaped(sldString, RECORD_SEPARATOR_SLD)) {
        if (!recordStr) continue;
        records.push(decodeRecord(recordStr));
    }

    return records.length > 1 ? records : (records[0] || {});
}

/**
 * Decode MLD format string to JavaScript objects
 * @param {string} mldString - MLD-formatted string
 * @returns {Object|Array<Object>} Decoded data
 */
function decodeMLD(mldString) {
    if (!mldString) {
        return {};
    }

    const records = [];

    for (const line of mldString.split(RECORD_SEPARATOR_MLD)) {
        if (!line.trim()) continue;
        records.push(decodeRecord(line));
    }

    return records.length > 1 ? records : (records[0] || {});
}

/**
 * Convert SLD format to MLD format
 * @param {string} sldString - SLD-formatted string
 * @returns {string} MLD-formatted string
 */
function sldToMLD(sldString) {
    return sldString.replace(/~+$/, '').replace(/~/g, '\n');
}

/**
 * Convert MLD format to SLD format
 * @param {string} mldString - MLD-formatted string
 * @returns {string} SLD-formatted string
 */
function mldToSLD(mldString) {
    return mldString.replace(/\n/g, '~') + '~';
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        encodeSLD,
        decodeSLD,
        encodeMLD,
        decodeMLD,
        sldToMLD,
        mldToSLD,
        escapeValue,
        unescapeValue
    };
}

// Example usage
if (typeof require !== 'undefined' && require.main === module) {
    console.log('=== SLD/MLD JavaScript Implementation v2.0 ===\n');

    // Example 1: Simple records with SLD
    console.log('Example 1: Simple user data (SLD)');
    const data1 = [
        { name: 'Alice', age: 30, city: 'New York' },
        { name: 'Bob', age: 25, city: 'Los Angeles' }
    ];
    const sld1 = encodeSLD(data1);
    console.log('Encoded SLD:', sld1);
    console.log('Decoded:', decodeSLD(sld1), '\n');

    // Example 2: Same data with MLD
    console.log('Example 2: Same data (MLD)');
    const mld1 = encodeMLD(data1);
    console.log('Encoded MLD:\n', mld1);
    console.log('Decoded:', decodeMLD(mld1), '\n');

    // Example 3: Arrays
    console.log('Example 3: Products with tags (arrays)');
    const data3 = [
        { sku: 'LAP001', name: 'UltraBook Pro', tags: ['business', 'ultrabook'] },
        { sku: 'MOU001', name: 'Wireless Mouse', tags: ['wireless', 'ergonomic'] }
    ];
    const sld3 = encodeSLD(data3);
    console.log('Encoded SLD:', sld3);
    console.log('Decoded:', decodeSLD(sld3), '\n');

    // Example 4: Booleans
    console.log('Example 4: Boolean values');
    const data4 = { name: 'Alice', verified: true, active: false };
    const sld4 = encodeSLD(data4);
    console.log('Encoded SLD:', sld4);
    console.log('Decoded:', decodeSLD(sld4), '\n');

    // Example 5: Conversion SLD ↔ MLD
    console.log('Example 5: Format conversion');
    const sld5 = 'name[Alice;age[30~name[Bob;age[25~';
    const mld5 = sldToMLD(sld5);
    console.log('SLD:', sld5);
    console.log('MLD:\n', mld5);
    console.log('Back to SLD:', mldToSLD(mld5), '\n');

    // Example 6: Escaped characters
    console.log('Example 6: Escaped characters');
    const data6 = { note: 'Price: $5;99', path: 'C:\\Users' };
    const sld6 = encodeSLD(data6);
    console.log('Encoded:', sld6);
    console.log('Decoded:', decodeSLD(sld6));
}
