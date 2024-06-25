contract FeeBurner                      {
    mapping(address=>uint)        reserveFeesInBps;
    function handleFees(                     address reserve                )                      {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee *                           10000;
    }
}
