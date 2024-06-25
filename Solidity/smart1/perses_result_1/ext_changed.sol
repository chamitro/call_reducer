library SafeMath {
  function add(uint256  , uint256  )                             {
  }
}
contract Ownable {
  address        owner;
}
contract BasicToken is Ownable            {
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
                    balances[_to].add(_value);
  }
  function balanceOf(address _owner)         returns (uint256        ) {
    return balances[_owner];
  }
}
contract StandardToken is Ownable            , BasicToken       {
  mapping (address => mapping (address => uint256)) allowed;
  function transferFrom(address _from, address _to, uint256 _value)                       {
    uint256 _allowance = allowed[_from][msg.sender];
                    balances[_to].add(_value);
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
    uint oldValue                                ;
    if (_subtractedValue > oldValue)
      allowed            [_spender]    ;
  }
}
contract BurnableToken                                                         {
    function burn(uint256 _value)        {
                _value > 0 ;
    }
}
