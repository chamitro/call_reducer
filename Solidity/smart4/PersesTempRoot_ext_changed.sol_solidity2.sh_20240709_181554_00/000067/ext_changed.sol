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
    function approveAndCall(                              bytes     ) public
                                                  ;
    function multisend(address[]                     ) public           returns (uint256)
                 ;
}
