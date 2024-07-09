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
}
contract NRM is ERC20Interface, Owned{
    using SafeMath for uint;
    function approveAndCall(address spender, uint tokens, bytes data) public            returns (bool success) {
        emit Approval(msg.sender, spender, tokens);
        ApproveAndCallFallBack(spender).receiveApproval(msg.sender, tokens, this, data);
        return true;
    }
}
