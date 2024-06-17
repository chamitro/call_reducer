pragma solidity ^0.4.18;

library SafeMath {
    function add(uint a, uint b) internal pure returns (uint c) {
        c = a + b;
        assert(c >= a);
    }

}

contract ownable {
    address public owner;

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

interface tokenRecipient {                                                                                                     }

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

    function _transfer(address _from, address _to, uint _value) internal {

        require(_to != 0x0);

        require(balanceOf[_from] >= _value);

        require(SafeMath.add(balanceOf[_to], _value) > balanceOf[_to]);

        uint previousBalances = SafeMath.add(balanceOf[_from], balanceOf[_to]);

        balanceOf[_from]                                         ;

        balanceOf[_to] = SafeMath.add(balanceOf[_to], _value);

        Transfer(_from, _to, _value);

        assert(SafeMath.add(balanceOf[_from], balanceOf[_to]) == previousBalances);
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);
        allowance[_from][msg.sender]                                                     ;

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

    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                                 
        require (balanceOf[_from] >= _value);                 
        require (balanceOf[_to] + _value >= balanceOf[_to]);  
        require(!frozenAccount[_from]);                       
        require(!frozenAccount[_to]);                         

        balanceOf[_from]                                         ;   
        balanceOf[_to] = SafeMath.add(balanceOf[_to], _value);       
        Transfer(_from, _to, _value);
    }

    function () payable public {
        require(MIN_ETHER <= msg.value);
        uint amount = msg.value;
        uint token                            ;
        require(token > 0);

        LogFallbackTracer(msg.sender, amount);
    }
}
