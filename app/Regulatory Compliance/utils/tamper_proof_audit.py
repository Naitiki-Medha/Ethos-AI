"""
Tamper-Proof Audit Logger
Uses cryptographic signing and immutable storage for legal defensibility
"""

import hashlib
import hmac
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path


class AuditEntry:
    """Represents a single tamper-proof audit entry"""

    def __init__(
        self,
        entry_id: str,
        timestamp: str,
        data: Dict[str, Any],
        previous_hash: Optional[str] = None,
    ):
        self.entry_id = entry_id
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash or "0" * 64  # Genesis entry
        self.entry_hash = self._calculate_hash()
        self.signature = None

    def _calculate_hash(self) -> str:
        """Calculate SHA-256 hash of entry"""
        entry_string = json.dumps(
            {
                "entry_id": self.entry_id,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash,
            },
            sort_keys=True,
        )
        return hashlib.sha256(entry_string.encode()).hexdigest()

    def sign(self, secret_key: str):
        """Sign entry with HMAC-SHA256"""
        message = f"{self.entry_id}:{self.timestamp}:{self.entry_hash}:{self.previous_hash}"
        self.signature = hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

    def verify_signature(self, secret_key: str) -> bool:
        """Verify entry signature"""
        if not self.signature:
            return False

        message = f"{self.entry_id}:{self.timestamp}:{self.entry_hash}:{self.previous_hash}"
        expected_signature = hmac.new(
            secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(self.signature, expected_signature)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "entry_hash": self.entry_hash,
            "signature": self.signature,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEntry":
        """Create from dictionary"""
        entry = cls(
            entry_id=data["entry_id"],
            timestamp=data["timestamp"],
            data=data["data"],
            previous_hash=data["previous_hash"],
        )
        entry.entry_hash = data["entry_hash"]
        entry.signature = data.get("signature")
        return entry


class TamperProofAuditLogger:
    """
    Tamper-proof audit logger using blockchain-like chain and cryptographic signing
    
    Features:
    1. Blockchain-like chain (each entry links to previous)
    2. Cryptographic signing (HMAC-SHA256)
    3. Immutable append-only storage
    4. Tamper detection
    5. Chain verification
    6. Legal defensibility
    """

    def __init__(
        self,
        log_file: str = "tamper_proof_audit.jsonl",
        secret_key: Optional[str] = None,
    ):
        """
        Initialize tamper-proof audit logger

        Args:
            log_file: Path to audit log file (JSONL format)
            secret_key: Secret key for HMAC signing (auto-generated if not provided)
        """
        self.log_file = Path(log_file)
        self.secret_key = secret_key or self._generate_secret_key()
        self.entry_counter = 0
        self.last_hash = None

        # Create log file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            self.log_file.touch()
        else:
            # Load last hash from existing log
            self._load_last_hash()

        # Setup standard logger for errors
        self.logger = logging.getLogger("TamperProofAudit")
        self.logger.setLevel(logging.INFO)

    def _generate_secret_key(self) -> str:
        """Generate a random secret key"""
        import secrets

        return secrets.token_hex(32)

    def _load_last_hash(self):
        """Load the last entry hash from existing log"""
        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    self.last_hash = last_entry["entry_hash"]
                    self.entry_counter = int(last_entry["entry_id"].split("-")[1])
        except Exception as e:
            self.logger.error(f"Error loading last hash: {e}")
            self.last_hash = None

    def log(self, data: Dict[str, Any]) -> AuditEntry:
        """
        Log an entry with tamper-proof guarantees

        Args:
            data: Data to log

        Returns:
            AuditEntry object
        """
        self.entry_counter += 1
        entry_id = f"AUDIT-{self.entry_counter:08d}"
        timestamp = datetime.now().isoformat()

        # Create entry
        entry = AuditEntry(
            entry_id=entry_id,
            timestamp=timestamp,
            data=data,
            previous_hash=self.last_hash,
        )

        # Sign entry
        entry.sign(self.secret_key)

        # Append to log (immutable)
        self._append_entry(entry)

        # Update last hash
        self.last_hash = entry.entry_hash

        return entry

    def _append_entry(self, entry: AuditEntry):
        """Append entry to log file (append-only)"""
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")
        except Exception as e:
            self.logger.error(f"Error appending entry: {e}")
            raise

    def verify_chain(self) -> tuple[bool, List[str]]:
        """
        Verify the entire audit chain

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        try:
            with open(self.log_file, "r") as f:
                lines = f.readlines()

            if not lines:
                return True, []

            previous_hash = None

            for i, line in enumerate(lines):
                try:
                    entry_data = json.loads(line)
                    entry = AuditEntry.from_dict(entry_data)

                    # Verify signature
                    if not entry.verify_signature(self.secret_key):
                        errors.append(
                            f"Entry {entry.entry_id}: Invalid signature (tampered)"
                        )

                    # Verify hash
                    expected_hash = entry._calculate_hash()
                    if entry.entry_hash != expected_hash:
                        errors.append(
                            f"Entry {entry.entry_id}: Hash mismatch (tampered)"
                        )

                    # Verify chain link
                    if i == 0:
                        if entry.previous_hash != "0" * 64:
                            errors.append(
                                f"Entry {entry.entry_id}: Invalid genesis entry"
                            )
                    else:
                        if entry.previous_hash != previous_hash:
                            errors.append(
                                f"Entry {entry.entry_id}: Broken chain link (tampered)"
                            )

                    previous_hash = entry.entry_hash

                except json.JSONDecodeError:
                    errors.append(f"Line {i+1}: Invalid JSON (corrupted)")
                except Exception as e:
                    errors.append(f"Line {i+1}: Error - {str(e)}")

        except Exception as e:
            errors.append(f"Error reading log file: {str(e)}")

        return len(errors) == 0, errors

    def get_entries(
        self, start_id: Optional[str] = None, end_id: Optional[str] = None
    ) -> List[AuditEntry]:
        """
        Get audit entries within range

        Args:
            start_id: Starting entry ID (inclusive)
            end_id: Ending entry ID (inclusive)

        Returns:
            List of AuditEntry objects
        """
        entries = []

        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    entry_data = json.loads(line)
                    entry = AuditEntry.from_dict(entry_data)

                    if start_id and entry.entry_id < start_id:
                        continue
                    if end_id and entry.entry_id > end_id:
                        break

                    entries.append(entry)

        except Exception as e:
            self.logger.error(f"Error reading entries: {e}")

        return entries

    def get_entry_by_id(self, entry_id: str) -> Optional[AuditEntry]:
        """Get specific entry by ID"""
        try:
            with open(self.log_file, "r") as f:
                for line in f:
                    entry_data = json.loads(line)
                    if entry_data["entry_id"] == entry_id:
                        return AuditEntry.from_dict(entry_data)
        except Exception as e:
            self.logger.error(f"Error finding entry: {e}")

        return None

    def export_for_legal(self, output_file: str):
        """
        Export audit log in legal-friendly format with verification

        Args:
            output_file: Path to output file
        """
        is_valid, errors = self.verify_chain()

        report = {
            "export_timestamp": datetime.now().isoformat(),
            "log_file": str(self.log_file),
            "total_entries": self.entry_counter,
            "chain_valid": is_valid,
            "verification_errors": errors,
            "entries": [],
        }

        # Add all entries
        entries = self.get_entries()
        for entry in entries:
            report["entries"].append(
                {
                    "entry_id": entry.entry_id,
                    "timestamp": entry.timestamp,
                    "data": entry.data,
                    "hash": entry.entry_hash,
                    "signature": entry.signature,
                    "signature_valid": entry.verify_signature(self.secret_key),
                }
            )

        # Write report
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def get_statistics(self) -> Dict[str, Any]:
        """Get audit log statistics"""
        entries = self.get_entries()

        if not entries:
            return {
                "total_entries": 0,
                "first_entry": None,
                "last_entry": None,
                "chain_valid": True,
            }

        is_valid, errors = self.verify_chain()

        return {
            "total_entries": len(entries),
            "first_entry": {
                "id": entries[0].entry_id,
                "timestamp": entries[0].timestamp,
            },
            "last_entry": {
                "id": entries[-1].entry_id,
                "timestamp": entries[-1].timestamp,
            },
            "chain_valid": is_valid,
            "verification_errors": errors if not is_valid else [],
        }


class ImmutableAuditLogger:
    """
    Wrapper for backward compatibility with existing AuditLogger
    Uses TamperProofAuditLogger internally
    """

    def __init__(self, log_file: str = "compliance_audit.log"):
        """Initialize with tamper-proof backend"""
        # Use tamper-proof logger
        self.tamper_proof_logger = TamperProofAuditLogger(
            log_file=log_file.replace(".log", "_tamper_proof.jsonl")
        )

        # Also keep standard logger for compatibility
        self.logger = logging.getLogger("IndianAICompliance")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        self.logger.addHandler(handler)

    def log(self, context, report):
        """Log with both standard and tamper-proof logging"""
        from datetime import datetime

        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": context.user_id,
            "content_hash": hash(context.content),
            "is_compliant": report.is_compliant,
            "violations": report.violations,
        }

        # Standard log
        self.logger.info(json.dumps(entry))

        # Tamper-proof log
        self.tamper_proof_logger.log(entry)

    def verify_integrity(self) -> tuple[bool, List[str]]:
        """Verify audit log integrity"""
        return self.tamper_proof_logger.verify_chain()

    def export_for_legal(self, output_file: str):
        """Export for legal purposes"""
        return self.tamper_proof_logger.export_for_legal(output_file)
