import time
from typing import List, Optional
from .block import Block
from .transaction import Transaction


class Blockchain:
    """Manages the distributed ledger chain, mining operations, and consensus validation."""

    def __init__(self, difficulty: int = 3, mining_reward: float = 50.0):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.mining_reward = mining_reward
        self.pending_transactions: List[Transaction] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Constructs block #0 (the genesis block)."""
        genesis_tx = Transaction(
            sender="NETWORK",
            recipient="Satoshi",
            amount=50.0,
            timestamp=1231006505.0,  # Jan 3, 2009 Bitcoin genesis timestamp
            signature="genesis_signature_0000000000",
        )
        genesis_block = Block(
            index=0,
            transactions=[genesis_tx],
            previous_hash="0" * 64,
            timestamp=1231006505.0,
            nonce=2083236893,
        )
        self.chain.append(genesis_block)

    def get_latest_block(self) -> Block:
        """Returns the most recently mined block in the chain."""
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction) -> bool:
        """Validates and appends a transaction to the mempool (pending queue)."""
        if not transaction.is_valid():
            return False

        # Verify sender has sufficient balance (except coinbase/system transactions)
        if transaction.sender not in ("COINBASE", "NETWORK"):
            sender_balance = self.get_balance(transaction.sender)
            pending_spend = sum(
                tx.amount for tx in self.pending_transactions
                if tx.sender == transaction.sender
            )
            if sender_balance - pending_spend < transaction.amount:
                return False

        self.pending_transactions.append(transaction)
        return True

    def mine_pending_transactions(self, miner_address: str) -> Block:
        """
        Batches pending transactions, mints the coinbase block reward,
        executes Proof-of-Work, and commits the new block to the chain.
        """
        # Coinbase transaction (miner reward)
        reward_tx = Transaction(
            sender="COINBASE",
            recipient=miner_address,
            amount=self.mining_reward,
            timestamp=time.time(),
            signature="coinbase_proof",
        )

        transactions_to_mine = [reward_tx] + self.pending_transactions
        latest_block = self.get_latest_block()

        new_block = Block(
            index=latest_block.index + 1,
            transactions=transactions_to_mine,
            previous_hash=latest_block.hash,
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

    def get_balance(self, address: str) -> float:
        """Calculates current ledger balance for an address by aggregating all mined transactions."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        return round(balance, 8)

    def is_chain_valid(self) -> bool:
        """
        Performs full cryptographic audit of the blockchain:
        1. Validates previous_hash linkage between every adjacent block.
        2. Recalculates block hashes to detect any tampering with header/nonce.
        3. Recalculates Merkle roots to detect transaction alterations.
        4. Verifies Proof of Work difficulty constraint.
        """
        if not self.chain:
            return False

        genesis = self.chain[0]
        if genesis.index != 0 or genesis.previous_hash != "0" * 64:
            return False
        if genesis.compute_hash() != genesis.hash or not genesis.has_valid_transactions():
            return False

        target_prefix = "0" * self.difficulty

        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # 1. Verify previous hash pointer
            if current.previous_hash != previous.hash:
                return False

            # 2. Verify hash recalculation
            if current.compute_hash() != current.hash:
                return False

            # 3. Verify Merkle root integrity
            if not current.has_valid_transactions():
                return False

            # 4. Verify Proof of Work target
            if not current.hash.startswith(target_prefix):
                return False

        return True
