"""
Unit tests for SLD/MLD Python Implementation v2.0
"""

import pytest
from sld import (
    encode_sld, decode_sld, encode_mld, decode_mld,
    sld_to_mld, mld_to_sld, escape_value, unescape_value
)


class TestEscaping:
    """Test escape and unescape functions"""
    
    def test_escape_semicolon(self):
        assert escape_value("a;b") == "a^;b"
    
    def test_escape_tilde(self):
        assert escape_value("a~b") == "a^~b"
    
    def test_escape_bracket(self):
        assert escape_value("a[b") == "a^[b"
    
    def test_escape_brace(self):
        assert escape_value("a{b") == "a^{b"
    
    def test_escape_caret(self):
        assert escape_value("a^b") == "a^^b"
    
    def test_unescape_semicolon(self):
        assert unescape_value("a^;b") == "a;b"
    
    def test_unescape_multiple(self):
        assert unescape_value("a^;b^~c") == "a;b~c"


class TestSLDEncoding:
    """Test SLD encoding"""
    
    def test_single_record(self):
        data = {"name": "Alice", "age": 30}
        sld = encode_sld(data)
        assert "name[Alice" in sld
        assert "age[30" in sld
    
    def test_multiple_records(self):
        data = [
            {"name": "Alice"},
            {"name": "Bob"}
        ]
        sld = encode_sld(data)
        assert sld.count("~") >= 2  # At least 2 record separators
    
    def test_array_encoding(self):
        data = {"tags": ["admin", "user"]}
        sld = encode_sld(data)
        assert "tags{admin,user" in sld
    
    def test_boolean_true(self):
        data = {"verified": True}
        sld = encode_sld(data)
        assert "verified[^1" in sld
    
    def test_boolean_false(self):
        data = {"active": False}
        sld = encode_sld(data)
        assert "active[^0" in sld
    
    def test_null_value(self):
        data = {"middle": None}
        sld = encode_sld(data)
        assert "middle[" in sld
    
    def test_escaped_characters(self):
        data = {"note": "Price: $5;99"}
        sld = encode_sld(data)
        assert "note[Price: $5^;99" in sld


class TestSLDDecoding:
    """Test SLD decoding"""
    
    def test_single_record(self):
        sld = "name[Alice;age[30"
        data = decode_sld(sld)
        assert data["name"] == "Alice"
        assert data["age"] == "30"
    
    def test_multiple_records(self):
        sld = "name[Alice~name[Bob~"
        data = decode_sld(sld)
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["name"] == "Alice"
        assert data[1]["name"] == "Bob"
    
    def test_array_decoding(self):
        sld = "tags{admin,user"
        data = decode_sld(sld)
        assert data["tags"] == ["admin", "user"]
    
    def test_boolean_true(self):
        sld = "verified[^1"
        data = decode_sld(sld)
        assert data["verified"] is True
    
    def test_boolean_false(self):
        sld = "active[^0"
        data = decode_sld(sld)
        assert data["active"] is False


class TestMLDEncoding:
    """Test MLD encoding"""
    
    def test_single_record(self):
        data = {"name": "Alice", "age": 30}
        mld = encode_mld(data)
        assert "name[Alice" in mld
        assert "age[30" in mld
    
    def test_multiple_records(self):
        data = [
            {"name": "Alice"},
            {"name": "Bob"}
        ]
        mld = encode_mld(data)
        assert "\n" in mld
        lines = mld.split("\n")
        assert len(lines) == 2


class TestMLDDecoding:
    """Test MLD decoding"""
    
    def test_single_record(self):
        mld = "name[Alice;age[30"
        data = decode_mld(mld)
        assert data["name"] == "Alice"
        assert data["age"] == "30"
    
    def test_multiple_records(self):
        mld = "name[Alice\nname[Bob"
        data = decode_mld(mld)
        assert isinstance(data, list)
        assert len(data) == 2


class TestFormatConversion:
    """Test conversion between SLD and MLD"""
    
    def test_sld_to_mld(self):
        sld = "name[Alice~name[Bob~"
        mld = sld_to_mld(sld)
        assert "~" not in mld
        assert "\n" in mld
    
    def test_mld_to_sld(self):
        mld = "name[Alice\nname[Bob"
        sld = mld_to_sld(mld)
        assert "\n" not in sld
        assert "~" in sld
    
    def test_round_trip_sld_mld_sld(self):
        original = "name[Alice;age[30~name[Bob;age[25~"
        mld = sld_to_mld(original)
        back_to_sld = mld_to_sld(mld)
        assert back_to_sld == original
    
    def test_round_trip_mld_sld_mld(self):
        original = "name[Alice;age[30\nname[Bob;age[25"
        sld = mld_to_sld(original)
        back_to_mld = sld_to_mld(sld)
        assert back_to_mld == original


class TestEdgeCases:
    """Test edge cases"""
    
    def test_empty_string(self):
        assert decode_sld("") == {}
        assert decode_mld("") == {}
    
    def test_empty_record(self):
        data = {}
        sld = encode_sld(data)
        assert sld == ""
    
    def test_special_characters_in_value(self):
        data = {"path": "C:\\Users\\Alice"}
        sld = encode_sld(data)
        decoded = decode_sld(sld)
        assert decoded["path"] == "C:\\Users\\Alice"


class TestComplexData:
    """Test complex data structures"""
    
    def test_mixed_types(self):
        data = {
            "name": "Alice",
            "age": 30,
            "verified": True,
            "tags": ["admin", "user"],
            "middle": None
        }
        sld = encode_sld(data)
        decoded = decode_sld(sld)
        assert decoded["name"] == "Alice"
        assert decoded["verified"] is True
        assert decoded["tags"] == ["admin", "user"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
