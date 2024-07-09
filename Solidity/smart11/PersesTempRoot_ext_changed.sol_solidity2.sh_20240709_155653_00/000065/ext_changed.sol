contract ERC20Token{
    function transfer(             uint256       )
        public
        returns (bool success)
                   ;
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
        uint256 transferable                                ;
        stox.transfer(msg.sender, transferable);
    }
}
