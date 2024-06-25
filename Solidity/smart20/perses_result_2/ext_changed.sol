interface IERC20 {
}
contract ERC20          {
    function transferFrom(address     , address   , uint256      ) public returns (bool)
                                                                          ;
}
contract PumaPayToken is IERC20, ERC20               {
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
