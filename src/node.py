from typing import List, Set
from .block import Block
from .blockchain import Blockchain
from .transaction import Transaction


class Node:
    """
    Simulates a peer-to-peer full node in the decentralized network.
    Maintains a local ledger copy, synchronizes with connected peers,
    and applies longest-valid-chain consensus to resolve network forks.
    """

    def __init__(self, node_id: str, difficulty: int = 2):
        self.node_id = node_id
        self.blockchain = Blockchain(difficulty=difficulty)
        self.peers: Set["Node"] = set()

    def connect_peer(self, peer: "Node") -> None:
        """Establishes bidirectional peer connection."""
        if peer != self:
            self.peers.add(peer)
            peer.peers.add(self)

    def broadcast_transaction(self, tx: Transaction) -> int:
        """Broadcasts a transaction to all connected network peers."""
        accepted_count = 0
        if self.blockchain.add_transaction(tx):
            accepted_count += 1

        for peer in self.peers:
            if peer.blockchain.add_transaction(tx):
                accepted_count += 1
        return accepted_count

    def mine_and_broadcast(self, miner_address: str) -> Block:
        """Mines pending transactions locally and propagates the new block to peers."""
        new_block = self.blockchain.mine_pending_transactions(miner_address)
        for peer in self.peers:
            peer.resolve_conflicts([self.blockchain.chain])
        return new_block

    def resolve_conflicts(self, peer_chains: List[List[Block]]) -> bool:
        """
        Consensus Algorithm: Adopts the longest valid chain in the network.
        Returns True if the node's local chain was replaced.
        """
        longest_chain: List[Block] = self.blockchain.chain
        max_length = len(self.blockchain.chain)

        for chain in peer_chains:
            if len(chain) > max_length:
                # Check candidate chain validity
                candidate_blockchain = Blockchain(difficulty=self.blockchain.difficulty)
                candidate_blockchain.chain = chain
                if candidate_blockchain.is_chain_valid():
                    max_length = len(chain)
                    longest_chain = chain

        if longest_chain != self.blockchain.chain:
            self.blockchain.chain = list(longest_chain)
            return True

        return False

    def __repr__(self) -> str:
        return f"<Node {self.node_id} (Blocks: {len(self.blockchain.chain)}, Peers: {len(self.peers)})>"
