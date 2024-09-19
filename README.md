# GReduce

GReduce is a tool designed to minimize source code files by reducing their code, while keeping specific properties of the code. It supports both Solidity and C and is useful for simplifying code while retaining its functionality.

## Installation

To install GReduce, clone the repository and install it in editable mode:

```bash
git clone https://github.com/chamitro/call_reducer.git
cd call_reducer
pip install --editable .
```

## Solidity Setup

GReduce uses the Solidity compiler, and you can install multiple versions of it using solc-select. Follow these steps to install it:

```
#Install solc-select
pip3 install solc-select

#List available Solidity versions
solc-select install

#Install a specific Solidity version (e.g., version 0.8.0)
solc-select install 0.8.0
```
## Install Slither

Slither is a static analysis tool for Solidity smart contracts. You can install it as follows:

```
sudo python3 -m pip install slither-analyzer
```

Once installed, you can run Slither on a Solidity file, such as:

```
slither Solidity/smart2/ext_changed.sol
```

## GReduce Usage

GReduce supports the following arguments:

	- `--language`: Specify the programming language. Options: `solidity` or `c.``(Default: `"solidity"`)
	- `--source-file`: The source file to minimize. (Default: `"ext_changed.sol"`)
	- `--script`: The script to run during the reduction process. (Default: `"./solidity2.sh"`)

## Example Usage

To reduce a Solidity smart contract (e.g., `ext_changed.sol`) using the script `solidity2.sh`, follow these steps:

```
# Delete the comments in the smart contract source file

python3 delete_comments.py ./Solidity/smart2/ext_changed

# Install the required version of the Solidity compilerInstall the required version of the Solidity compiler

solc-select install 0.4.24
solc-select use 0.4.24

# Run GReduce on the source file

greduce --source-file ./Solidity/smart2/ext_changed.sol --script ./Solidity/smart2/solidity2.sh

```

Note: For each smart contract, ensure that Slither runs with the appropriate Solidity compiler version. The `solc-select` use version command is mandatory before running Slither.

## Running Solidity Benchmarks

To run all benchmarks for Solidity, execute:

```
./run_benchmarks.sh
```

In the folder `Solidity/smart*`, you will find the compiler version(`version`) and the property(`property`) for each smart contract.
