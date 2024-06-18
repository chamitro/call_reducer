

pragma solidity 0.5.0;

contract Ownable {

    address private _owner;
    address private _pendingOwner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    function transferOwnership(address _newOwner) public           {
        _pendingOwner = _newOwner;
    }

}

pragma solidity 0.5.0;

contract Operable is Ownable {

    address private _operator; 

    event OperatorChanged(address indexed previousOperator, address indexed newOperator);

}

pragma solidity 0.5.0;

library SafeMath {

}

pragma solidity 0.5.0;

contract TokenStore is Operable {

    using SafeMath for uint256;

    uint256 public totalSupply;

    string  public name = "PingAnToken";
    string  public symbol = "PAT";
    uint8 public decimals = 18;

    mapping (address => uint256) public balances;
    mapping (address => mapping (address => uint256)) public allowed;

}

pragma solidity 0.5.0;

interface ERC20Interface {  

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed holder, address indexed spender, uint256 value);

}

pragma solidity 0.5.0;

contract ERC20StandardToken is ERC20Interface, Ownable {

    TokenStore public tokenStore;

    event TokenStoreSet(address indexed previousTokenStore, address indexed newTokenStore);
    event ChangeTokenName(string newName, string newSymbol);

}

pragma solidity 0.5.0;

contract PausableToken is ERC20StandardToken {

    address private _pauser;
    bool public paused = false;

    event Pause();
    event Unpause();
    event PauserChanged(address indexed previousPauser, address indexed newPauser);

}

pragma solidity 0.5.0;

contract BlacklistStore is Operable {

    mapping (address => uint256) public blacklisted;

}

pragma solidity 0.5.0;

contract BlacklistableToken is PausableToken {

    BlacklistStore public blacklistStore;

    address private _blacklister;

    event BlacklisterChanged(address indexed previousBlacklister, address indexed newBlacklister);
    event BlacklistStoreSet(address indexed previousBlacklistStore, address indexed newblacklistStore);
    event Blacklist(address indexed account, uint256 _status);

}

pragma solidity 0.5.0;

contract BurnableToken is BlacklistableToken {

    event Burn(address indexed burner, uint256 value);

}

pragma solidity 0.5.0;

contract MintableToken is BlacklistableToken {

    event MinterChanged(address indexed previousMinter, address indexed newMinter);
    event Mint(address indexed minter, address indexed to, uint256 value);

    address private _minter;

}

pragma solidity 0.5.0;

contract PingAnToken is BurnableToken, MintableToken {

    bool private initialized = true;

}
