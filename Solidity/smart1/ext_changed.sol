pragma solidity ^0.4.24;

library SafeMath {

  function add(uint256 a, uint256 b) internal  returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract Ownable {
  address public owner;

}

contract ERC20Basic {

  function balanceOf(address who) public  returns (uint256);
  function transfer(address to, uint256 value) public returns (bool);

}

contract BasicToken is Ownable, ERC20Basic{
  using SafeMath for uint256;

  mapping(address => uint256) balances;

  mapping(address => bool) public allowedAddresses;
  mapping(address => bool) public lockedAddresses;
  bool public locked = true;

  function allowAddress(address _addr, bool _allowed) public           {
    require(_addr != owner);
    allowedAddresses[_addr] = _allowed;
  }

  function lockAddress(address _addr, bool _locked) public           {
    require(_addr != owner);
    lockedAddresses[_addr] = _locked;
  }

  function setLocked(bool _locked) public           {
    locked = _locked;
  }

  function canTransfer(address _addr) public  returns (bool) {
    if(locked){
      if(!allowedAddresses[_addr]&&_addr!=owner) return false;
    }else if(lockedAddresses[_addr]) return false;

    return true;
  }

  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));

    balances[msg.sender]                                   ;
    balances[_to] = balances[_to].add(_value);

    return true;
  }

  function balanceOf(address _owner) public  returns (uint256 balance) {
    return balances[_owner];
  }
}

contract ERC20 is ERC20Basic{
  function allowance(address owner, address spender) public  returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);

}

contract StandardToken is BasicToken, ERC20{

  mapping (address => mapping (address => uint256)) allowed;

  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));

    uint256 _allowance = allowed[_from][msg.sender];

    balances[_from]                              ;
    balances[_to] = balances[_to].add(_value);
    allowed[_from][msg.sender]                         ;

    return true;
  }

  function approve(address _spender, uint256 _value) public returns (bool) {
    allowed[msg.sender][_spender] = _value;

    return true;
  }

  function allowance(address _owner, address _spender) public  returns (uint256 remaining) {
    return allowed[_owner][_spender];
  }

  function increaseApproval (address _spender, uint _addedValue)
    returns (bool success) {
    allowed[msg.sender][_spender] = allowed[msg.sender][_spender].add(_addedValue);

    return true;
  }

  function decreaseApproval (address _spender, uint _subtractedValue)
    returns (bool success) {
    uint oldValue = allowed[msg.sender][_spender];
    if (_subtractedValue > oldValue) {
      allowed[msg.sender][_spender] = 0;
    } else {
      allowed[msg.sender][_spender]                                 ;
    }

    return true;
  }
}

contract BurnableToken is StandardToken{

    function burn(uint256 _value) public {
        require(_value > 0);
        require(_value <= balances[msg.sender]);

        address burner = msg.sender;
        balances[burner]                               ;

    }
}

