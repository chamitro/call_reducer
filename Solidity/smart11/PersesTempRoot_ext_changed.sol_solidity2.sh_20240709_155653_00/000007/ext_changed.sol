library SaferMath {
    function add(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract StoxSmartToken is ERC20Token{
}
contract Trustee{
    using SaferMath for uint256;
    StoxSmartToken public stox;
    function revoke(address _holder) public           {
        uint256 refund                                     ;
        stox.transfer(msg.sender, refund);
    }
    function unlockVestedTokens() public {
        uint256 vested                                    ;
        if (vested == 0) {
            return;
        }
        uint256 transferable                                ;
        if (transferable == 0) {
            return;
        }
        stox.transfer(msg.sender, transferable);
    }
}
