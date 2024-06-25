pragma solidity 0.4.18;

interface BurnableToken {

}

interface FeeBurnerInterface {
    function handleFees (uint tradeWeiAmount, address reserve, address wallet) public returns(bool);
}

contract FeeBurner is FeeBurnerInterface{

    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>address) public reserveKNCWallet;
    mapping(address=>uint) public walletFeesInBps;
    mapping(address=>uint) public reserveFeeToBurn;
    mapping(address=>mapping(address=>uint)) public reserveFeeToWallet;

    BurnableToken public knc;
    address public kyberNetwork;
    uint public kncPerETHRate = 300;

    event AssignFeeToWallet(address reserve, address wallet, uint walletFee);
    event AssignBurnFees(address reserve, uint burnFee);

    function handleFees(uint tradeWeiAmount, address reserve, address wallet) public returns(bool) {
        require(msg.sender == kyberNetwork);

        uint kncAmount = tradeWeiAmount * kncPerETHRate;
        uint fee = kncAmount * reserveFeesInBps[reserve] / 10000;

        uint walletFee = fee * walletFeesInBps[wallet] / 10000;
        require(fee >= walletFee);
        uint feeToBurn = fee - walletFee;

        if (walletFee > 0) {
            reserveFeeToWallet[reserve][wallet] += walletFee;
            AssignFeeToWallet(reserve, wallet, walletFee);
        }

        if (feeToBurn > 0) {
            AssignBurnFees(reserve, feeToBurn);
            reserveFeeToBurn[reserve] += feeToBurn;
        }

        return true;
    }

    event BurnAssignedFees(address indexed reserve, address sender);

    event SendWalletFees(address indexed wallet, address reserve, address sender);

}
