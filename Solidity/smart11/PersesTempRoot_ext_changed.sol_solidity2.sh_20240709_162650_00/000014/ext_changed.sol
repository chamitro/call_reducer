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
contract Trustee{
    using SaferMath for uint256;
    StoxSmartToken public stox;
}
