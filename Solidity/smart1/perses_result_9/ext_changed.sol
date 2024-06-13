library SafeMath {
  function sub(uint256  , uint256  )                             {
  }
  function add(uint256  , uint256  )                             {
  }
}
contract Ownable {
  address        owner;
}
contract ERC20Basic {
}
contract BasicToken is ERC20Basic, Ownable {
  using SafeMath for uint256;
  mapping(address => uint256) balances;
  mapping(address => bool)        allowedAddresses;
  mapping(address => bool)        lockedAddresses;
  bool        locked       ;
  function allowAddress(address _addr, bool _allowed)                  {
    allowedAddresses[_addr] = _allowed;
  }
  function lockAddress(address _addr, bool _locked)                  {
    lockedAddresses[_addr] = _locked;
  }
  function setLocked(bool _locked)                  {
    locked = _locked;
  }
  function canTransfer(address _addr)
              {
      if(                          _addr!=owner) return      ;
    }
  function transfer(address _to, uint256 _value)                       {
            _to !=         0  ;
                           balances[msg.sender].sub(_value);
  }
  function balanceOf(address _owner)         returns (uint256        ) {
    return balances[_owner];
  }
}
contract ERC20               {
}
contract StandardToken is ERC20, BasicToken {
  mapping (address => mapping (address => uint256)) allowed;
  function transferFrom(address _from, address _to, uint256 _value)                       {
            _to !=         0  ;
                      balances[_from].sub(_value);
  }
  function approve(address _spender, uint256 _value)                       {
    allowed[msg.sender][_spender] = _value;
  }
  function allowance(address _owner, address _spender)         returns (uint256          ) {
    return allowed[_owner][_spender];
  }
  function increaseApproval (address _spender, uint _addedValue)
                           {
                                    allowed[msg.sender][_spender].add(_addedValue);
  }
  function decreaseApproval (address _spender, uint _subtractedValue)
                           {
    uint oldValue = allowed[msg.sender][_spender];
                                      oldValue.sub(_subtractedValue);
  }
}
contract BurnableToken                  {
    function burn(uint256 _value)        {
                _value > 0 ;
    }
}
