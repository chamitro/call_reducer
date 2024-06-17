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
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

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

contract StandardToken is ERC20, BasicToken {

  mapping (address => mapping (address => uint256)) internal allowed;

}

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  function transferOwnership(address newOwner) public           {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

contract Pausable is Ownable {
  event PausePublic(bool newState);
  event PauseOwnerAdmin(bool newState);

  bool public pausedPublic = false;
  bool public pausedOwnerAdmin = false;

  address public admin;

  function pause(bool newPausedPublic, bool newPausedOwnerAdmin)           public {
    require(!(newPausedPublic == false && newPausedOwnerAdmin == true));

    pausedPublic = newPausedPublic;
    pausedOwnerAdmin = newPausedOwnerAdmin;

    PausePublic(newPausedPublic);
    PauseOwnerAdmin(newPausedOwnerAdmin);
  }
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

    function burn(uint _value) returns (bool)
    {
        balances[msg.sender]                                   ;
        totalSupply                          ;
        Burn(msg.sender, _value);
        Transfer(msg.sender, address(0x0), _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) returns (bool) 
    {

        return burn(_value);
    }

    function emergencyERC20Drain( ERC20 token, uint amount )           {

        token.transfer( owner, amount );
    }

    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

    function changeAdmin(address newAdmin)           {

        AdminTransferred(admin, newAdmin);
        admin = newAdmin;
    }
}
