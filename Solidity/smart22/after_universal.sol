pragma solidity 0.5.0;

interface IERC20 {

}

contract ERC20Detailed is IERC20{

    constructor (string memory name, string memory symbol, uint8 decimals) public {

    }

    function name() public view returns (string memory) {

    }

    function symbol() public view returns (string memory) {

    }

    function decimals() public view returns (uint8) {

    }
}

