pragma solidity ^0.4.11;

contract ISmartToken{

}

contract SafeMath {

}

contract ERC20Token is SafeMath{
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

        Transfer(msg.sender, _to, _value);
        return true;
    }

}

library SaferMath {

}

contract StoxSmartToken is ERC20Token, ISmartToken{

}

contract Trustee{
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

        uint256 refund                                     ;

        totalVesting                           ;
        stox.transfer(msg.sender, refund);

        RevokeGrant(_holder, refund);
    }

    function unlockVestedTokens() public {

        uint256 vested                                    ;
        if (vested == 0) {
            return;
        }

        uint256 transferable                                ;
        if (transferable == 0) {
            return;
        }

        totalVesting                                 ;
        stox.transfer(msg.sender, transferable);

        UnlockGrant(msg.sender, transferable);
    }
}

contract StoxSmartTokenSale{
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
