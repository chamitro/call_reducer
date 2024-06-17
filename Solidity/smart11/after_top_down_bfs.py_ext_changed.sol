pragma solidity ^0.4.11;

contract IOwned {

}

contract IERC20Token {

    function totalSupply() public  returns (uint256 totalSupply) { totalSupply; }
    function balanceOf(address _owner) public  returns (uint256 balance) { _owner; balance; }

    function transfer(address _to, uint256 _value) public returns (bool success);

}

contract ITokenHolder is IOwned {

}

contract ISmartToken is ITokenHolder, IERC20Token {

}

contract SafeMath {

    function safeAdd(uint256 _x, uint256 _y) internal returns (uint256) {
        uint256 z = _x + _y;
        assert(z >= _x);
        return z;
    }

    function safeSub(uint256 _x, uint256 _y) internal returns (uint256) {
        assert(_x >= _y);
        return _x - _y;
    }

}

contract ERC20Token is IERC20Token, SafeMath {
    string public standard = 'Token 0.1';
    string public name = '';
    string public symbol = '';
    uint8 public decimals = 0;
    uint256 public totalSupply = 0;
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    modifier validAddress(address _address) {
        require(_address != 0x0);
        _;
    }

    function transfer(address _to, uint256 _value)
        public
        validAddress(_to)
        returns (bool success)
    {
        balanceOf[msg.sender] = safeSub(balanceOf[msg.sender], _value);
        balanceOf[_to] = safeAdd(balanceOf[_to], _value);
        Transfer(msg.sender, _to, _value);
        return true;
    }

}

contract Owned is IOwned {
    address public owner;
    address public newOwner;

    event OwnerUpdate(address _prevOwner, address _newOwner);

    modifier ownerOnly {
        assert(msg.sender == owner);
        _;
    }

}

contract TokenHolder is ITokenHolder, Owned {

    modifier validAddress(address _address) {
        require(_address != 0x0);
        _;
    }

    modifier notThis(address _address) {
        require(_address != address(this));
        _;
    }

}

contract SmartToken is ISmartToken, ERC20Token, Owned, TokenHolder {
    string public version = '0.2';

    bool public transfersEnabled = true;    

    event NewSmartToken(address _token);

    event Issuance(uint256 _amount);

    event Destruction(uint256 _amount);

    modifier transfersAllowed {
        assert(transfersEnabled);
        _;
    }

    function transfer(address _to, uint256 _value) public transfersAllowed returns (bool success) {
        assert(super.transfer(_to, _value));

        if (_to == address(this)) {
            balanceOf[_to] -= _value;
            totalSupply -= _value;
            Destruction(_value);
        }

        return true;
    }

}

contract Ownable {
    address public owner;
    address public newOwnerCandidate;

    event OwnershipRequested(address indexed _by, address indexed _to);
    event OwnershipTransferred(address indexed _from, address indexed _to);

    modifier onlyOwner() {
        if (msg.sender != owner) {
            throw;
        }

        _;
    }

}

library SaferMath {
    function mul(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal returns (uint256) {

        uint256 c = a / b;

        return c;
    }

    function sub(uint256 a, uint256 b) internal returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }

    function min256(uint256 a, uint256 b) internal  returns (uint256) {
        return a < b ? a : b;
    }
}

contract StoxSmartToken is SmartToken {

}

contract Trustee is Ownable {
    using SaferMath for uint256;

    StoxSmartToken public stox;

    struct Grant {
        uint256 value;
        uint256 start;
        uint256 cliff;
        uint256 end;
        uint256 transferred;
        bool revokable;
    }

    mapping (address => Grant) public grants;

    uint256 public totalVesting;

    event NewGrant(address indexed _from, address indexed _to, uint256 _value);
    event UnlockGrant(address indexed _holder, uint256 _value);
    event RevokeGrant(address indexed _holder, uint256 _refund);

    function revoke(address _holder) public onlyOwner {
        Grant grant = grants[_holder];

        require(grant.revokable);

        uint256 refund = grant.value.sub(grant.transferred);

        delete grants[_holder];

        totalVesting = totalVesting.sub(refund);
        stox.transfer(msg.sender, refund);

        RevokeGrant(_holder, refund);
    }

    function calculateVestedTokens(Grant _grant, uint256 _time) private  returns (uint256) {

        if (_time < _grant.cliff) {
            return 0;
        }

        if (_time >= _grant.end) {
            return _grant.value;
        }

         return _grant.value.mul(_time.sub(_grant.start)).div(_grant.end.sub(_grant.start));
    }

    function unlockVestedTokens() public {
        Grant grant = grants[msg.sender];
        require(grant.value != 0);

        uint256 vested = calculateVestedTokens(grant, now);
        if (vested == 0) {
            return;
        }

        uint256 transferable = vested.sub(grant.transferred);
        if (transferable == 0) {
            return;
        }

        grant.transferred = grant.transferred.add(transferable);
        totalVesting = totalVesting.sub(transferable);
        stox.transfer(msg.sender, transferable);

        UnlockGrant(msg.sender, transferable);
    }
}

contract StoxSmartTokenSale is Ownable {
    using SaferMath for uint256;

    uint256 public  DURATION = 14 days;

    bool public isFinalized = false;
    bool public isDistributed = false;

    StoxSmartToken public stox;

    Trustee public trustee;

    uint256 public startTime = 0;
    uint256 public endTime = 0;
    address public fundingRecipient;

    uint256 public tokensSold = 0;

    uint256 public  ETH_CAP = 148000;
    uint256 public  EXCHANGE_RATE = 200; 
    uint256 public  TOKEN_SALE_CAP = ETH_CAP * EXCHANGE_RATE * 10 ** 18;

    event TokensIssued(address indexed _to, uint256 _tokens);

    modifier onlyDuringSale() {
        if (tokensSold >= TOKEN_SALE_CAP || now < startTime || now >= endTime) {
            throw;
        }

        _;
    }

    modifier onlyAfterSale() {
        if (!(tokensSold >= TOKEN_SALE_CAP || now >= endTime)) {
            throw;
        }

        _;
    }

}
