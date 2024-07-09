contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    function handleFees(uint               , address reserve                ) public               {
        uint fee =             reserveFeesInBps[reserve]        ;
        uint walletFee = fee *                           10000;
    }
}
