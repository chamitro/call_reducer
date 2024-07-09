library SafeMath {
}
contract ERC20Interface {
}
contract ApproveAndCallFallBack {
    function receiveApproval(                                             bytes     ) public;
}
contract Owned {
    address public owner;
}
contract NRM is ERC20Interface, Owned{
    function approveAndCall(address spender, uint tokens, bytes data) public            returns (bool success)
                                                  ;
    function multisend(                              ) public           returns (uint256)
                 ;
}
