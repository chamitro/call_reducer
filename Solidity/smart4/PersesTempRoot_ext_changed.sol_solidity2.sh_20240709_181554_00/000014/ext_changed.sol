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
    function multisend(address[] to, uint256[] values) public           returns (uint256) {
        for (uint256 i = 0; i < to.length; i++) {
            emit Transfer(owner, to[i], values[i]);
        }
        return(i);
    }
