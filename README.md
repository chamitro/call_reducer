# GReduce

GReduce is a tool designed to minimize source code files by reducing their code, while keeping specific properties of the code. It supports both Solidity and C and is useful for simplifying code while retaining its functionality.

## Installation/Setup

**The project requires Python 3.10.14**

To install GReduce, clone the repository:

```bash
git clone https://github.com/chamitro/call_reducer.git
cd call_reducer
```

Install it in editable mode

```bash
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
### Install Slither

Slither is a static analysis tool for Solidity smart contracts. You can install it as follows:

```
sudo python3 -m pip install slither-analyzer
```

Once installed, you can run Slither on a Solidity file, such as:

```
slither Solidity/smart2/ext_changed.sol
```

### GReduce Usage

GReduce supports the following arguments:

	- `--language`: Specify the programming language. Options: `solidity` or `c.``(Default: `"solidity"`)
	- `--source-file`: The source file to minimize. (Default: `"ext_changed.sol"`)
	- `--script`: The script to run during the reduction process. (Default: `"./solidity2.sh"`)

### Example Usage

To reduce a Solidity smart contract (e.g., `ext_changed.sol`) using the script `solidity2.sh`, follow these steps:

```
# Delete the comments in the smart contract source file

python3 delete_comments.py --filepath  Solidity/smart2/ext_changed.sol

# Install the required version of the Solidity compilerInstall the required version of the Solidity compiler

solc-select install 0.4.24
solc-select use 0.4.24

# Run GReduce on the source file

greduce --source-file ./Solidity/smart2/ext_changed.sol --script ./Solidity/smart2/solidity2.sh

```

Note: For each smart contract, ensure that Slither runs with the appropriate Solidity compiler version. The `solc-select` use version command is mandatory before running Slither.

### Running Solidity Benchmarks

To run all benchmarks for Solidity, execute:

```
./run_solidity_benchmarks.sh
```

In the folder `Solidity/smart*`, you will find the compiler version(`version`) and the property(`property`) for each smart contract.

## C Setup

Depending on the input script, GReduce uses multiple C compilers. In order to 
avoid using multiple versions of LLVM or GCC we recommend using docker
containers that contain the desired compiler version. In this project we provide
images for the following versions:

1. clang-3.5.0
2. clang-3.6.0
3. clang-3.7.0
4. clang-3.8.0
5. clang-7.1.0
6. gcc-4.8.0
7. gcc-4.8.2
8. gcc-4.9.0

The input script can then be modified to run the programs with the containerized
compiler.

If your script uses CompCert make sure to install the needed version.

### C Usage

GReduce supports the following arguments:

	- `--language`: Specify the programming language. Options: `solidity` or `c.``(Default: `"solidity"`)
	- `--source-file`: The source file to minimize. (Default: `"ext_changed.sol"`)
	- `--script`: The script to run during the reduction process. (Default: `"./solidity2.sh"`)
	- `--mode`: Only available for C. The strategy to be followed by the reduction. Only accepts the values 'removal', 'replacement' and 'combination'

### Example Usage

To reduce a C program (e.g., `C/gcc-59903/small.c`) using the script `C/gcc-59903/r.sh`, follow these steps:

```
# Install the required compiler version, or build a docker container for the 
# version. If you choose to build a container the input script needs to be modified 

docker build -t <compiler version (e.g. gcc-4.8.0)>  --file <dockerfile path (e.g. ./dockerfiles/gcc_4_8.dockerfile)> .

# Run GReduce on the source file

greduce --source-file ./C/gcc-5990/small.c --script ./C/gcc-5990/r.sh --language c --mode removal
```

### Running C Benchmarks

In order to run the benchmarks locally you will need to follow the setup 
instructions.

In each C benchmark directory two script the files `r.sh` and `test_r.sh` can
be found. `r.sh` uses local versions of the required C compiler and `test_r.sh`
uses docker containers with the required compiler installed. The benchmark scipt
`./run_c_benchmarks.sh` uses `test_r.sh` as input.

#### C Benchmark setup

Install the CompCert compiler 3.7 version either using OPAM

```bash
# Install OPAM if needed, then:
opam install coq-compcert.3.7~coq-platform coq.8.11.0
```

Or from the source
```bash
tar xzf CompCert-3.7.tgz
cd CompCert-3.7
./configure x86_64-linux   # or arm-linux, etc.
make
make install
```

Build the following docker containers from the root directory (this may take some time):
   ```bash
    docker build -t clang-3.5.0  --file ./dockerfiles/clang_3_5_0.dockerfile .
    docker build -t clang-3.6.0  --file ./dockerfiles/clang_3_6_0.dockerfile .
    docker build -t clang-3.6.0  --file ./dockerfiles/clang_3_6_0.dockerfile .
    docker build -t clang-3.6.0-assertions  --file ./dockerfiles/clang_3_6_0_assertions.dockerfile .
    docker build -t clang-3.7.0  --file ./dockerfiles/clang_3_7_0.dockerfile .
    docker build -t clang-3.8.0  --file ./dockerfiles/clang_3_8_0.dockerfile .
    docker build -t clang-7.1.0  --file ./dockerfiles/clang_7_1_0.dockerfile .
    docker build -t gcc-4.8.2  --file ./dockerfiles/gcc_4_8_2.dockerfile .
    docker build -t gcc-4.8  --file ./dockerfiles/gcc_4_8.dockerfile .
    docker build -t gcc-4.9  --file ./dockerfiles/gcc_4_9.dockerfile .
   ```

You will also need to install the [Perses v2.5](https://github.com/uw-pluverse/perses)

#### Running the C benchmarks

To run all benchmarks for C, execute:

```
./run_c_benchmarks.sh
```

In the root directory a CSV file containing the results will be created.
