pragma solidity 0.4.18;

contract MerchantWallet{

    address public merchantAccount;

    function changeMerchantAccount(address newAccount) external                            {
        merchantAccount = newAccount;
    }
}

library SafeMath {

}

contract MonethaGateway{

    using SafeMath for uint256;

    address public monethaVault;

    function changeMonethaVault(address newVault) external                         {
        monethaVault = newVault;
    }

}

