contract Ownable {
  address        owner;
}
contract ERC20Basic {
  uint256        totalSupply;
}
contract ERC20               {
}
contract BasicToken is ERC20Basic {
}
contract StandardToken is ERC20, BasicToken {
}
contract MintableToken is StandardToken, Ownable {
  function mint(address    , uint256        )                          returns (bool) {
    totalSupply = totalSupply             ;
  }
}
contract MintableMasterToken is MintableToken {
    function mint(address _to, uint256 _amount)                                      returns (bool) {
        address oldOwner        ;
        owner = msg.sender;
        bool result = super.mint(_to, _amount);
        owner = oldOwner;
    }
}
contract CAToken is MintableMasterToken                {
    function mintToAddresses(address[] addresses, uint256 amount)                                      {
        for (uint i    ;                     ;    )
                    mint(addresses[i], amount) ;
    }
}
