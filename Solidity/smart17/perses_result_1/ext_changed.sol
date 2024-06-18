contract Ownable {
    address         _owner;
}
interface ERC20Interface {
}
contract ERC20StandardToken is ERC20Interface, Ownable {
}
contract PausableToken is ERC20StandardToken {
}
contract BlacklistableToken is PausableToken {
}
contract BurnableToken                       {
}
contract MintableToken is BlacklistableToken {
}
contract PingAnToken is BurnableToken, MintableToken {
    function initialize(address _owner) public
                                                    ;
}
