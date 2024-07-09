interface BurnableToken {
}
contract FeeBurner{
    mapping(address=>uint) public reserveFeesInBps;
    mapping(address=>uint) public walletFeesInBps;
    BurnableToken public knc;
}
