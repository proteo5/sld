/**
 * SLD (Single Line Data) Format - JavaScript Implementation
 * A token-efficient data serialization format
 */

/**
 * Escape special SLD characters in a string
 * @param {string|any} text - The text to escape
 * @returns {string} Escaped text safe for SLD format
 */
function escape(text) {
    if (text === null || text === undefined) {
        return '';
    }
    
    const str = String(text);
    return str
        .replace(/\^/g, '^^')
        .replace(/\|/g, '^|')
        .replace(/~/g, '^~')
        .replace(/\[/g, '^[');
}

/**
 * Unescape SLD escape sequences
 * @param {string} text - The escaped text
 * @returns {string} Unescaped original text
 */
function unescape(text) {
    const result = [];
    let i = 0;
    
    while (i < text.length) {
        if (text[i] === '^' && i + 1 < text.length) {
            result.push(text[i + 1]);
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
        if (text[i] === '^' && i + 1 < text.length) {
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
 * Encode a single record (object) to SLD format
 * @param {Object} record - Object to encode
 * @returns {string} SLD-formatted string for the record
 */
function encodeRecord(record) {
    const parts = [];
    
    for (const [key, value] of Object.entries(record)) {
        const escapedKey = escape(key);
        
        if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
            const nested = encodeRecord(value);
            parts.push(`${escapedKey}[${nested}`);
        } else if (Array.isArray(value)) {
            const nestedItems = value.map(item => 
                typeof item === 'object' ? encodeRecord(item) : escape(item)
            );
            parts.push(`${escapedKey}[${nestedItems.join('~')}`);
        } else if (value === null || value === undefined) {
            parts.push(`${escapedKey}|`);
        } else {
            const escapedValue = escape(value);
            parts.push(`${escapedKey}|${escapedValue}`);
        }
    }
    
    return parts.join('|');
}

/**
 * Encode data to SLD format
 * @param {Object|Array|any} data - Data to encode
 * @returns {string} SLD-formatted string
 */
function encode(data) {
    if (Array.isArray(data)) {
        return data.map(record => encodeRecord(record)).join('~');
    } else if (typeof data === 'object' && data !== null) {
        return encodeRecord(data);
    } else {
        return escape(data);
    }
}

/**
 * Decode SLD format string to JavaScript objects
 * @param {string} sldString - SLD-formatted string
 * @returns {Object|Array<Object>} Decoded data
 */
function decode(sldString) {
    if (!sldString) {
        return {};
    }
    
    const records = [];
    
    for (const recordStr of splitUnescaped(sldString, '~')) {
        if (!recordStr) continue;
        
        const record = {};
        const fields = splitUnescaped(recordStr, '|');
        
        let i = 0;
        while (i < fields.length) {
            if (i >= fields.length) break;
            
            let key = unescape(fields[i]);
            
            // Check if this is a nested structure
            if (fields[i].includes('[') && !fields[i].includes('^[')) {
                key = key.replace('[', '');
                if (i + 1 < fields.length) {
                    const nestedValue = unescape(fields[i + 1]);
                    record[key] = nestedValue;
                    i += 2;
                } else {
                    i += 1;
                }
            } else {
                if (i + 1 < fields.length) {
                    const value = unescape(fields[i + 1]);
                    record[key] = value !== '' ? value : null;
                    i += 2;
                } else {
                    record[key] = null;
                    i += 1;
                }
            }
        }
        
        records.push(record);
    }
    
    return records.length > 1 ? records : (records[0] || {});
}

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { encode, decode, escape, unescape };
}

// Example usage
if (typeof require !== 'undefined' && require.main === module) {
    console.log('=== SLD JavaScript Implementation ===\n');
    
    // Example 1: Simple records
    console.log('Example 1: Simple product data');
    const data1 = [
        { name: 'Laptop', price: '3999.90' },
        { name: 'Mouse', price: '149.90' },
        { name: 'Headset', price: '499.00' }
    ];
    const sld1 = encode(data1);
    console.log('Encoded:', sld1);
    console.log('Decoded:', decode(sld1), '\n');
    
    // Example 2: Objects with IDs
    console.log('Example 2: User records');
    const data2 = [
        { id: '1', name: 'John', lastname: 'Smith' },
        { id: '2', name: 'Juan', lastname: 'Perez' }
    ];
    const sld2 = encode(data2);
    console.log('Encoded:', sld2);
    console.log('Decoded:', decode(sld2), '\n');
    
    // Example 3: Data with special characters
    console.log('Example 3: Escaped characters');
    const data3 = [
        { company: 'Pipe|Works Inc' },
        { product: 'Model~XZ~2000' }
    ];
    const sld3 = encode(data3);
    console.log('Encoded:', sld3);
    console.log('Decoded:', decode(sld3), '\n');
    
    // Example 4: Null values
    console.log('Example 4: Null/empty values');
    const data4 = { name: 'John', middle: null, lastname: 'Doe' };
    const sld4 = encode(data4);
    console.log('Encoded:', sld4);
    console.log('Decoded:', decode(sld4));
}
