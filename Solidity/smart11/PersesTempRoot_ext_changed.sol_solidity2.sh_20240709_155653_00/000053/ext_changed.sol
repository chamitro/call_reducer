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
        stox         (msg.sender, refund);
    }
    function unlockVestedTokens() public {
        uint256 transferable                                ;
        stox.transfer(msg.sender, transferable);
    }
}
