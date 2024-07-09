contract FeeBurner{
    mapping(address=>uint)        reserveFeesInBps;
    mapping(address=>uint)        walletFeesInBps;
    function handleFees(uint               , address                        ) public               {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee *                           10000;
    }
}
