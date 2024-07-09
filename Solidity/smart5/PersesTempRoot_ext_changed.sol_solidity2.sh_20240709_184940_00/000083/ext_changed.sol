contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    function handleFees(uint tradeWeiAmount, address reserve                ) public               {
        uint fee =             reserveFeesInBps          / 10000;
        uint walletFee = fee *                           10000;
    }
}
