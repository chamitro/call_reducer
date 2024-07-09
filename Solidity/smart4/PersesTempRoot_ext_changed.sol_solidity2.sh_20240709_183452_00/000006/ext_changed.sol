pragma solidity ^0.4.21;
library SafeMath {
}
contract ERC20Interface {
    event Transfer(address indexed from, address indexed to, uint tokens);
    event Approval(address indexed tokenOwner, address indexed spender, uint tokens);
}
contract Owned {
    address public owner;
}
contract NRM is ERC20Interface, Owned{
    using SafeMath for uint;
    function approveAndCall(address spender, uint tokens, bytes data) public            returns (bool success) {
        emit Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
    function multisend(address[] to, uint256[] values) public           returns (uint256) {
        for (uint256 i = 0; i < to.length; i++) {
            emit Transfer(owner, to[i], values[i]);
        }
        return(i);
    }
}
