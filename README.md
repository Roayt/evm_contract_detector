# Arc Contract Monitor 

This script monitors contract deployments on Arc Layer 1 chain.
## What it does

- Extract contract address deployed in a block 
- Save the extracted contract address in a arc_monitor.log
- Saves the last processed blocks in state.json file 
- Continues from the last processed block when program starts again

## Requirements 

- python 3.13+
- uv 

## Project Structure

- `main.py` - Initial setup and entry point of the program

- `rpc.py` -  Calls Arc endpoint rpc and returns the response object 

- `blocks.py` - Core block processing and contract detection logic

- `last_seen.py` - Stores the last processed block and read the file when program starts again 

- `config.py` - Stores the arc rpc endpoint 

- `state.json` - Stores the last processed block number

- `arc_monitor.log` - Stores logs included detected contract address

## Setup 

### 1. Install uv (only if you don't have)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone repository 
```bash
git clone https://github.com/Roayt/arc_contract_monitor.git
cd arc_contract_monitor
uv run main.py
``` 

## Basic Usage 
- Default/Normal run 

```bash
uv run main.py
 ```

## Options 
- --rpc-url 

The RPC endpoint you can give according to your choice the endpoint you want to call

Example: 
```bash
uv run main.py --rpc-url <your rpc url>
```
- --interval 

Set sleep time for the loop according to the demand

Default: 2 seconds 
Example: 
```bash
uv run main.py --interval 5
```
This makes loop wait for 5 seconds 

- --start-block 

Sets the block number from which monitor should start fetching blocks

Example: 
```bash
uv run main.py --start-block <your number>
```

if --start-block is not provided:
     -If state.json exist, the monitor continues from the saved states 
     -If state.json does not exist, the monitor starts from the current chain height


## Sample Output
```
INFO:2026-08-31 12:34:16,510 - blocks -Contract Address is 0xa6e6a203a5a7b6cbd277e5a73f64d11883b45c5b
INFO:2026-08-31 12:36:22,258 - blocks Contract Address is 0x7914fb0946940e22cf018a43571c2a14f963fde2
```

The logs are also stored in arc_monitor.log 

## Limitations

- No reorg handling,as Arc uses PoA BFT consensus with deterministic finality so committed blocks can't be replaced.
- Receipts unavailable for pruned history 
- Current state Testnet


## License 

MIT see [LICENSE](LICENSE)
