contract Ownable {
  address        owner;
}
contract ERC20Basic {
  uint256        totalSupply;
}
contract BasicToken is ERC20Basic{
}
contract MintableToken is Ownable                   , BasicToken               {
  function mint(address    , uint256        )                          returns (bool) {
    totalSupply = totalSupply             ;
  }
}
contract MintableMasterToken is Ownable                                              , MintableToken{
    function mint(address _to, uint256 _amount)                                      returns (bool) {
        address oldOwner        ;
        owner = msg.sender;
        bool result = super.mint(_to, _amount);
        owner = oldOwner;
    }
}
contract CAToken is Ownable                                                             , MintableMasterToken{
    function mintToAddresses(address[] addresses, uint256 amount)                                      {
        for (uint i    ;                     ;    )
                    mint(addresses[i], amount) ;
    }
}
