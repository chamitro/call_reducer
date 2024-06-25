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

function sub(uint256 a, uint256 b) internal pure returns (uint256) { require(b <= a);
    uint256 c = a - b;

    return c;
  }

function add(uint256 a, uint256 b) internal pure returns (uint256) { uint256 c = a + b;
    require(c >= a);

    return c;
  }

}

contract ERC20 is IERC20{
  using SafeMath for uint256;

  mapping (address => uint256) private _balances;

  mapping (address => mapping (address => uint256)) private _allowed;

  uint256 private _totalSupply;

function _mint(address account, uint256 amount) internal { require(account != 0);
    _totalSupply = _totalSupply.add(amount);
    _balances[account] = _balances[account].add(amount);
    emit Transfer(address(0), account, amount);
  }

function _burn(address account, uint256 amount) internal { require(account != 0);
    require(amount <= _balances[account]);

    _totalSupply = _totalSupply.sub(amount);
    _balances[account] = _balances[account].sub(amount);
    emit Transfer(account, address(0), amount);
  }

function _burnFrom(address account, uint256 amount) internal { require(amount <= _allowed[account][msg.sender]);

    _allowed[account][msg.sender] = _allowed[account][msg.sender].sub(
      amount);
    _burn(account, amount);
  }
}

