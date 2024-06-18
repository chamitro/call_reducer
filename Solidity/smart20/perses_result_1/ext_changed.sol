contract ERC20           {
    function transferFrom(address     , address   , uint256      ) public returns (bool)
                                                                          ;
}
contract ERC20Mintable is ERC20             {
}
contract PumaPayToken is ERC20Mintable {
}
contract PumaPayPullPayment                   {
    PumaPayToken        token;
    function executePullPayment(address _client                    )
    public
    {
        uint256 amountInPMA;
        token.transferFrom(
            _client,
                         _client                             ,
            amountInPMA
        );
    }
}
