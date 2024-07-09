library SafeMath {
}
contract ERC20Interface {
}
contract Owned {
    address public owner;
}
contract NRM is ERC20Interface, Owned{
    function approveAndCall(address spender, uint tokens, bytes data) public            returns (bool success)
                                                  ;
    function multisend(address[] to, uint256[] values) public           returns (uint256)
                 ;
}
