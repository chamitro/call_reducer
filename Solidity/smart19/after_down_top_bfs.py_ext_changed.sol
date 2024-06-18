

pragma solidity 0.5.0;

contract Ownable {

    address private _owner;
    address private _pendingOwner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    constructor() public {

    }

    function transferOwnership(address _newOwner) public           {
        _pendingOwner = _newOwner;
    }

    function claimOwnership() public                  {
        emit OwnershipTransferred(_owner, _pendingOwner);
        _owner = _pendingOwner;
        _pendingOwner = address(0); 
    }

}

pragma solidity 0.5.0;

contract Operable is Ownable {

    address private _operator; 

    event OperatorChanged(address indexed previousOperator, address indexed newOperator);

    function updateOperator(address _newOperator) public           {
        require(_newOperator != address(0), "Cannot change the newOperator to the zero address");
        emit OperatorChanged(_operator, _newOperator);
        _operator = _newOperator;
    }

}

pragma solidity 0.5.0;

library SafeMath {

    function mul(uint256 a, uint256 b) internal pure returns (uint256) {

        if (a == 0) {
            return 0;
        }

        uint256 c = a * b;
        require(c / a == b);

        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) {

        require(b > 0);
        uint256 c = a / b;

        return c;
    }

    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b != 0);
        return a % b;
    }
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

    function setBalance(address _holder, uint256 _value) public              {
        balances[_holder] = _value;
    }

    function setTotalSupply(uint256 _value) public              {
        totalSupply = _value;
    }

}

pragma solidity 0.5.0;

interface ERC20Interface {  

    function balanceOf(address holder) external view returns (uint256);

    function allowance(address holder, address spender) external view returns (uint256);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed holder, address indexed spender, uint256 value);

}

pragma solidity 0.5.0;

contract ERC20StandardToken is ERC20Interface, Ownable {

    TokenStore public tokenStore;

    event TokenStoreSet(address indexed previousTokenStore, address indexed newTokenStore);
    event ChangeTokenName(string newName, string newSymbol);

    function setTokenStore(address _newTokenStore) public           returns (bool) {
        emit TokenStoreSet(address(tokenStore), _newTokenStore);
        tokenStore = TokenStore(_newTokenStore);
        return true;
    }

    function balanceOf(address _holder) public view returns (uint256) {
        return tokenStore.balances(_holder);
    }

    function allowance(address _holder, address _spender) public view returns (uint256) {
        return tokenStore.allowed(_holder, _spender);
    }

}

pragma solidity 0.5.0;

contract PausableToken is ERC20StandardToken {

    address private _pauser;
    bool public paused = false;

    event Pause();
    event Unpause();
    event PauserChanged(address indexed previousPauser, address indexed newPauser);

    function pause() public            {
        paused = true;
        emit Pause();
    }

    function unpause() public            {
        paused = false;
        emit Unpause();
    }

    function updatePauser(address _newPauser) public           {
        require(_newPauser != address(0), "Cannot update the newPauser to the zero address");
        emit PauserChanged(_pauser, _newPauser);
        _pauser = _newPauser;
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

    function setBlacklistStore(address _newblacklistStore) public           returns (bool) {
        emit BlacklistStoreSet(address(blacklistStore), _newblacklistStore);
        blacklistStore = BlacklistStore(_newblacklistStore);
        return true;
    }

    function updateBlacklister(address _newBlacklister) public           {
        require(_newBlacklister != address(0), "Cannot update the blacklister to the zero address");
        emit BlacklisterChanged(_blacklister, _newBlacklister);
        _blacklister = _newBlacklister;
    }

    function queryBlacklist(address _account) public view returns (uint256) {
        return blacklistStore.blacklisted(_account);
    }

    function changeBlacklist(address _account, uint256 _status) public                 {

        emit Blacklist(_account, _status);
    }

}

pragma solidity 0.5.0;

contract BurnableToken is BlacklistableToken {

    event Burn(address indexed burner, uint256 value);

    function burn(
        uint256 _value
    ) public                                          returns (bool success) {   

        emit Burn(msg.sender, _value);
        emit Transfer(msg.sender, address(0), _value);
        return true;
    }

}

pragma solidity 0.5.0;

contract MintableToken is BlacklistableToken {

    event MinterChanged(address indexed previousMinter, address indexed newMinter);
    event Mint(address indexed minter, address indexed to, uint256 value);

    address private _minter;

    function updateMinter(address _newMinter) public           {
        require(_newMinter != address(0), "Cannot update the newPauser to the zero address");
        emit MinterChanged(_minter, _newMinter);
        _minter = _newMinter;
    }

    function mint(
        address _to, 
        uint256 _value
    ) public                                                                         returns (bool) {
        require(_to != address(0), "Cannot mint to zero address");

        emit Mint(msg.sender, _to, _value);
        emit Transfer(address(0), _to, _value);
        return true;
    }

}

pragma solidity 0.5.0;

contract PingAnToken is BurnableToken, MintableToken {

    bool private initialized = true;

    function initialize(address _owner) public {
        require(!initialized, "already initialized");
        require(_owner != address(0), "Cannot initialize the owner to zero address");

        initialized = true;
    }

}
