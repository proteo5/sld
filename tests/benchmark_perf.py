#!/usr/bin/env python3
"""Performance benchmark for SLD/MLD parser and serializer."""
import json
import sys
import time
from typing import List, Dict, Any

sys.path.insert(0, 'tools')
from validator import parse_sld, parse_mld
from canonicalizer import encode_record


def generate_test_data(num_records: int = 1000) -> List[Dict[str, Any]]:
    """Generate synthetic test data."""
    records = []
    for i in range(num_records):
        records.append({
            "id": i,
            "name": f"User_{i}",
            "email": f"user{i}@example.com",
            "active": i % 2 == 0,
            "score": float(i * 1.5),
            "tags": ["tag1", "tag2", "tag3"],
            "description": "A test record with some text and; special chars"
        })
    return records


def benchmark_parse_sld(data_sld: str, iterations: int = 100) -> float:
    """Benchmark SLD parsing."""
    start = time.perf_counter()
    for _ in range(iterations):
        parse_sld(data_sld)
    end = time.perf_counter()
    return (end - start) / iterations


def benchmark_serialize_sld(records: List[Dict], iterations: int = 100) -> float:
    """Benchmark SLD serialization."""
    start = time.perf_counter()
    for _ in range(iterations):
        result = []
        for rec in records:
            result.append(encode_record(rec))
        "~".join(result) + "~"
    end = time.perf_counter()
    return (end - start) / iterations


def main():
    print("SLD/MLD Performance Benchmark\n")

    # Generate test data
    records = generate_test_data(1000)

    # Serialize to SLD
    sld_parts = [encode_record(rec) for rec in records]
    data_sld = "~".join(sld_parts) + "~"

    # JSON equivalent
    data_json = json.dumps({"records": records})

    print(f"Test data: {len(records)} records")
    print(f"SLD size: {len(data_sld):,} bytes")
    print(f"JSON size: {len(data_json):,} bytes")
    print(f"Compression ratio: {len(data_sld)/len(data_json):.2%}\n")

    # Benchmark parsing
    parse_time = benchmark_parse_sld(data_sld, iterations=10)
    print(f"Parse SLD (avg): {parse_time*1000:.2f} ms")
    print(f"Throughput: {len(records)/parse_time:,.0f} records/sec\n")

    # Benchmark serialization
    serialize_time = benchmark_serialize_sld(records, iterations=10)
    print(f"Serialize SLD (avg): {serialize_time*1000:.2f} ms")
    print(f"Throughput: {len(records)/serialize_time:,.0f} records/sec\n")

    # JSON baseline
    json_parse_start = time.perf_counter()
    for _ in range(10):
        json.loads(data_json)
    json_parse_time = (time.perf_counter() - json_parse_start) / 10

    json_serialize_start = time.perf_counter()
    for _ in range(10):
        json.dumps({"records": records})
    json_serialize_time = (time.perf_counter() - json_serialize_start) / 10

    print(f"JSON parse (avg): {json_parse_time*1000:.2f} ms")
    print(f"JSON serialize (avg): {json_serialize_time*1000:.2f} ms\n")

    print(f"SLD parse vs JSON: {parse_time/json_parse_time:.2f}x slower")
    print(f"SLD serialize vs JSON: {serialize_time/json_serialize_time:.2f}x slower")


if __name__ == '__main__':
    main()
