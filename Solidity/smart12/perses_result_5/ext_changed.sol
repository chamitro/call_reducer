contract ERC20Basic {
  function transfer(address   , uint256      )        returns (bool);
}
contract ERC20 is ERC20Basic{
}
contract Ownable {
  address        owner;
}
contract SMILECOINToken is Ownable                   {
    function emergencyERC20Drain( ERC20 token, uint amount )           {
        token.transfer( owner, amount );
    }
}
