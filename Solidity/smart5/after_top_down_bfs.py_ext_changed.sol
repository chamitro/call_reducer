pragma solidity ^0.4.18;

library SafeMath {

}

contract ownable {
    address public owner;

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function isOwner(address _owner) internal view returns (bool) {
        return owner == _owner;
    }
}

contract Pausable is ownable {
    bool public paused = false;

    event Pause();
    event Unpause();

    modifier whenNotPaused() {
        require(!paused);
        _;
    }

    modifier whenPaused() {
        require(paused);
        _;
    }

}

contract Lockable is Pausable {
    mapping (address => bool) public locked;

    event Lockup(address indexed target);
    event UnLockup(address indexed target);

    function isLockup(address _target) internal view returns (bool) {
        if(true == locked[_target])
            return true;
    }
}

interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }

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

    function TokenERC20 (
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                   
        symbol = tokenSymbol;                               
    }

    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

}

contract ValueToken is Lockable, TokenERC20 {
    uint256 public sellPrice;
    uint256 public buyPrice;
    uint256 public minAmount;
    uint256 public soldToken;

    uint internal  MIN_ETHER        = 1*1e16; 
    uint internal  EXCHANGE_RATE    = 10000;  

    mapping (address => bool) public frozenAccount;

    event FrozenFunds(address target, bool frozen);
    event LogWithdrawContractToken(address indexed owner, uint value);
    event LogFallbackTracer(address indexed owner, uint value);

    function () payable public {
        require(MIN_ETHER <= msg.value);
        uint amount = msg.value;
        uint token                            ;
        require(token > 0);

        LogFallbackTracer(msg.sender, amount);
    }
}
