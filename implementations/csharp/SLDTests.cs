using System;
using System.Collections.Generic;
using Xunit;
using SLD;

namespace SLD.Tests
{
    public class EscapingTests
    {
        [Fact]
        public void TestEscapeSemicolon()
        {
            Assert.Equal("a^;b", SLDParser.EscapeValue("a;b"));
        }

        [Fact]
        public void TestEscapeTilde()
        {
            Assert.Equal("a^~b", SLDParser.EscapeValue("a~b"));
        }

        [Fact]
        public void TestEscapeBracket()
        {
            Assert.Equal("a^[b", SLDParser.EscapeValue("a[b"));
        }

        [Fact]
        public void TestEscapeBrace()
        {
            Assert.Equal("a^{b", SLDParser.EscapeValue("a{b"));
        }

        [Fact]
        public void TestEscapeCaret()
        {
            Assert.Equal("a^^b", SLDParser.EscapeValue("a^b"));
        }

        [Fact]
        public void TestUnescapeSemicolon()
        {
            Assert.Equal("a;b", SLDParser.UnescapeValue("a^;b"));
        }

        [Fact]
        public void TestUnescapeMultiple()
        {
            Assert.Equal("a;b~c", SLDParser.UnescapeValue("a^;b^~c"));
        }
    }

