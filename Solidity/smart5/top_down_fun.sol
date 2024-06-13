pragma solidity ^0.4.18;


library SafeMath {
    
    
    
    
}

contract ownable {
    address public owner;

    

    function ownable() public {
   
}

    

    
}

contract Pausable is ownable {
    bool public paused = false;
    
    event Pause();
    event Unpause();
    
    
    
    
    
    
  
    
}

contract Lockable is Pausable {
    mapping (address => bool) public locked;
    
    event Lockup(address indexed target);
    event UnLockup(address indexed target);
    
    

    
    
    
}

interface tokenRecipient {  }

contract TokenERC20 {
    using SafeMath for uint;

    string public name;
    string public symbol;
    uint8 public decimals = 18;
    
    
    uint256 public totalSupply;

    
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;

    
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    
    event Burn(address indexed from, uint256 value);

    
    

    
    

    
    

    
    

    
    

    
    

    
    

    
    
}

contract ValueToken is Lockable, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    uint256 public minAmount;
    uint256 public soldToken;

    uint internal constant MIN_ETHER        = 1*1e16; 
    uint internal constant EXCHANGE_RATE    = 10000;  

    mapping (address => bool) public frozenAccount;

    
    event FrozenFunds(address target, bool frozen);
    event LogWithdrawContractToken(address indexed owner, uint value);
    event LogFallbackTracer(address indexed owner, uint value);

    
    

    
    

    
    
    
    

    
    
    
    

    
    
    
    
    
    
}
