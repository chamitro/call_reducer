contract IERC20Token {
    function transfer(address    , uint256       )        returns (bool        );
}
contract ITokenHolder           {
}
contract ISmartToken is ITokenHolder, IERC20Token {
}
contract SmartToken is ISmartToken                                 {
}
contract StoxSmartToken is SmartToken {
}
contract Trustee            {
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
