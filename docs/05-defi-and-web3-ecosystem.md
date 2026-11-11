# Module 05: DeFi Primitives & Web3 Ecosystem

Decentralized Finance (DeFi) reconstructs traditional financial services (trading, lending, derivatives, insurance) using composable, non-custodial smart contracts.

---

## 1. Automated Market Makers (AMM) & Uniswap Math

Traditional exchanges use an order book of bids and asks. In blockchain, frequent order modifications incur prohibitive gas fees. 

**AMMs** solve this using algorithmic liquidity pools governed by the **Constant Product Formula**:

$$x \cdot y = k$$

Where:
- $x$: Token balance of Asset A in pool (e.g., ETH)
- $y$: Token balance of Asset B in pool (e.g., USDC)
- $k$: Invariant constant

```
                  Token Y (USDC)
                       ▲
                       │     * (Curve: x * y = k)
                       │      \
                       │       \  Price = dy / dx
                       │        \
                       └───────────► Token X (ETH)
```

When a trader swaps $\Delta x$ of Asset A into the pool, they receive $\Delta y$ of Asset B such that:

$$(x + \Delta x)(y - \Delta y) = k \implies \Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$$

---

## 2. Decentralized Lending Protocols (Aave, Compound)

- Users deposit crypto collateral to earn yield.
- Borrowers withdraw loans against **over-collateralized** deposits (e.g., deposit $150 of ETH to borrow $100 of USDC).
- If market volatility drops collateral value below the liquidation threshold, automated liquidator bots trigger a programmatic liquidation, repaying the debt with a penalty discount.

---

## 3. Decentralized Oracles (The Oracle Problem)

Blockchains are deterministic state machines that cannot natively make external HTTP requests or query real-world APIs.
- **The Oracle Problem**: How does a smart contract securely know the current off-chain price of ETH/USD or weather outcomes?
- **Decentralized Oracle Networks (DONs)** (e.g., Chainlink): Independent nodes fetch API data, aggregate multiple data sources, reach consensus on the median value, and commit the verified result to an on-chain oracle contract.

---

## 4. Maximal Extractable Value (MEV)

Block builders and searchers observe pending unconfirmed transactions in the public mempool:
- **Front-running**: Inserting a transaction with a higher priority gas tip right before a victim's trade.
- **Sandwich Attacks**: Buying ahead of a large DEX trade to push up the price, then selling immediately after for guaranteed profit.
- Mitigated by private RPC endpoints (e.g., Flashbots Protect) and decentralized sequencing.
