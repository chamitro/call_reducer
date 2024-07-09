contract ERC20Token{
    function transfer(address _to, uint256 _value)
        public
        returns (bool success)
    {
        return true;
    }
}
contract StoxSmartToken is ERC20Token{
}
contract Trustee{
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
