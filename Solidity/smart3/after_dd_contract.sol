pragma solidity ^0.4.11;

library SafeMath {

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

contract ERC20Basic {
  uint256 public totalSupply;

  event Transfer(address indexed from, address indexed to, uint256 value);
}

contract ERC20 is ERC20Basic{

  event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract BasicToken is ERC20Basic{
  using SafeMath for uint256;

  mapping(address => uint256) balances;

}

contract StandardToken is ERC20Basic, ERC20, BasicToken{

  mapping (address => mapping (address => uint256)) allowed;

}

contract MintableToken is Ownable, ERC20Basic, ERC20, BasicToken, StandardToken{
  event Mint(address indexed to, uint256 amount);
  event MintFinished();

  bool public mintingFinished = false;

  function mint(address _to, uint256 _amount)                   public returns (bool) {
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(0x0, _to, _amount);
    return true;
  }

}

contract MintableMasterToken is Ownable, ERC20Basic, ERC20, BasicToken, StandardToken, MintableToken{
    event MintMasterTransferred(address indexed previousMaster, address indexed newMaster);
    address public mintMaster;

    function mint(address _to, uint256 _amount)                               public returns (bool) {
        address oldOwner = owner;
        owner = msg.sender;

        bool result = super.mint(_to, _amount);

        owner = oldOwner;

        return result;
    }

}

contract CAToken is Ownable, ERC20Basic, ERC20, BasicToken, StandardToken, MintableToken, MintableMasterToken{

    string public constant symbol = "testCAT";
    string public constant name = "testCAT";
    uint8 public constant decimals = 18;
    string public constant version = "2.0";

    function mintToAddresses(address[] addresses, uint256 amount) public                               {
        for (uint i = 0; i < addresses.length; i++) {
            require(mint(addresses[i], amount));
        }
    }

}
