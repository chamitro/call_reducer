pragma solidity 0.4.18;

library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {

    uint256 c = a / b;

    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

}

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

contract FxRates is Ownable {
    using SafeMath for uint256;

    struct Rate {
        string rate;
        string timestamp;
    }

    event RateUpdate(string symbol, uint256 updateNumber, string timestamp, string rate);

    uint256 public numberBtcUpdates = 0;

    mapping(uint256 => Rate) public btcUpdates;

    uint256 public numberEthUpdates = 0;

    mapping(uint256 => Rate) public ethUpdates;

}
