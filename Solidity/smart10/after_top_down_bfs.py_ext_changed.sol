pragma solidity ^0.4.22;

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

    address private boss;

    uint public fees;

    address private top;

    address private loser;

    uint private topbid;

    uint private loserbid;

    mapping(address => uint) pendingReturns;

    mapping(address => string) giverNames;

    mapping(address => string) giverMessages;

    function bid() public payable {

        require(
            msg.value > 0.0001 ether,
            "?????"
        );

        require(
            msg.value > topbid,
            "loser fuck off."
        );

        pendingReturns[msg.sender] += (msg.value.div(10).mul(9));
        fees+= msg.value.div(10);

        if(top != 0){
            loser = top;
            loserbid = topbid;
        }
        top = msg.sender;
        topbid = msg.value;

        if(bytes(giverNames[msg.sender]).length== 0) {
            giverNames[msg.sender] = "#Anonymous";
            giverMessages[msg.sender] = "#Nothing";
        }
    }

    function getInfo(address _add) public view returns (string,string){
        return (giverNames[_add],giverMessages[_add]);
    }

}
