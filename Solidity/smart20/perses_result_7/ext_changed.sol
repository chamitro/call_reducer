interface IERC20 {
    function transferFrom(address     , address   , uint256      ) external returns (bool);
}
contract ERC20 is IERC20{
}
contract PumaPayToken is ERC20{
}
contract PumaPayPullPayment{
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
