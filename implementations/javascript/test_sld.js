/**
 * Unit tests for SLD/MLD JavaScript Implementation v1.1
 * Run with: node test_sld.js
 */

const {
    encodeSLD, decodeSLD, encodeMLD, decodeMLD,
    sldToMLD, mldToSLD, escapeValue, unescapeValue
} = require('./sld.js');

let passed = 0;
let failed = 0;

function assert(condition, message) {
    if (condition) {
        console.log(`✓ ${message}`);
        passed++;
    } else {
        console.error(`✗ ${message}`);
        failed++;
    }
}

function assertEqual(actual, expected, message) {
    assert(actual === expected, `${message} (expected: ${expected}, got: ${actual})`);
}

function assertArrayEqual(actual, expected, message) {
    const isEqual = JSON.stringify(actual) === JSON.stringify(expected);
    assert(isEqual, `${message} (expected: ${JSON.stringify(expected)}, got: ${JSON.stringify(actual)})`);
}

console.log('\n=== Testing Escaping ===');
assertEqual(escapeValue('a;b'), 'a^;b', 'Escape semicolon');
assertEqual(escapeValue('a~b'), 'a^~b', 'Escape tilde');
assertEqual(escapeValue('a[b'), 'a^[b', 'Escape bracket');
assertEqual(escapeValue('a{b'), 'a^{b', 'Escape brace');
assertEqual(escapeValue('a^b'), 'a^^b', 'Escape caret');
assertEqual(unescapeValue('a^;b'), 'a;b', 'Unescape semicolon');
assertEqual(unescapeValue('a^;b^~c'), 'a;b~c', 'Unescape multiple');

console.log('\n=== Testing SLD Encoding ===');
let data = { name: 'Alice', age: 30 };
let sld = encodeSLD(data);
assert(sld.includes('name[Alice'), 'Single record with name');
assert(sld.includes('age[30'), 'Single record with age');

data = [{ name: 'Alice' }, { name: 'Bob' }];
sld = encodeSLD(data);
assert((sld.match(/~/g) || []).length >= 2, 'Multiple records');

data = { tags: ['admin', 'user'] };
sld = encodeSLD(data);
assert(sld.includes('tags{admin,user'), 'Array encoding');

data = { verified: true };
sld = encodeSLD(data);
assert(sld.includes('verified[^1'), 'Boolean true');

data = { active: false };
sld = encodeSLD(data);
assert(sld.includes('active[^0'), 'Boolean false');

data = { middle: null };
sld = encodeSLD(data);
assert(sld.includes('middle['), 'Null value');

data = { note: 'Price: $5;99' };
sld = encodeSLD(data);
assert(sld.includes('note[Price: $5^;99'), 'Escaped characters');

console.log('\n=== Testing SLD Decoding ===');
sld = 'name[Alice;age[30';
data = decodeSLD(sld);
assertEqual(data.name, 'Alice', 'Decode name');
assertEqual(data.age, '30', 'Decode age');

sld = 'name[Alice~name[Bob~';
data = decodeSLD(sld);
assert(Array.isArray(data), 'Multiple records returns array');
assertEqual(data.length, 2, 'Two records');
assertEqual(data[0].name, 'Alice', 'First record name');
assertEqual(data[1].name, 'Bob', 'Second record name');

sld = 'tags{admin,user';
data = decodeSLD(sld);
assertArrayEqual(data.tags, ['admin', 'user'], 'Array decoding');

sld = 'verified[^1';
data = decodeSLD(sld);
assertEqual(data.verified, true, 'Boolean true decoding');

sld = 'active[^0';
data = decodeSLD(sld);
assertEqual(data.active, false, 'Boolean false decoding');

console.log('\n=== Testing MLD Encoding ===');
data = { name: 'Alice', age: 30 };
let mld = encodeMLD(data);
assert(mld.includes('name[Alice'), 'MLD single record with name');
assert(mld.includes('age[30'), 'MLD single record with age');

data = [{ name: 'Alice' }, { name: 'Bob' }];
mld = encodeMLD(data);
assert(mld.includes('\n'), 'MLD multiple records with newline');
const lines = mld.split('\n');
assertEqual(lines.length, 2, 'MLD two lines');

console.log('\n=== Testing MLD Decoding ===');
mld = 'name[Alice;age[30';
data = decodeMLD(mld);
assertEqual(data.name, 'Alice', 'MLD decode name');
assertEqual(data.age, '30', 'MLD decode age');

mld = 'name[Alice\nname[Bob';
data = decodeMLD(mld);
assert(Array.isArray(data), 'MLD multiple records returns array');
assertEqual(data.length, 2, 'MLD two records');

console.log('\n=== Testing Format Conversion ===');
sld = 'name[Alice~name[Bob~';
mld = sldToMLD(sld);
assert(!mld.includes('~'), 'SLD to MLD removes tildes');
assert(mld.includes('\n'), 'SLD to MLD adds newlines');

mld = 'name[Alice\nname[Bob';
sld = mldToSLD(mld);
assert(!sld.includes('\n'), 'MLD to SLD removes newlines');
assert(sld.includes('~'), 'MLD to SLD adds tildes');

const original_sld = 'name[Alice;age[30~name[Bob;age[25~';
mld = sldToMLD(original_sld);
const back_to_sld = mldToSLD(mld);
assertEqual(back_to_sld, original_sld, 'Round trip SLD->MLD->SLD');

const original_mld = 'name[Alice;age[30\nname[Bob;age[25';
sld = mldToSLD(original_mld);
const back_to_mld = sldToMLD(sld);
assertEqual(back_to_mld, original_mld, 'Round trip MLD->SLD->MLD');

console.log('\n=== Testing Edge Cases ===');
data = decodeSLD('');
assertEqual(JSON.stringify(data), '{}', 'Empty SLD string');

data = decodeMLD('');
assertEqual(JSON.stringify(data), '{}', 'Empty MLD string');

sld = encodeSLD({});
assertEqual(sld, '', 'Empty object encoding');

data = { path: 'C:\\Users\\Alice' };
sld = encodeSLD(data);
const decoded = decodeSLD(sld);
assertEqual(decoded.path, 'C:\\Users\\Alice', 'Special characters preserved');

console.log('\n=== Testing Complex Data ===');
data = {
    name: 'Alice',
    age: 30,
    verified: true,
    tags: ['admin', 'user'],
    middle: null
};
sld = encodeSLD(data);
const decoded_complex = decodeSLD(sld);
assertEqual(decoded_complex.name, 'Alice', 'Complex: name');
assertEqual(decoded_complex.verified, true, 'Complex: boolean');
assertArrayEqual(decoded_complex.tags, ['admin', 'user'], 'Complex: array');

console.log('\n=== Test Summary ===');
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);
console.log(`Total:  ${passed + failed}`);

process.exit(failed > 0 ? 1 : 0);
