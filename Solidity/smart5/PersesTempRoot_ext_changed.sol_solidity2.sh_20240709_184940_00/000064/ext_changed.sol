interface BurnableToken {
}
contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
            address        public walletFeesInBps;
    uint public kncPerETHRate = 300;
    function handleFees(uint tradeWeiAmount, address reserve, address wallet) public returns(bool) {
        uint fee =             reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
    }
}
