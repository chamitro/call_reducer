pragma solidity ^0.4.21;

library SafeMath {

}

contract ERC20Interface {

    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}

contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
}

contract Owned {
    address public owner;
    address public newOwner;

    event OwnershipTransferred(address indexed _from, address indexed _to);

}

contract NRM is ERC20Interface, Owned {
    using SafeMath for uint;

    bool public running = true;
    string public symbol;
    string public name;
    uint8 public decimals;
    uint _totalSupply;

    mapping(address => uint) balances;
    mapping(address => mapping(address => uint)) allowed;

    address public FreezeAddress;
    uint256 public FreezeTokens;
    uint256 public FreezeTokensReleaseTime;

    function approveAndCall(address spender, uint tokens, bytes data) public            returns (bool success) {
        allowed[msg.sender][spender] = tokens;
        emit Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }

    function multisend(address[] to, uint256[] values) public           returns (uint256) {
        for (uint256 i = 0; i < to.length; i++) {
            balances[owner]                                 ;
            balances[to[i]]                                 ;
            emit Transfer(owner, to[i], values[i]);
        }
        return(i);
    }
}
