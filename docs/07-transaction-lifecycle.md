# Transaction Lifecycle

A transaction is a request to change blockchain state. Nodes typically validate it, share it with peers, include it in a proposed block, and apply it after the network's consensus rules accept that block.

## 1. Create and sign

A wallet assembles the transaction's intended action and required fields. On account-based networks these may include a sender, recipient, value, nonce, fee, and optional contract-call data. The sender signs a canonical representation with their private key; nodes can verify the signature against the sender's public identity without learning the private key.

Exact transaction formats differ between protocols. A signature authenticates authorization, but it does not by itself guarantee that the transaction is valid or will be included.

## 2. Validate and propagate

A receiving node checks protocol-specific rules before relaying a transaction. Typical checks include a valid signature, correct nonce, sufficient funds for the value and fee, acceptable size, and compliance with fee or policy rules. Invalid transactions are rejected; valid ones may wait in a local transaction pool until selected for a block.

## 3. Include and execute

A block producer chooses eligible transactions, often considering fees, and orders them in a candidate block. Other nodes independently validate the block and execute its transactions in order. This ordering matters: earlier transactions can change the state against which later transactions are checked.

## 4. Confirm and finalize

Consensus determines which valid block becomes part of the canonical chain. Some protocols offer probabilistic confirmation, where confidence increases as more blocks build on top. Others provide explicit finality under stated assumptions. Applications should choose confirmation requirements appropriate to the value and risk of an action.

## Important distinction

A transaction being signed, broadcast, or included in a block are different milestones. A robust application should communicate pending, confirmed, and (where relevant) finalized status separately, while accounting for protocol-specific replacement, expiration, and reorganization behavior.
