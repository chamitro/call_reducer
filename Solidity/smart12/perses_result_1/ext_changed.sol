contract ERC20Basic {
  function transfer(address   , uint256      )        returns (bool);
}
contract ERC20 is ERC20Basic {
}
contract StandardToken                      {
}
contract Ownable {
  address        owner;
}
contract Pausable is Ownable {
}
contract PausableToken is StandardToken, Pausable {
}
contract SMILECOINToken is PausableToken {
    function emergencyERC20Drain( ERC20 token, uint amount )           {
        token.transfer( owner, amount );
    }
}
