"""
SLD (Single Line Data) Format - Python Implementation
A token-efficient data serialization format
"""

from typing import Any, Dict, List, Union


def escape(text: str) -> str:
    """Escape special SLD characters in a string.
    
    Args:
        text: The text to escape
        
    Returns:
        Escaped text safe for SLD format
    """
    if text is None:
        return ""
    
    str_text = str(text)
    return (str_text
            .replace("^", "^^")
            .replace("|", "^|")
            .replace("~", "^~")
            .replace("[", "^["))


def unescape(text: str) -> str:
    """Unescape SLD escape sequences.
    
    Args:
        text: The escaped text
        
    Returns:
        Unescaped original text
    """
    result = []
    i = 0
    while i < len(text):
        if text[i] == "^" and i + 1 < len(text):
            result.append(text[i + 1])
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def split_unescaped(text: str, delimiter: str) -> List[str]:
    """Split text by delimiter, respecting escape sequences.
    
    Args:
        text: The text to split
        delimiter: The delimiter character
        
    Returns:
        List of split parts
    """
    parts = []
    current = []
    i = 0
    
    while i < len(text):
        if text[i] == "^" and i + 1 < len(text):
            current.append(text[i:i+2])
            i += 2
        elif text[i] == delimiter:
            parts.append("".join(current))
            current = []
            i += 1
        else:
            current.append(text[i])
            i += 1
    
    if current or text.endswith(delimiter):
        parts.append("".join(current))
    
    return parts


def encode_record(record: Dict[str, Any]) -> str:
    """Encode a single record (dictionary) to SLD format.
    
    Args:
        record: Dictionary to encode
        
    Returns:
        SLD-formatted string for the record
    """
    parts = []
    
    for key, value in record.items():
        escaped_key = escape(str(key))
        
        if isinstance(value, dict):
            nested = encode_record(value)
            parts.append(f"{escaped_key}[{nested}")
        elif isinstance(value, list):
            # Handle list as nested records
            nested_items = []
            for item in value:
                if isinstance(item, dict):
                    nested_items.append(encode_record(item))
                else:
                    nested_items.append(escape(str(item)))
            parts.append(f"{escaped_key}[{'~'.join(nested_items)}")
        elif value is None:
            parts.append(f"{escaped_key}|")
        else:
            escaped_value = escape(str(value))
            parts.append(f"{escaped_key}|{escaped_value}")
    
    return "|".join(parts)


def encode(data: Union[List[Dict], Dict, Any]) -> str:
    """Encode data to SLD format.
    
    Args:
        data: Data to encode (dict, list of dicts, or simple value)
        
    Returns:
        SLD-formatted string
        
    Examples:
        >>> encode([{"name": "Laptop", "price": 3999.90}])
        'name|Laptop|price|3999.90'
        
        >>> encode([{"name": "Laptop", "price": 3999.90}, {"name": "Mouse", "price": 149.90}])
        'name|Laptop|price|3999.90~name|Mouse|price|149.90'
    """
    if isinstance(data, list):
        return "~".join(encode_record(record) for record in data)
    elif isinstance(data, dict):
        return encode_record(data)
    else:
        return escape(str(data))


def decode(sld_string: str) -> Union[List[Dict], Dict]:
    """Decode SLD format string to Python data structures.
    
    Args:
        sld_string: SLD-formatted string
        
    Returns:
        Decoded data (dict or list of dicts)
        
    Examples:
        >>> decode('name|Laptop|price|3999.90')
        {'name': 'Laptop', 'price': '3999.90'}
        
        >>> decode('name|Laptop|price|3999.90~name|Mouse|price|149.90')
        [{'name': 'Laptop', 'price': '3999.90'}, {'name': 'Mouse', 'price': '149.90'}]
    """
    if not sld_string:
        return {}
    
    records = []
    
    for record_str in split_unescaped(sld_string, "~"):
        if not record_str:
            continue
            
        record = {}
        fields = split_unescaped(record_str, "|")
        
        i = 0
        while i < len(fields):
            if i >= len(fields):
                break
                
            key = unescape(fields[i])
            
            # Check if this is a nested structure
            if "[" in fields[i] and "^[" not in fields[i]:
                # Remove the [ from the key
                key = key.replace("[", "")
                # Parse nested content (simplified)
                if i + 1 < len(fields):
                    nested_value = unescape(fields[i + 1])
                    record[key] = nested_value
                    i += 2
                else:
                    i += 1
            else:
                if i + 1 < len(fields):
                    value = unescape(fields[i + 1])
                    record[key] = value if value != "" else None
                    i += 2
                else:
                    record[key] = None
                    i += 1
        
        records.append(record)
    
    return records if len(records) > 1 else records[0] if records else {}


if __name__ == "__main__":
    # Example usage
    print("=== SLD Python Implementation ===\n")
    
    # Example 1: Simple records
    print("Example 1: Simple product data")
    data1 = [
        {"name": "Laptop", "price": "3999.90"},
        {"name": "Mouse", "price": "149.90"},
        {"name": "Headset", "price": "499.00"}
    ]
    sld1 = encode(data1)
    print(f"Encoded: {sld1}")
    print(f"Decoded: {decode(sld1)}\n")
    
    # Example 2: Objects with IDs
    print("Example 2: User records")
    data2 = [
        {"id": "1", "name": "John", "lastname": "Smith"},
        {"id": "2", "name": "Juan", "lastname": "Perez"}
    ]
    sld2 = encode(data2)
    print(f"Encoded: {sld2}")
    print(f"Decoded: {decode(sld2)}\n")
    
    # Example 3: Data with special characters
    print("Example 3: Escaped characters")
    data3 = [
        {"company": "Pipe|Works Inc"},
        {"product": "Model~XZ~2000"}
    ]
    sld3 = encode(data3)
    print(f"Encoded: {sld3}")
    print(f"Decoded: {decode(sld3)}\n")
    
    # Example 4: Null values
    print("Example 4: Null/empty values")
    data4 = {"name": "John", "middle": None, "lastname": "Doe"}
    sld4 = encode(data4)
    print(f"Encoded: {sld4}")
    print(f"Decoded: {decode(sld4)}")
