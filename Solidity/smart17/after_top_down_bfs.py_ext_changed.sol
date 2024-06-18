

pragma solidity 0.5.0;

contract Ownable {

    address private _owner;
    address private _pendingOwner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    modifier onlyPendingOwner() {
        require(msg.sender == _pendingOwner, "msg.sender should be onlyPendingOwner");
        _;
    }

    modifier onlyOwner() {
        require(msg.sender == _owner, "msg.sender should be owner");
        _;
    }

    function setOwner(address _newOwner) internal {
        _owner = _newOwner;
    }

}

pragma solidity 0.5.0;

contract Operable is Ownable {

    address private _operator; 

    event OperatorChanged(address indexed previousOperator, address indexed newOperator);

    modifier onlyOperator() {
        require(msg.sender == _operator, "msg.sender should be operator");
        _;
    }

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

    modifier whenNotPaused() {
        require(!paused, "state shouldn't be paused");
        _;
    }

    modifier onlyPauser() {
        require(msg.sender == _pauser, "msg.sender should be pauser");
        _;
    }

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

    modifier notBlacklisted(address _account) {
        require(blacklistStore.blacklisted(_account) == 0, "Account in the blacklist");
        _;
    }

    modifier onlyBlacklister() {
        require(msg.sender == _blacklister, "msg.sener should be blacklister");
        _;
    }

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

    modifier onlyMinter() {
        require(msg.sender == _minter, "msg.sender should be minter");
        _;
    }

}

pragma solidity 0.5.0;

contract PingAnToken is BurnableToken, MintableToken {

    bool private initialized = true;

    function initialize(address _owner) public {
        require(!initialized, "already initialized");
        require(_owner != address(0), "Cannot initialize the owner to zero address");
        setOwner(_owner);
        initialized = true;
    }

}
