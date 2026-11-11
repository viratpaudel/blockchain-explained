import hashlib
import secrets
from typing import Optional
from .transaction import Transaction


class Wallet:
    """
    Represents an asymmetric cryptographic user wallet.
    Generates private keys, derives public addresses, and signs transactions.
    """

    def __init__(self, name: str, private_key: Optional[str] = None):
        self.name = name
        self.private_key = private_key or secrets.token_hex(32)
        self.address = self._derive_address(self.private_key)

    @staticmethod
    def _derive_address(private_key: str) -> str:
        """Derives a deterministic public address by hashing the private key material."""
        first_hash = hashlib.sha256(private_key.encode("utf-8")).hexdigest()
        second_hash = hashlib.sha256(first_hash.encode("utf-8")).hexdigest()
        return f"0x{second_hash[:40]}"

    def create_transaction(self, recipient_address: str, amount: float) -> Transaction:
        """Creates and cryptographically signs an outbound transaction."""
        tx = Transaction(
            sender=self.address,
            recipient=recipient_address,
            amount=amount,
        )
        tx.sign(self.private_key)
        return tx

    def __repr__(self) -> str:
        return f"<Wallet {self.name} [{self.address[:8]}...{self.address[-4:]}]>"
