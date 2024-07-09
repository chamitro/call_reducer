interface BurnableToken {
}
contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    uint public kncPerETHRate = 300;
    function handleFees(uint tradeWeiAmount, address reserve, address wallet) public returns(bool)
                           {
        }
}
