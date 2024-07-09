contract ERC20Token{
    function transfer(address    , uint256       )
        returns (bool        )
                   ;
}
contract StoxSmartToken is ERC20Token{
}
contract Trustee{
    StoxSmartToken        stox;
    function revoke(               )                  {
        uint256 refund                                     ;
        stox.transfer(msg.sender, refund);
    }
    function unlockVestedTokens()        {
        uint256 transferable                                ;
        stox.transfer(msg.sender, transferable);
    }
}
