

library BytesDeserializer {

}

library SafeMath {

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract Exchange         {
    using SafeMath for uint256;
    using BytesDeserializer for bytes;

    string public  ROLE_FORCED = "forced";
    string public  ROLE_TRANSFER_TOKENS = "transfer tokens";
    string public  ROLE_TRANSFER_INVESTOR_TOKENS = "transfer investor tokens";
    string public  ROLE_CLAIM = "claim";
    string public  ROLE_WITHDRAW = "withdraw";
    string public  ROLE_TRADE = "trade";
    string public  ROLE_CHANGE_DELAY = "change delay";
    string public  ROLE_SET_FEEACCOUNT = "set feeaccount";
    string public  ROLE_TOKEN_WHITELIST = "token whitelist user";

    mapping(bytes32 => bool) public withdrawn;

    mapping(bytes32 => bool) public transferred;

    mapping(address => bool) public tokenWhitelist;

    mapping(address => uint256) public tokensTotal;

    mapping(address => mapping(address => uint256)) public balanceOf;

    mapping (bytes32 => uint256) public orderFilled;

    address public feeAccount;

    uint256 public delay;

    event TokenWhitelistUpdated(address token, bool status);

    event FeeAccountChanged(address newFeeAccocunt);

    event DelayChanged(uint256 newDelay);

    event Deposited(address token, address who, uint256 amount, uint256 balance);

    event Forced(address token, address who, uint256 amount);

    event Withdrawn(address token, address who, uint256 amount, uint256 balance);

    event Requested(address token, address who, uint256 amount, uint256 index);

    event TransferredInvestorTokens(address, address, address, uint256);

    event TransferredTokens(address, address, address, uint256, uint256, uint256);

    event OrderExecuted(
        bytes32 orderHash,
        address maker,
        address baseToken,
        address quoteToken,
        address feeToken,
        uint256 baseAmountFilled,
        uint256 quoteAmountFilled,
        uint256 feePaid,
        uint256 baseTokenBalance,
        uint256 quoteTokenBalance,
        uint256 feeTokenBalance
    );

    struct Withdrawal {
      address user;
      address token;
      uint256 amount;
      uint256 createdAt;
      bool executed;
    }

    Withdrawal[] withdrawals;

    enum OrderType {Buy, Sell}

    struct Order {
      OrderType orderType;
      address maker;
      address baseToken;
      address quoteToken;
      address feeToken;
      uint256 amount;
      uint256 priceNumerator;
      uint256 priceDenominator;
      uint256 feeNumerator;
      uint256 feeDenominator;
      uint256 expiresAt;
      uint256 nonce;
    }

    function checkBalances(address addr, address boughtToken, address soldToken, address feeToken, uint256 boughtAmount, uint256 soldAmount, uint256 feeAmount) private {
      if (feeToken == soldToken) {
        require (balanceOf[soldToken][addr] >= (soldAmount.add(feeAmount)));
      } else {
        if (feeToken == boughtToken) {
          require (balanceOf[feeToken][addr].add(boughtAmount) >= feeAmount);
        } else {
          require (balanceOf[feeToken][addr] >= feeAmount);
        }
        require (balanceOf[soldToken][addr] >= soldAmount);
      }
    }
}
