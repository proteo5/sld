<?php

namespace SLD\Tests;

use PHPUnit\Framework\TestCase;
use SLD\Parser;

class EscapingTest extends TestCase
{
    public function testEscapeSemicolon(): void
    {
        $this->assertEquals('a^;b', Parser::escapeValue('a;b'));
    }

    public function testEscapeTilde(): void
    {
        $this->assertEquals('a^~b', Parser::escapeValue('a~b'));
    }

    public function testEscapeBracket(): void
    {
        $this->assertEquals('a^[b', Parser::escapeValue('a[b'));
    }

    public function testEscapeBrace(): void
    {
        $this->assertEquals('a^{b', Parser::escapeValue('a{b'));
    }

    public function testEscapeCaret(): void
    {
        $this->assertEquals('a^^b', Parser::escapeValue('a^b'));
    }

    public function testUnescapeSemicolon(): void
    {
        $this->assertEquals('a;b', Parser::unescapeValue('a^;b'));
    }

    public function testUnescapeMultiple(): void
    {
        $this->assertEquals('a;b~c', Parser::unescapeValue('a^;b^~c'));
    }
}

class SLDEncodingTest extends TestCase
{
    public function testSingleRecord(): void
    {
        $data = ['name' => 'Alice', 'age' => 30];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('name[Alice', $sld);
        $this->assertStringContainsString('age[30', $sld);
    }

    public function testMultipleRecords(): void
    {
        $data = [
            ['name' => 'Alice'],
            ['name' => 'Bob']
        ];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('~', $sld);
        $count = substr_count($sld, '~');
        $this->assertGreaterThanOrEqual(2, $count);
    }

    public function testArrayEncoding(): void
    {
        $data = ['tags' => ['admin', 'user']];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('tags{admin,user', $sld);
    }

    public function testBooleanTrue(): void
    {
        $data = ['verified' => true];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('verified[^1', $sld);
    }

    public function testBooleanFalse(): void
    {
        $data = ['active' => false];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('active[^0', $sld);
    }

    public function testNullValue(): void
    {
        $data = ['middle' => null];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('middle[', $sld);
    }

    public function testEscapedCharacters(): void
    {
        $data = ['note' => 'Price: $5;99'];
        $sld = Parser::encodeSLD($data);
        $this->assertStringContainsString('note[Price: $5^;99', $sld);
    }
}

class SLDDecodingTest extends TestCase
{
    public function testSingleRecord(): void
    {
        $sld = 'name[Alice;age[30';
        $data = Parser::decodeSLD($sld);
        $this->assertIsArray($data);
        $this->assertEquals('Alice', $data['name']);
        $this->assertEquals('30', $data['age']);
    }

    public function testMultipleRecords(): void
    {
        $sld = 'name[Alice~name[Bob~';
        $data = Parser::decodeSLD($sld);
        $this->assertIsArray($data);
        $this->assertCount(2, $data);
        $this->assertEquals('Alice', $data[0]['name']);
        $this->assertEquals('Bob', $data[1]['name']);
    }

    public function testArrayDecoding(): void
    {
        $sld = 'tags{admin,user';
        $data = Parser::decodeSLD($sld);
        $this->assertIsArray($data);
        $this->assertIsArray($data['tags']);
        $this->assertEquals(['admin', 'user'], $data['tags']);
    }

    public function testBooleanTrue(): void
    {
        $sld = 'verified[^1';
        $data = Parser::decodeSLD($sld);
        $this->assertIsArray($data);
        $this->assertTrue($data['verified']);
    }

    public function testBooleanFalse(): void
    {
        $sld = 'active[^0';
        $data = Parser::decodeSLD($sld);
        $this->assertIsArray($data);
        $this->assertFalse($data['active']);
    }
}

class MLDEncodingTest extends TestCase
{
    public function testSingleRecord(): void
    {
        $data = ['name' => 'Alice', 'age' => 30];
        $mld = Parser::encodeMLD($data);
        $this->assertStringContainsString('name[Alice', $mld);
        $this->assertStringContainsString('age[30', $mld);
    }

    public function testMultipleRecords(): void
    {
        $data = [
            ['name' => 'Alice'],
            ['name' => 'Bob']
        ];
        $mld = Parser::encodeMLD($data);
        $this->assertStringContainsString("\n", $mld);
        $lines = explode("\n", $mld);
        $this->assertCount(2, $lines);
    }
}

class MLDDecodingTest extends TestCase
{
    public function testSingleRecord(): void
    {
        $mld = 'name[Alice;age[30';
        $data = Parser::decodeMLD($mld);
        $this->assertIsArray($data);
        $this->assertEquals('Alice', $data['name']);
        $this->assertEquals('30', $data['age']);
    }

    public function testMultipleRecords(): void
    {
        $mld = "name[Alice\nname[Bob";
        $data = Parser::decodeMLD($mld);
        $this->assertIsArray($data);
        $this->assertCount(2, $data);
    }
}

class FormatConversionTest extends TestCase
{
    public function testSLDToMLD(): void
    {
        $sld = 'name[Alice~name[Bob~';
        $mld = Parser::sldToMLD($sld);
        $this->assertStringNotContainsString('~', $mld);
        $this->assertStringContainsString("\n", $mld);
    }

    public function testMLDToSLD(): void
    {
        $mld = "name[Alice\nname[Bob";
        $sld = Parser::mldToSLD($mld);
        $this->assertStringNotContainsString("\n", $sld);
        $this->assertStringContainsString('~', $sld);
    }

    public function testRoundTripSLDMLDSLD(): void
    {
        $original = 'name[Alice;age[30~name[Bob;age[25~';
        $mld = Parser::sldToMLD($original);
        $backToSLD = Parser::mldToSLD($mld);
        $this->assertEquals($original, $backToSLD);
    }

    public function testRoundTripMLDSLDMLD(): void
    {
        $original = "name[Alice;age[30\nname[Bob;age[25";
        $sld = Parser::mldToSLD($original);
        $backToMLD = Parser::sldToMLD($sld);
        $this->assertEquals($original, $backToMLD);
    }
}

class EdgeCaseTest extends TestCase
{
    public function testEmptyStringSLD(): void
    {
        $data = Parser::decodeSLD('');
        $this->assertIsArray($data);
        $this->assertEmpty($data);
    }

    public function testEmptyStringMLD(): void
    {
        $data = Parser::decodeMLD('');
        $this->assertIsArray($data);
        $this->assertEmpty($data);
    }

    public function testEmptyObjectEncoding(): void
    {
        $data = [];
        $sld = Parser::encodeSLD($data);
        $this->assertEquals('', $sld);
    }

    public function testSpecialCharactersPreserved(): void
    {
        $data = ['path' => 'C:\\Users\\Alice'];
        $sld = Parser::encodeSLD($data);
        $decoded = Parser::decodeSLD($sld);
        $this->assertEquals('C:\\Users\\Alice', $decoded['path']);
    }
}

class ComplexDataTest extends TestCase
{
    public function testMixedTypes(): void
    {
        $data = [
            'name' => 'Alice',
            'age' => 30,
            'verified' => true,
            'tags' => ['admin', 'user'],
            'middle' => null
        ];
        $sld = Parser::encodeSLD($data);
        $decoded = Parser::decodeSLD($sld);
        $this->assertEquals('Alice', $decoded['name']);
        $this->assertTrue($decoded['verified']);
        $this->assertEquals(['admin', 'user'], $decoded['tags']);
    }
}
