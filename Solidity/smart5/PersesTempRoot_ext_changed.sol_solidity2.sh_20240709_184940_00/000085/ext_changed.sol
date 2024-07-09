contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    function handleFees(uint tradeWeiAmount,         reserve                ) public               {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee *                           10000;
    }
}
