pragma solidity ^0.4.18;

library SafeMath {

    function div(uint a, uint b) internal pure returns (uint c) {
        assert(b > 0);
        c = a / b;
        assert(a == b * c + a % b);
    }
}

contract ownable {
    address public owner;

    function transferOwnership(address newOwner)           public {
        owner = newOwner;
    }

}

contract Pausable is ownable {
    bool public paused = false;

    event Pause();
    event Unpause();

    function pause()                         public returns (bool success) {
        paused = true;
        Pause();
        return true;
    }

    function unpause()                      public returns (bool success) {
        paused = false;
        Unpause();
        return true;
    }
}

contract Lockable is Pausable {
    mapping (address => bool) public locked;

    event Lockup(address indexed target);
    event UnLockup(address indexed target);

    function lockup(address _target)           public returns (bool success) {

        locked[_target] = true;
        Lockup(_target);
        return true;
    }

    function unlockup(address _target)           public returns (bool success) {

        delete locked[_target];
        UnLockup(_target);
        return true;
    }

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

    function transfer(address _to, uint256 _value) public returns (bool success) {

        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);
        allowance[_from][msg.sender]                                                     ;

        return true;
    }

    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {

            return true;
        }
    }

    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);                               
        balanceOf[msg.sender]                                              ;    
        totalSupply                                    ;                        
        Burn(msg.sender, _value);
        return true;
    }

    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);                        
        require(_value <= allowance[_from][msg.sender]);            
        balanceOf[_from]                                         ;  
        allowance[_from][msg.sender]                                                     ; 
        totalSupply                                    ;            
        Burn(_from, _value);
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

    function ValueToken (
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    )                                                   public {

    }

    function mintToken(address target, uint256 mintedAmount)           public {
        balanceOf[target]                                                ;
        totalSupply                                          ;
        Transfer(0, this, mintedAmount);
        Transfer(this, target, mintedAmount);
    }

    function freezeAccount(address target, bool freeze)           public {

        require(!frozenAccount[target]);

        frozenAccount[target] = freeze;
        FrozenFunds(target, freeze);
    }

    function withdrawContractToken(uint _value)           public returns (bool success) {

        LogWithdrawContractToken(msg.sender, _value);
        return true;
    }

    function () payable public {
        require(MIN_ETHER <= msg.value);
        uint amount = msg.value;
        uint token                            ;
        require(token > 0);

        LogFallbackTracer(msg.sender, amount);
    }
}
