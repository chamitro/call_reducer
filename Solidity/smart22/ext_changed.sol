pragma solidity 0.5.0;

contract ERC20Detailed{
    string private _name;

    constructor (string memory name, string memory symbol, uint8 decimals) public {
        _name = name;

    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {

    }

    function decimals() public view returns (uint8) {

    }
}

