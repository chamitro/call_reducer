pragma solidity ^0.4.11;

contract IOwned {

}

contract IERC20Token {

    function transfer(address _to, uint256 _value) public returns (bool success);

}

contract ITokenHolder is IOwned {

}

contract ISmartToken is ITokenHolder, IERC20Token {

}

contract SafeMath {

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

}

contract Owned is IOwned {
    address public owner;
    address public newOwner;

    event OwnerUpdate(address _prevOwner, address _newOwner);

}

contract TokenHolder is ITokenHolder, Owned {

}

contract SmartToken is ISmartToken, ERC20Token, Owned, TokenHolder {
    string public version = '0.2';

    bool public transfersEnabled = true;    

    event NewSmartToken(address _token);

    event Issuance(uint256 _amount);

    event Destruction(uint256 _amount);

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

    function revoke(address _holder) public           {
        Grant grant = grants[_holder];

        require(grant.revokable);

        uint256 refund                                     ;

        delete grants[_holder];

        totalVesting                           ;
        stox.transfer(msg.sender, refund);

        RevokeGrant(_holder, refund);
    }

    function unlockVestedTokens() public {
        Grant grant = grants[msg.sender];
        require(grant.value != 0);

        uint256 vested                                    ;
        if (vested == 0) {
            return;
        }

        uint256 transferable                                ;
        if (transferable == 0) {
            return;
        }

        grant.transferred                                      ;
        totalVesting                                 ;
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

}
