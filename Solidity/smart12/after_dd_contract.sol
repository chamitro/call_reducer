pragma solidity ^0.4.18;

contract ERC20Basic {
  uint256 public totalSupply;

  function transfer(address to, uint256 value) public returns (bool);
  event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ERC20 is ERC20Basic {

  event Approval(address indexed owner, address indexed spender, uint256 value);
}

library SafeMath {

}

contract BasicToken is ERC20Basic {
  using SafeMath for uint256;

  mapping(address => uint256) balances;

  function transfer(address _to, uint256 _value) public returns (bool) {
    require(_to != address(0));
    require(_value <= balances[msg.sender]);

    balances[msg.sender]                                   ;
    balances[_to]                            ;
    Transfer(msg.sender, _to, _value);
    return true;
  }

}


contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

contract Pausable {
  event PausePublic(bool newState);
  event PauseOwnerAdmin(bool newState);

  bool public pausedPublic = false;
  bool public pausedOwnerAdmin = false;

  address public admin;

}

contract PausableToken is StandardToken, Pausable {

  function transfer(address _to, uint256 _value) public               returns (bool) {
    return super.transfer(_to, _value);
  }

}

contract SMILECOINToken is PausableToken {
    string  public  constant name = "SMILECOIN";
    string  public  constant symbol = "SMC";
    uint8   public  constant decimals = 18;

    function transfer(address _to, uint _value)                       returns (bool) 
    {
        return super.transfer(_to, _value);
    }

    event Burn(address indexed _burner, uint _value);

    function emergencyERC20Drain( ERC20 token, uint amount )           {

        token.transfer( owner, amount );
    }

    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

}
