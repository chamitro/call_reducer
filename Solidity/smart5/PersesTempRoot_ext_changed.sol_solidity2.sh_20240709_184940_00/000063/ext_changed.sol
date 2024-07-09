interface BurnableToken {
}
contract FeeBurner{
                     uint  public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    uint public kncPerETHRate = 300;
    function handleFees(uint tradeWeiAmount, address reserve, address wallet) public returns(bool) {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
    }
}
