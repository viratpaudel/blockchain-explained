import unittest
from src.block import Block, compute_merkle_root
from src.blockchain import Blockchain
from src.transaction import Transaction
from src.wallet import Wallet


class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.chain = Blockchain(difficulty=2, mining_reward=50.0)

    def test_genesis_block_creation(self):
        self.assertEqual(len(self.chain.chain), 1)
        genesis = self.chain.get_latest_block()
        self.assertEqual(genesis.index, 0)
        self.assertEqual(genesis.previous_hash, "0" * 64)
        self.assertTrue(len(genesis.hash) == 64)

    def test_transaction_signing_and_validation(self):
        tx = Transaction(sender="Alice", recipient="Bob", amount=25.0)
        self.assertFalse(tx.is_valid())  # Unsigned should fail

        tx.sign("alice_private_key")
        self.assertTrue(tx.is_valid())
        self.assertEqual(tx.amount, 25.0)

    def test_mining_and_balance_aggregation(self):
        # Alice mines block 1
        self.chain.mine_pending_transactions("Alice")
        self.assertEqual(self.chain.get_balance("Alice"), 50.0)

        # Alice sends 20 to Bob
        tx = Transaction(sender="Alice", recipient="Bob", amount=20.0)
        tx.sign("alice_key")
        success = self.chain.add_transaction(tx)
        self.assertTrue(success)

        # Charlie mines block 2
        self.chain.mine_pending_transactions("Charlie")
        self.assertEqual(self.chain.get_balance("Alice"), 30.0)
        self.assertEqual(self.chain.get_balance("Bob"), 20.0)
        self.assertEqual(self.chain.get_balance("Charlie"), 50.0)

    def test_insufficient_balance_rejection(self):
        # Bob has 0 balance, tries to send 10
        tx = Transaction(sender="Bob", recipient="Alice", amount=10.0)
        tx.sign("bob_key")
        added = self.chain.add_transaction(tx)
        self.assertFalse(added)

    def test_merkle_root_integrity(self):
        tx1 = Transaction("A", "B", 10.0, timestamp=100.0, signature="sig1")
        tx2 = Transaction("B", "C", 5.0, timestamp=101.0, signature="sig2")
        root1 = compute_merkle_root([tx1, tx2])

        # Same transactions produce identical Merkle root
        root2 = compute_merkle_root([tx1, tx2])
        self.assertEqual(root1, root2)

        # Tampering with an amount produces a different Merkle root
        tx2_tampered = Transaction("B", "C", 5.1, timestamp=101.0, signature="sig2")
        root3 = compute_merkle_root([tx1, tx2_tampered])
        self.assertNotEqual(root1, root3)

    def test_wallet_address_derivation_and_tx_signing(self):
        wallet_a = Wallet("Alice")
        wallet_b = Wallet("Bob")
        self.assertTrue(wallet_a.address.startswith("0x"))
        self.assertEqual(len(wallet_a.address), 42)

        tx = wallet_a.create_transaction(wallet_b.address, 15.0)
        self.assertTrue(tx.is_valid())
        self.assertEqual(tx.sender, wallet_a.address)
        self.assertEqual(tx.recipient, wallet_b.address)

    def test_chain_tamper_detection(self):
        self.chain.mine_pending_transactions("Miner1")
        self.assertTrue(self.chain.is_chain_valid())

        # Malicious modification of historical block
        self.chain.chain[1].transactions[0].amount = 9999.0
        self.assertFalse(self.chain.is_chain_valid())


if __name__ == "__main__":
    unittest.main()