    public class SLDEncodingTests
    {
        [Fact]
        public void TestSingleRecord()
        {
            var data = new Dictionary<string, object>
            {
                { "name", "Alice" },
                { "age", 30 }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("name[Alice", sld);
            Assert.Contains("age[30", sld);
        }

        [Fact]
        public void TestMultipleRecords()
        {
            var data = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { { "name", "Alice" } },
                new Dictionary<string, object> { { "name", "Bob" } }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("~", sld);
            var count = sld.Split('~').Length;
            Assert.True(count >= 2);
        }

        [Fact]
        public void TestArrayEncoding()
        {
            var data = new Dictionary<string, object>
            {
                { "tags", new List<string> { "admin", "user" } }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("tags{admin~user}", sld);
        }

        [Fact]
        public void TestBooleanTrue()
        {
            var data = new Dictionary<string, object>
            {
                { "verified", true }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("verified[^1", sld);
        }

        [Fact]
        public void TestBooleanFalse()
        {
            var data = new Dictionary<string, object>
            {
                { "active", false }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("active[^0", sld);
        }

        [Fact]
        public void TestNullValue()
        {
            var data = new Dictionary<string, object>();
            data["middle"] = null!;
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("middle[", sld);
        }

        [Fact]
        public void TestEscapedCharacters()
        {
            var data = new Dictionary<string, object>
            {
                { "note", "Price: $5;99" }
            };
            var sld = SLDParser.EncodeSLD(data);
            Assert.Contains("note[Price: $5^;99", sld);
        }
    }

    public class SLDDecodingTests
    {
        [Fact]
        public void TestSingleRecord()
        {
            var sld = "name[Alice;age[30";
            var data = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.Equal("Alice", data["name"]);
            Assert.Equal("30", data["age"]);
        }

        [Fact]
        public void TestMultipleRecords()
        {
            var sld = "name[Alice~name[Bob~";
            var data = SLDParser.DecodeSLD(sld) as List<Dictionary<string, object>>;
            Assert.NotNull(data);
            Assert.Equal(2, data.Count);
            Assert.Equal("Alice", data[0]["name"]);
            Assert.Equal("Bob", data[1]["name"]);
        }

        [Fact]
        public void TestArrayDecoding()
        {
            var sld = "tags{admin~user}";
            var data = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(data);
            var tags = data["tags"] as List<object>;
            Assert.NotNull(tags);
            Assert.Equal(2, tags.Count);
            Assert.Equal("admin", tags[0]);
            Assert.Equal("user", tags[1]);
        }

        [Fact]
        public void TestBooleanTrue()
        {
            var sld = "verified[^1";
            var data = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.True((bool)data["verified"]);
        }

        [Fact]
        public void TestBooleanFalse()
        {
            var sld = "active[^0";
            var data = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.False((bool)data["active"]);
        }
    }

    public class MLDEncodingTests
    {
        [Fact]
        public void TestSingleRecord()
        {
            var data = new Dictionary<string, object>
            {
                { "name", "Alice" },
                { "age", 30 }
            };
            var mld = SLDParser.EncodeMLD(data);
            Assert.Contains("name[Alice", mld);
            Assert.Contains("age[30", mld);
        }

        [Fact]
        public void TestMultipleRecords()
        {
            var data = new List<Dictionary<string, object>>
            {
                new Dictionary<string, object> { { "name", "Alice" } },
                new Dictionary<string, object> { { "name", "Bob" } }
            };
            var mld = SLDParser.EncodeMLD(data);
            Assert.Contains("\n", mld);
            var lines = mld.Split('\n');
            Assert.Equal(2, lines.Length);
        }
    }

    public class MLDDecodingTests
    {
        [Fact]
        public void TestSingleRecord()
        {
            var mld = "name[Alice;age[30";
            var data = SLDParser.DecodeMLD(mld) as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.Equal("Alice", data["name"]);
            Assert.Equal("30", data["age"]);
        }

        [Fact]
        public void TestMultipleRecords()
        {
            var mld = "name[Alice\nname[Bob";
            var data = SLDParser.DecodeMLD(mld) as List<Dictionary<string, object>>;
            Assert.NotNull(data);
            Assert.Equal(2, data.Count);
        }
    }

    public class FormatConversionTests
    {
        [Fact]
        public void TestSLDToMLD()
        {
            var sld = "name[Alice~name[Bob~";
            var mld = SLDParser.SLDToMLD(sld);
            Assert.DoesNotContain("~", mld);
            Assert.Contains("\n", mld);
        }

        [Fact]
        public void TestMLDToSLD()
        {
            var mld = "name[Alice\nname[Bob";
            var sld = SLDParser.MLDToSLD(mld);
            Assert.DoesNotContain("\n", sld);
            Assert.Contains("~", sld);
        }

        [Fact]
        public void TestRoundTripSLDMLDSLD()
        {
            var original = "name[Alice;age[30~name[Bob;age[25";
            var mld = SLDParser.SLDToMLD(original);
            var backToSLD = SLDParser.MLDToSLD(mld);
            Assert.Equal(original, backToSLD);
        }

        [Fact]
        public void TestRoundTripMLDSLDMLD()
        {
            var original = "name[Alice;age[30\nname[Bob;age[25";
            var sld = SLDParser.MLDToSLD(original);
            var backToMLD = SLDParser.SLDToMLD(sld);
            Assert.Equal(original, backToMLD);
        }
    }

    public class EdgeCaseTests
    {
        [Fact]
        public void TestEmptyStringSLD()
        {
            var data = SLDParser.DecodeSLD("") as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.Empty(data);
        }

        [Fact]
        public void TestEmptyStringMLD()
        {
            var data = SLDParser.DecodeMLD("") as Dictionary<string, object>;
            Assert.NotNull(data);
            Assert.Empty(data);
        }

        [Fact]
        public void TestEmptyObjectEncoding()
        {
            var data = new Dictionary<string, object>();
            var sld = SLDParser.EncodeSLD(data);
            Assert.Equal("", sld);
        }

        [Fact]
        public void TestSpecialCharactersPreserved()
        {
            var data = new Dictionary<string, object>
            {
                { "path", "C:\\Users\\Alice" }
            };
            var sld = SLDParser.EncodeSLD(data);
            var decoded = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(decoded);
            Assert.Equal("C:\\Users\\Alice", decoded["path"]);
        }
    }

    public class ComplexDataTests
    {
        [Fact]
        public void TestMixedTypes()
        {
            var data = new Dictionary<string, object>
            {
                { "name", "Alice" },
                { "age", 30 },
                { "verified", true },
                { "tags", new List<string> { "admin", "user" } }
            };
            data["middle"] = null!;
            var sld = SLDParser.EncodeSLD(data);
            var decoded = SLDParser.DecodeSLD(sld) as Dictionary<string, object>;
            Assert.NotNull(decoded);
            Assert.Equal("Alice", decoded["name"]);
            Assert.True((bool)decoded["verified"]);
            var tags = decoded["tags"] as List<object>;
            Assert.NotNull(tags);
            Assert.Equal(2, tags.Count);
            Assert.Equal("admin", tags[0]);
            Assert.Equal("user", tags[1]);
        }
    }
}
