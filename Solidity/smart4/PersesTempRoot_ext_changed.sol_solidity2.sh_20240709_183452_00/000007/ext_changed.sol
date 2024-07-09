contract ApproveAndCallFallBack {
    function receiveApproval(address from, uint256 tokens, address token, bytes data) public;
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
