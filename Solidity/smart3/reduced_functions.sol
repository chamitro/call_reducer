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


  
  


  
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }


  
  

}


contract Destructible is Ownable {

  

  
  

  
}


contract Pausable is Ownable {
  event Pause();
  event Unpause();

  bool public paused = false;


  
  

  
  

  
  

  
  
}


contract ERC20Basic {
  uint256 public totalSupply;
  
  
  event Transfer(address indexed from, address indexed to, uint256 value);
}


contract ERC20 is ERC20Basic {
  
  
  
  event Approval(address indexed owner, address indexed spender, uint256 value);
}


contract BasicToken is ERC20Basic {
  using SafeMath for uint256;

  mapping(address => uint256) balances;

  
  

  
  

}


contract StandardToken is ERC20, BasicToken {

  mapping (address => mapping (address => uint256)) allowed;


  
  

  
  

  
  

  
  

  

}



contract MintableToken is StandardToken, Ownable {
  event Mint(address indexed to, uint256 amount);
  event MintFinished();

  bool public mintingFinished = false;


  modifier canMint() {
    require(!mintingFinished);
    _;
  }

  
  function mint(address _to, uint256 _amount) onlyOwner canMint public returns (bool) {
    totalSupply = totalSupply.add(_amount);
    balances[_to] = balances[_to].add(_amount);
    Mint(_to, _amount);
    Transfer(0x0, _to, _amount);
    return true;
  }

  
  
}



contract PausableToken is StandardToken, Pausable {

  

  

  

  

  
}

contract MintableMasterToken is MintableToken {
    event MintMasterTransferred(address indexed previousMaster, address indexed newMaster);
    address public mintMaster;

    modifier onlyMintMasterOrOwner() {
        require(msg.sender == mintMaster || msg.sender == owner);
        _;
    }

    

    

    
    function mint(address _to, uint256 _amount) onlyMintMasterOrOwner canMint public returns (bool) {
        address oldOwner = owner;
        owner = msg.sender;

        bool result = super.mint(_to, _amount);

        owner = oldOwner;

        return result;
    }

}


contract CAToken is MintableMasterToken, PausableToken {
    
    
    string public constant symbol = "testCAT";
    string public constant name = "testCAT";
    uint8 public constant decimals = 18;
    string public constant version = "2.0";

    function mintToAddresses(address[] addresses, uint256 amount) public onlyMintMasterOrOwner canMint {
        for (uint i = 0; i < addresses.length; i++) {
            require(mint(addresses[i], amount));
        }
    }

    

    
    

}
