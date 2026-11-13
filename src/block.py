import hashlib
import json
import time
from typing import Any, Dict, List
from .transaction import Transaction


def compute_merkle_root(transactions: List[Transaction]) -> str:
    """Computes the binary Merkle root hash from an array of transactions."""
    if not transactions:
        return hashlib.sha256(b"empty_block").hexdigest()

    hashes = [tx.compute_hash() for tx in transactions]

    while len(hashes) > 1:
        # Duplicate last element if odd number of hashes
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])

        next_level = []
        for i in range(0, len(hashes), 2):
            combined = (hashes[i] + hashes[i + 1]).encode("utf-8")
            parent_hash = hashlib.sha256(combined).hexdigest()
            next_level.append(parent_hash)
        hashes = next_level

    return hashes[0]


class Block:
    """Represents a discrete block in the ledger chain containing verified transactions."""

    def __init__(
        self,
        index: int,
        transactions: List[Transaction],
        previous_hash: str,
        timestamp: Optional[float] = None,
        nonce: int = 0,
        merkle_root: Optional[str] = None,
    ):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = time.time() if timestamp is None else timestamp
        self.nonce = nonce
        self.merkle_root = merkle_root or compute_merkle_root(transactions)
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Calculates double-SHA-256 header hash satisfying Nakamoto block architecture."""
        header_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }
        canonical_str = json.dumps(header_data, sort_keys=True).encode("utf-8")
        first_round = hashlib.sha256(canonical_str).digest()
        return hashlib.sha256(first_round).hexdigest()

    def mine_block(self, difficulty: int) -> int:
        """
        Executes Proof-of-Work: repeatedly increments the nonce until the hash
        begins with `difficulty` number of leading zeros.
        """
        target_prefix = "0" * difficulty
        start_time = time.time()
        hashes_calculated = 0

        while not self.hash.startswith(target_prefix):
            self.nonce += 1
            self.hash = self.compute_hash()
            hashes_calculated += 1

        elapsed = max(time.time() - start_time, 0.0001)
        hashrate = int(hashes_calculated / elapsed)
        return hashrate

    def has_valid_transactions(self) -> bool:
        """Verifies that all contained transactions are valid and Merkle root matches."""
        if self.merkle_root != compute_merkle_root(self.transactions):
            return False

        for tx in self.transactions:
            if not tx.is_valid():
                return False

        return True

    def to_dict(self) -> Dict[str, Any]:
        """Provides human-readable JSON representation of the block."""
        return {
            "index": self.index,
            "hash": self.hash,
            "previous_hash": self.previous_hash,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
        }

    def __repr__(self) -> str:
        return f"<Block #{self.index} [Hash: {self.hash[:10]}.. Nonce: {self.nonce}]>"
