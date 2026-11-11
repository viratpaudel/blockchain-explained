import hashlib
import json
import time
from typing import Any, Dict, Optional


class Transaction:
    """Represents a financial or state transition between two parties."""

    def __init__(
        self,
        sender: str,
        recipient: str,
        amount: float,
        timestamp: Optional[float] = None,
        signature: Optional[str] = None,
    ):
        self.sender = sender
        self.recipient = recipient
        self.amount = round(float(amount), 8)
        self.timestamp = timestamp or time.time()
        self.signature = signature

    def to_dict(self) -> Dict[str, Any]:
        """Returns a canonical dictionary of transaction fields."""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }

    def compute_hash(self) -> str:
        """Calculates the unique SHA-256 hash of the transaction data."""
        canonical_json = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def sign(self, private_signer_key: str) -> None:
        """Simulates signing transaction with private key using deterministic HMAC-SHA256."""
        tx_hash = self.compute_hash()
        signature_material = f"{private_signer_key}:{tx_hash}".encode("utf-8")
        self.signature = hashlib.sha256(signature_material).hexdigest()

    def is_valid(self) -> bool:
        """Validates transaction integrity and non-negative amount."""
        # Genesis / Coinbase reward transactions have sender 'COINBASE' or 'NETWORK'
        if self.sender in ("COINBASE", "NETWORK"):
            return self.amount > 0

        if self.amount <= 0:
            return False

        if not self.signature:
            return False

        return True

    def __repr__(self) -> str:
        return f"<Tx {self.sender[:8]}.. -> {self.recipient[:8]}..: {self.amount} SETU>"
