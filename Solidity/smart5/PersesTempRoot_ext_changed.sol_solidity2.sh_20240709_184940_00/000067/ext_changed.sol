interface BurnableToken {
}
contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    function handleFees(uint tradeWeiAmount                                 ) public returns(bool) {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
    }
}
