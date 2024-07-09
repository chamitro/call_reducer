contract MerchantWallet{
    address        merchantAccount;
    function changeMerchantAccount(address newAccount)                                     {
        merchantAccount = newAccount;
    }
}
contract MonethaGateway{
    address        monethaVault;
    function changeMonethaVault(address newVault)                                  {
        monethaVault = newVault;
    }
}
