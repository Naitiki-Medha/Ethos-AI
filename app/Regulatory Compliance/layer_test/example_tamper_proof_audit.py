"""
Tamper-Proof Audit Logging Example
Demonstrates cryptographic signing and immutable storage for legal defensibility
"""

from utils.tamper_proof_audit import TamperProofAuditLogger
import json

print("=" * 80)
print("TAMPER-PROOF AUDIT LOGGING DEMONSTRATION")
print("Cryptographic signing + Immutable storage = Legal defensibility")
print("=" * 80)

# Initialize tamper-proof audit logger
logger = TamperProofAuditLogger(
    log_file="demo_tamper_proof_audit.jsonl",
    secret_key="demo_secret_key_for_testing_only_12345678"  # In production, use secure key
)

print("\n1. LOGGING ENTRIES")
print("-" * 80)

# Log some compliance checks
entries = []

entry1 = logger.log({
    "user_id": "user_001",
    "content_hash": "abc123",
    "is_compliant": True,
    "violations": [],
    "action": "Content approved"
})
print(f"✓ Logged: {entry1.entry_id}")
print(f"  Hash: {entry1.entry_hash[:16]}...")
print(f"  Signature: {entry1.signature[:16]}...")
entries.append(entry1)

entry2 = logger.log({
    "user_id": "user_002",
    "content_hash": "def456",
    "is_compliant": False,
    "violations": ["SGI_MANDATORY_LABELING"],
    "action": "Content blocked"
})
print(f"✓ Logged: {entry2.entry_id}")
print(f"  Hash: {entry2.entry_hash[:16]}...")
print(f"  Previous Hash: {entry2.previous_hash[:16]}...")
entries.append(entry2)

entry3 = logger.log({
    "user_id": "user_003",
    "content_hash": "ghi789",
    "is_compliant": False,
    "violations": ["HUMAN_REVIEW_REQUIRED"],
    "action": "Sent for human review"
})
print(f"✓ Logged: {entry3.entry_id}")
entries.append(entry3)

# Verify chain
print("\n2. VERIFYING CHAIN INTEGRITY")
print("-" * 80)

is_valid, errors = logger.verify_chain()

if is_valid:
    print("✅ CHAIN VALID - No tampering detected")
    print(f"   All {len(entries)} entries verified")
    print("   • All signatures valid")
    print("   • All hashes match")
    print("   • Chain links intact")
else:
    print("❌ CHAIN INVALID - Tampering detected!")
    for error in errors:
        print(f"   • {error}")

# Get statistics
print("\n3. AUDIT LOG STATISTICS")
print("-" * 80)

stats = logger.get_statistics()
print(f"Total Entries: {stats['total_entries']}")
print(f"First Entry: {stats['first_entry']['id']} at {stats['first_entry']['timestamp']}")
print(f"Last Entry: {stats['last_entry']['id']} at {stats['last_entry']['timestamp']}")
print(f"Chain Valid: {'✅ Yes' if stats['chain_valid'] else '❌ No'}")

# Demonstrate tamper detection
print("\n4. TAMPER DETECTION TEST")
print("-" * 80)

print("Attempting to tamper with log file...")

# Read log file
with open("demo_tamper_proof_audit.jsonl", "r") as f:
    lines = f.readlines()

# Tamper with second entry
if len(lines) >= 2:
    tampered_entry = json.loads(lines[1])
    tampered_entry["data"]["is_compliant"] = True  # Change False to True
    lines[1] = json.dumps(tampered_entry) + "\n"
    
    # Write tampered log
    with open("demo_tamper_proof_audit.jsonl", "w") as f:
        f.writelines(lines)
    
    print("✓ Tampered: Changed entry #2 is_compliant from False to True")

# Verify again
print("\nVerifying chain after tampering...")
is_valid, errors = logger.verify_chain()

if is_valid:
    print("❌ ERROR: Tampering not detected (this shouldn't happen!)")
else:
    print("✅ TAMPERING DETECTED!")
    print(f"   Found {len(errors)} integrity violations:")
    for error in errors:
        print(f"   • {error}")

# Restore original log for demo
print("\nRestoring original log...")
logger2 = TamperProofAuditLogger(
    log_file="demo_tamper_proof_audit_restored.jsonl",
    secret_key="demo_secret_key_for_testing_only_12345678"
)

logger2.log({
    "user_id": "user_001",
    "content_hash": "abc123",
    "is_compliant": True,
    "violations": [],
    "action": "Content approved"
})

logger2.log({
    "user_id": "user_002",
    "content_hash": "def456",
    "is_compliant": False,
    "violations": ["SGI_MANDATORY_LABELING"],
    "action": "Content blocked"
})

logger2.log({
    "user_id": "user_003",
    "content_hash": "ghi789",
    "is_compliant": False,
    "violations": ["HUMAN_REVIEW_REQUIRED"],
    "action": "Sent for human review"
})

# Export for legal purposes
print("\n5. LEGAL EXPORT")
print("-" * 80)

report = logger2.export_for_legal("audit_legal_export.json")

print(f"✓ Exported to: audit_legal_export.json")
print(f"  Total Entries: {report['total_entries']}")
print(f"  Chain Valid: {'✅ Yes' if report['chain_valid'] else '❌ No'}")
print(f"  Export Timestamp: {report['export_timestamp']}")
print("\nLegal export includes:")
print("  • All audit entries with timestamps")
print("  • Cryptographic hashes for each entry")
print("  • Digital signatures for verification")
print("  • Chain validation results")
print("  • Tamper detection status")

# Retrieve specific entry
print("\n6. ENTRY RETRIEVAL")
print("-" * 80)

entry = logger2.get_entry_by_id("AUDIT-00000002")
if entry:
    print(f"Retrieved Entry: {entry.entry_id}")
    print(f"  Timestamp: {entry.timestamp}")
    print(f"  Data: {json.dumps(entry.data, indent=4)}")
    print(f"  Hash: {entry.entry_hash}")
    print(f"  Signature Valid: {'✅ Yes' if entry.verify_signature(logger2.secret_key) else '❌ No'}")

print("\n" + "=" * 80)
print("TAMPER-PROOF AUDIT BENEFITS:")
print("=" * 80)
print("✓ Cryptographic signing (HMAC-SHA256)")
print("✓ Blockchain-like chain (each entry links to previous)")
print("✓ Immutable append-only storage")
print("✓ Tamper detection (any modification detected)")
print("✓ Chain verification (entire history validated)")
print("✓ Legal defensibility (cryptographically provable)")
print("✓ Non-repudiation (signatures prove authenticity)")
print("✓ Audit trail integrity (complete history preserved)")
print("✓ Compliance evidence (for regulatory audits)")
print("✓ Forensic analysis (track all changes)")
print("=" * 80)

print("\n💡 KEY FEATURES:")
print("• Each entry has unique hash")
print("• Each entry links to previous (blockchain-like)")
print("• Each entry is cryptographically signed")
print("• Any tampering breaks the chain")
print("• Verification is instant and cryptographic")
print("• Legal export includes all proof")
print("=" * 80)
