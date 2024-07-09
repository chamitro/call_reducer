pragma solidity ^0.4.11;
contract ERC20Token{
    function transfer(address _to, uint256 _value)
        public
        returns (bool success)
    {
        return true;
    }
}
library SaferMath {
}
contract StoxSmartToken is ERC20Token{
}
