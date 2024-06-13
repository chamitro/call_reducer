pragma solidity ^0.4.24;




interface IERC20 { 



  



  event Transfer(
    address indexed from,
    address indexed to,
    uint256 value
  );

  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}



library SafeMath {

  
function mul(uint256 a, uint256 b) internal pure returns (uint256) {   
    if (a == 0) {
      return 0;
    }

    uint256 c = a * b;
    require(c / a == b);

    return c;
  }

  
function div(uint256 a, uint256 b) internal pure returns (uint256) { require(b > 0);
    uint256 c = a / b;
    

    return c;
  }

  


  
function add(uint256 a, uint256 b) internal pure returns (uint256) { uint256 c = a + b;
    require(c >= a);

    return c;
  }

  
function mod(uint256 a, uint256 b) internal pure returns (uint256) { require(b != 0);
    return a % b;
  }
}



contract ERC20 is IERC20 {
  using SafeMath for uint256;

  mapping (address => uint256) private _balances;

  mapping (address => mapping (address => uint256)) private _allowed;

  uint256 private _totalSupply;

  
function totalSupply() public view returns (uint256) { return _totalSupply;
  }

  


  


  


  


  


  


  


  
function _mint(address account, uint256 amount) internal { require(account != 0);
    _totalSupply = _totalSupply.add(amount);
    _balances[account] = _balances[account].add(amount);
    emit Transfer(address(0), account, amount);
  }

  
function _burn(address account, uint256 amount) internal { require(account != 0);
    require(amount <= _balances[account]);

    
    
    emit Transfer(account, address(0), amount);
  }

  
function _burnFrom(address account, uint256 amount) internal { require(amount <= _allowed[account][msg.sender]);

    
    
    _burn(account, amount);
  }
}



contract Girlfriend is ERC20 {

  string public constant name = "Girlfriend";
  string public constant symbol = "GF";
  uint8 public constant decimals = 9;

  uint256 public constant INITIAL_SUPPLY = 8000000000 * (10 ** uint256(decimals));


  constructor() public {
    _mint(msg.sender, INITIAL_SUPPLY);
  }

}
