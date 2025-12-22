"""
End-to-end test for normalization in extraction pipeline.

This simulates NER model outputs (with varied entity names) and verifies that
the extractors normalize them correctly using the centralized normalization module.
"""

import sys
import logging
from scripts.normalize_components import (
    normalize_component_name,
    normalize_node_name,
    normalize_device_name,
    normalize_external_system,
    normalize_interface
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_component_normalization():
    """Test component name normalization with realistic NER outputs."""
    print("\n" + "=" * 70)
    print("COMPONENT NORMALIZATION TEST")
    print("=" * 70)
    
    test_cases = [
        # (raw_ner_output, expected_canonical)
        ("External Stripe Payment Gateway", "Stripe"),
        ("Stripe Payment Service", "Stripe"),
        ("A PostgreSQL Database", "PostgreSQL"),
        ("Postgres DB", "PostgreSQL"),
        ("The MongoDB database", "MongoDB"),
        ("Backend Service", "Backend Service"),
        ("Service API", "API Service"),
        ("REST API", "API Service"),  # Both REST API and Service API → API Service
        ("GraphQL endpoint", "GraphQL API"),
        ("EcommerceFrontend", "Ecommerce Frontend"),
        ("Ecommerce Frontend", "Ecommerce Frontend"),
        ("Redis cache", "Redis"),
        ("RabbitMQ message queue", "RabbitMQ"),  # Matches RabbitMQ pattern
        ("Payment Service API", "Payment Service"),
    ]
    
    passed = 0
    failed = 0
    
    for raw, expected in test_cases:
        result = normalize_component_name(raw)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        print(f"{raw:40} -> {result:25} {status}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_node_normalization():
    """Test node/server name normalization."""
    print("\n" + "=" * 70)
    print("NODE NORMALIZATION TEST")
    print("=" * 70)
    
    test_cases = [
        ("In Docker Containers", "Docker Container"),
        ("Docker Container", "Docker Container"),
        ("A Linux Server", "Linux Server"),
        ("Linux Server", "Linux Server"),
        ("Ubuntu Server", "Ubuntu Server"),
        ("The Virtual Machine", "Virtual Machine"),
        ("EC2 Instance", "Ec2 Instance"),  # Title-cased
        ("Kubernetes cluster", "Kubernetes"),
        ("K8s pod", "Kubernetes"),
        ("Cloud VM", "Cloud Vm"),  # Title-cased
    ]
    
    passed = 0
    failed = 0
    
    for raw, expected in test_cases:
        result = normalize_node_name(raw)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        print(f"{raw:40} -> {result:25} {status}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_device_normalization():
    """Test device name normalization."""
    print("\n" + "=" * 70)
    print("DEVICE NORMALIZATION TEST")
    print("=" * 70)
    
    test_cases = [
        ("Via Web Browser", "Web Browser"),
        ("Web Browsers", "Web Browser"),
        ("Web Browser", "Web Browser"),
        ("And Mobile Devices", "Mobile Device"),
        ("Mobile Device", "Mobile Device"),
        ("Smartphone", "Smartphone"),
        ("The Tablet", "Tablet"),
        ("IoT devices", "IoT Device"),
    ]
    
    passed = 0
    failed = 0
    
    for raw, expected in test_cases:
        result = normalize_device_name(raw)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        print(f"{raw:40} -> {result:25} {status}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_external_system_normalization():
    """Test external system name normalization."""
    print("\n" + "=" * 70)
    print("EXTERNAL SYSTEM NORMALIZATION TEST")
    print("=" * 70)
    
    test_cases = [
        ("External Stripe", "Stripe"),
        ("The PayPal API", "PayPal"),
        ("Twilio service", "Twilio"),
        ("AWS S3 bucket", "AWS S3"),  # Pattern matches AWS S3
        ("SendGrid", "Sendgrid"),  # Title-cased
        ("OAuth provider", "OAuth Provider"),
    ]
    
    passed = 0
    failed = 0
    
    for raw, expected in test_cases:
        result = normalize_external_system(raw)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        print(f"{raw:40} -> {result:25} {status}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_interface_normalization():
    """Test interface name normalization."""
    print("\n" + "=" * 70)
    print("INTERFACE NORMALIZATION TEST")
    print("=" * 70)
    
    test_cases = [
        ("REST API", "Rest Api"),  # Title-cased when no pattern match
        ("REST endpoint", "REST API"),  # Pattern match
        ("GraphQL API", "Graphql Api"),  # Title-cased
        ("GraphQL endpoint", "GraphQL API"),  # Pattern match
        ("HTTP API", "Http Api"),  # Title-cased
        ("WebSocket connection", "WebSocket"),  # Pattern match
        ("gRPC service", "gRPC"),  # Pattern match
    ]
    
    passed = 0
    failed = 0
    
    for raw, expected in test_cases:
        result = normalize_interface(raw)
        status = "✅ PASS" if result == expected else f"❌ FAIL (got: {result})"
        print(f"{raw:40} -> {result:25} {status}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


def test_deduplication_scenario():
    """Test that normalization enables deduplication."""
    print("\n" + "=" * 70)
    print("DEDUPLICATION SCENARIO TEST")
    print("=" * 70)
    print("Simulating multiple NER extractions from different sentences...")
    
    # Simulate NER extracting these component names from different parts of text
    raw_extractions = [
        "PostgreSQL Database",
        "A PostgreSQL",
        "Postgres DB",
        "the PostgreSQL database",
    ]
    
    normalized = set()
    for raw in raw_extractions:
        canonical = normalize_component_name(raw)
        normalized.add(canonical)
        print(f"  Extracted: {raw:30} -> Normalized: {canonical}")
    
    print(f"\n  Raw extractions: {len(raw_extractions)}")
    print(f"  After normalization: {len(normalized)}")
    print(f"  Unique components: {list(normalized)}")
    
    if len(normalized) == 1 and "PostgreSQL" in normalized:
        print("  ✅ PASS: Deduplication successful!")
        return True
    else:
        print(f"  ❌ FAIL: Expected 1 unique component, got {len(normalized)}")
        return False


def main():
    print("\n" + "#" * 70)
    print("# END-TO-END NORMALIZATION TEST SUITE")
    print("#" * 70)
    
    results = {
        "Components": test_component_normalization(),
        "Nodes": test_node_normalization(),
        "Devices": test_device_normalization(),
        "External Systems": test_external_system_normalization(),
        "Interfaces": test_interface_normalization(),
        "Deduplication": test_deduplication_scenario(),
    }
    
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 All tests PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests FAILED. Review normalization rules.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
