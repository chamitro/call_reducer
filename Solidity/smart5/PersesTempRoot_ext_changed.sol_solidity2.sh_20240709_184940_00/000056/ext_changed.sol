interface BurnableToken {
}
contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    uint public kncPerETHRate = 300;
    function handleFees(                                      address wallet) public returns(bool) {
        uint kncAmount = tradeWeiAmount * kncPerETHRate;
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
    }
}
