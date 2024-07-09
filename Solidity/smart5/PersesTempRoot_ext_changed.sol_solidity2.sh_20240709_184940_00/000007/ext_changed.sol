interface BurnableToken {
}
    function handleFees(uint tradeWeiAmount, address reserve, address wallet) public returns(bool) {
        uint kncAmount = tradeWeiAmount * kncPerETHRate;
        uint fee = kncAmount * reserveFeesInBps[reserve] / 10000;
        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
        require(fee >= walletFee);
        uint feeToBurn = fee - walletFee;
        if (walletFee > 0) {
        }
        if (feeToBurn > 0) {
        }
        return true;
    }
