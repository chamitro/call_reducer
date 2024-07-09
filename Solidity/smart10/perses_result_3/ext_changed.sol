library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    require(c / a == b);
    return c;
  }
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    require(b > 0);
    uint256 c = a / b;
    return c;
  }
}
library NameFilter {
}
contract SimpleAuction {
    using NameFilter for string;
    using SafeMath for *;
    address private top;
    mapping(address => uint) pendingReturns;
    mapping(address => string) giverNames;
    function bid() public payable {
        require(
            msg.value > 0.0001 ether,
            "?????"
        );
        pendingReturns[msg.sender] += (msg.value.div(10).mul(9));
        if(top != 0){
        }
        top = msg.sender;
        if(bytes(giverNames[msg.sender]).length== 0) {
            giverNames[msg.sender] = "#Anonymous";
        }
    }
}
