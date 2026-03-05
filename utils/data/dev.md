## Interaction with linora Chain Full Node via starknet_py

- **Documentation**: [Starknet.py docs](https://starknetpy.readthedocs.io/en/latest/index.html)
- **Address Handling**: Use `AddressRepresentation` and `parse_address` when interacting with addresses.
- **Contract Addresses**: Available in the `SystemConfig` object returned by the linora API.
- **ABIs**: Should be loaded using contract addresses from the full node client.

# Data Loading and Storage

## Configuration
- `DataConfig` class manages connections to linora API, full node client, and contract interactions
- Default data storage location: `data/linora/chain/`
- Automatically loads and caches system configuration and contract instances

## Available Loaders
- `load_markets()`: Fetches market data from linora API and saves to `markets.parquet`
- `block_timerange()`: Returns [start, end] block range from full node

## Contract Access
Key contracts loaded automatically via `load_contracts()`:
- ParaClear contract
- USDC token contract
- Oracle contract

## Data Storage
- Data stored in Parquet format for efficient querying
- Directory structure maintained under `data/linora/chain/`

## Querying Data
Data can be queried using DuckDB:
```python
import duckdb

# Read parquet files
markets = duckdb.sql("SELECT * FROM 'data/linora/chain/markets.parquet'").df()
```

Use DuckDB for efficient filtering and aggregation directly on parquet files in backtesting and algo trading systems.

