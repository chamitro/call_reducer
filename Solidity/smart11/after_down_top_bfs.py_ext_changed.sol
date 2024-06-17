pragma solidity ^0.4.11;

contract IOwned {

}

contract IERC20Token {

    function transfer(address _to, uint256 _value) public returns (bool success);

    function approve(address _spender, uint256 _value) public returns (bool success);
}

contract ITokenHolder is IOwned {
    function withdrawTokens(IERC20Token _token, address _to, uint256 _amount) public;
}

contract ISmartToken is ITokenHolder, IERC20Token {

    function destroy(address _from, uint256 _amount) public;
}

contract SafeMath {

    function safeMul(uint256 _x, uint256 _y) internal returns (uint256) {
        uint256 z = _x * _y;
        assert(_x == 0 || z / _x == _y);
        return z;
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

    function transfer(address _to, uint256 _value)
        public

        returns (bool success)
    {
        balanceOf[msg.sender]                                         ;
        balanceOf[_to]                                  ;
        Transfer(msg.sender, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value)
        public

        returns (bool success)
    {

        require(_value == 0 || allowance[msg.sender][_spender] == 0);

        allowance[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }
}

contract Owned is IOwned {
    address public owner;
    address public newOwner;

    event OwnerUpdate(address _prevOwner, address _newOwner);

}

contract TokenHolder is ITokenHolder, Owned {

    function withdrawTokens(IERC20Token _token, address _to, uint256 _amount)
        public

    {
        assert(_token.transfer(_to, _amount));
    }
}

contract SmartToken is ISmartToken, ERC20Token, Owned, TokenHolder {
    string public version = '0.2';

    bool public transfersEnabled = true;    

    event NewSmartToken(address _token);

    event Issuance(uint256 _amount);

    event Destruction(uint256 _amount);

    function destroy(address _from, uint256 _amount)
        public

    {
        balanceOf[_from]                                     ;
        totalSupply                                ;

        Transfer(_from, this, _amount);
        Destruction(_amount);
    }

    function transfer(address _to, uint256 _value) public                  returns (bool success) {
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

}

contract StoxSmartToken is SmartToken {
    function StoxSmartToken()                               {

    }
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

    function Trustee(StoxSmartToken _stox) {
        require(_stox != address(0));

        stox = _stox;
    }

    function revoke(address _holder) public           {
        Grant grant = grants[_holder];

        require(grant.revokable);

        uint256 refund = grant.value.sub(grant.transferred);

        delete grants[_holder];

        totalVesting = totalVesting.sub(refund);
        stox.transfer(msg.sender, refund);

        RevokeGrant(_holder, refund);
    }

    function vestedTokens(address _holder, uint256 _time) public  returns (uint256) {
        Grant grant = grants[_holder];
        if (grant.value == 0) {
            return 0;
        }

        return calculateVestedTokens(grant, _time);
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

        grant.transferred                                      ;
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

    function StoxSmartTokenSale(address _stox, address _fundingRecipient, uint256 _startTime) {
        require(_stox != address(0));
        require(_fundingRecipient != address(0));
        require(_startTime > now);

        stox                        ;

        fundingRecipient = _fundingRecipient;
        startTime = _startTime;
        endTime = startTime + DURATION;
    }

    function distributePartnerTokens() external           {
        require(!isDistributed);

        assert(tokensSold == 0);
        assert(stox.totalSupply() == 0);

        isDistributed = true;
    }

    function finalize() external               {
        if (isFinalized) {
            throw;
        }

        trustee = new Trustee(stox);

        uint256 unsoldTokens = tokensSold;

        uint256 strategicPartnershipTokens = unsoldTokens.mul(55).div(100);

        isFinalized = true;
    }

    function create(address _recipient) public payable                {
        require(_recipient != address(0));
        require(msg.value > 0);

        assert(isDistributed);

        uint256 tokens                                                                                 ;
        uint256 contribution = tokens.div(EXCHANGE_RATE);

        fundingRecipient.transfer(contribution);

        uint256 refund = msg.value.sub(contribution);
        if (refund > 0) {
            msg.sender.transfer(refund);
        }
    }

    function transferSmartTokenOwnership(address _newOwnerCandidate) external           {

    }

    function acceptSmartTokenOwnership() external           {

    }

    function transferTrusteeOwnership(address _newOwnerCandidate) external           {

    }

    function acceptTrusteeOwnership() external           {

    }
}
