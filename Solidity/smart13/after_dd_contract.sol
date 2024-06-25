pragma solidity 0.4.18;

contract Contactable           {

    string public contactInformation;

}

contract MerchantWallet is Contactable{

    string  VERSION = "0.3";

    address public merchantAccount;

    bytes32 public merchantIdHash;

    mapping (string=>string) profileMap;

    mapping (string=>string) paymentSettingsMap;

    mapping (string=>uint32) compositeReputationMap;

    uint8 public  REPUTATION_DECIMALS = 4;

    function changeMerchantAccount(address newAccount) external                            {
        merchantAccount = newAccount;
    }
}

library SafeMath {

}

contract MonethaGateway is Contactable{

    using SafeMath for uint256;

    string  VERSION = "0.4";

    uint public  FEE_PERMILLE = 15;

    address public monethaVault;

    address public admin;

    event PaymentProcessed(address merchantWallet, uint merchantIncome, uint monethaIncome);

    function changeMonethaVault(address newVault) external                         {
        monethaVault = newVault;
    }

}

