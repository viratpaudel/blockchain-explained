# Module 02: Consensus Mechanisms

Distributed consensus enables independent, mutually untrusted nodes across the globe to synchronize and agree on a single shared version of history without a central authority.

---

## 1. The Byzantine Generals Problem

In 1982, Leslie Lamport, Robert Shostak, and Marshall Pease formulated the problem:
Multiple generals besieging an enemy city must coordinate an attack or retreat. Communication is conducted via messengers who may be intercepted or killed, and some generals may be traitors sending contradictory orders.

- In classical computer science, Byzantine Fault Tolerance (BFT) requires that fewer than $\frac{1}{3}$ of the nodes are traitorous ($n \ge 3f + 1$).
- In permissionless networks (Internet), anyone can spawn millions of fake identities (a **Sybil Attack**).
- Satoshi Nakamoto's breakthrough in 2008 resolved this by tying voting weight to **scarce physical resources** rather than IP addresses.

---

## 2. Proof of Work (PoW) - Nakamoto Consensus

In Proof of Work, nodes (miners) compete to solve an asymmetric computational puzzle: finding a `nonce` such that:

$$\text{SHA-256}(\text{SHA-256}(\text{BlockHeader})) < \text{Target}$$

### Characteristics:
- **Asymmetry**: Hard to calculate (billions of hashes per second), but trivial to verify (1 single hash evaluation).
- **Difficulty Adjustment**: Algorithms dynamically adjust the target so blocks are mined at consistent intervals (e.g., every 10 minutes in Bitcoin, every 12 seconds in pre-Merge Ethereum).
- **Longest Chain Rule**: If two miners produce a block simultaneously (a fork), nodes follow the chain with the most accumulated Proof of Work.

```
       ┌──► [Block 5A]
[Block 4] 
       └──► [Block 5B] ──► [Block 6B] (Longest valid chain wins; 5A is orphaned)
```

### Security Properties:
- **51% Attack Resistance**: An adversary must control more than half of the entire global hash rate to rewrite historical transactions.
- **Costly Immutability**: Modifying a block $k$ blocks deep requires re-mining that block and all subsequent $k$ blocks faster than the rest of the honest network combined.

---

## 3. Proof of Stake (PoS)

Rather than expending physical electricity, Proof of Stake replaces hardware miners with **economic validators** who lock up native cryptocurrency ("stake") as collateral.

### How PoS Works:
1. Validators deposit a minimum stake (e.g. 32 ETH).
2. Pseudo-random selection (using algorithms like RANDAO) chooses a block proposer for each time slot.
3. Committees of other validators attest to (vote on) the proposed block.
4. If a validator attempts a double-sign or votes for contradictory forks, their stake is programmatically **slashed** (destroyed).

```
┌─────────────────┬───────────────────────────────┬───────────────────────────────┐
│ Feature         │ Proof of Work (PoW)           │ Proof of Stake (PoS)          │
├─────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Resource        │ Computation (ASICs, energy)   │ Capital (locked cryptocurrency)│
│ Energy Usage    │ High (~countries' consumption)│ ~99.95% reduction vs PoW      │
│ Sybil Defense   │ Hashrate threshold            │ Capital value threshold       │
│ Penalty         │ Wasted electricity hardware   │ Slashing of deposited capital │
│ Finality        │ Probabilistic (e.g. 6 blocks) │ Deterministic (Casper FFG)    │
└─────────────────┴───────────────────────────────┴───────────────────────────────┘
```

---

## 4. Other Consensus Paradigms

1. **Delegated Proof of Stake (DPoS)**: Token holders vote for a fixed set of delegates (e.g., 21 block producers in EOS) who take turns producing blocks.
2. **Proof of Authority (PoA)**: Blocks are validated by approved identity-verified accounts. Common in enterprise and testnets.
3. **Practical Byzantine Fault Tolerance (pBFT)**: State-machine replication using multiple rounds of pre-prepare, prepare, and commit votes. High throughput, low validator scalability ($O(n^2)$ communication complexity).
