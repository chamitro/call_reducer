pragma solidity 0.4.18;

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

}

contract Restricted is Ownable {

    event MonethaAddressSet(
        address _address,
        bool _isMonethaAddress
    );

    mapping (address => bool) public isMonethaAddress;

    modifier onlyMonetha() {
        require(isMonethaAddress[msg.sender]);
        _;
    }

}

contract SafeDestructible is Ownable {

}

contract Pausable is Ownable {
  event Pause();
  event Unpause();

  bool public paused = false;

  modifier whenNotPaused() {
    require(!paused);
    _;
  }

  modifier whenPaused() {
    require(paused);
    _;
  }

}

contract Contactable is Ownable{

    string public contactInformation;

}

contract MerchantWallet is Pausable, SafeDestructible, Contactable, Restricted {

    string  VERSION = "0.3";

    address public merchantAccount;

    bytes32 public merchantIdHash;

    mapping (string=>string) profileMap;

    mapping (string=>string) paymentSettingsMap;

    mapping (string=>uint32) compositeReputationMap;

    uint8 public  REPUTATION_DECIMALS = 4;

    modifier onlyMerchant() {
        require(msg.sender == merchantAccount);
        _;
    }

    function changeMerchantAccount(address newAccount) external onlyMerchant whenNotPaused {
        merchantAccount = newAccount;
    }
}

contract Destructible is Ownable {

}

library SafeMath {

  function div(uint256 a, uint256 b) internal  returns (uint256) {

    uint256 c = a / b;

    return c;
  }

}

contract MonethaGateway is Pausable, Contactable, Destructible, Restricted {

    using SafeMath for uint256;

    string  VERSION = "0.4";

    uint public  FEE_PERMILLE = 15;

    address public monethaVault;

    address public admin;

    event PaymentProcessed(address merchantWallet, uint merchantIncome, uint monethaIncome);

    function changeMonethaVault(address newVault) external onlyOwner whenNotPaused {
        monethaVault = newVault;
    }

}

contract PrivatePaymentProcessor is Pausable, Destructible, Contactable, Restricted {

    using SafeMath for uint256;

    string  VERSION = "0.4";

    event OrderPaid(
        uint indexed _orderId,
        address indexed _originAddress,
        uint _price,
        uint _monethaFee
    );

    event PaymentsProcessed(
        address indexed _merchantAddress,
        uint _amount,
        uint _fee
    );

    event PaymentRefunding(
         uint indexed _orderId,
         address indexed _clientAddress,
         uint _amount,
         string _refundReason);

    event PaymentWithdrawn(
        uint indexed _orderId,
        address indexed _clientAddress,
        uint amount);

    MonethaGateway public monethaGateway;

    MerchantWallet public merchantWallet;

    bytes32 public merchantIdHash;

    enum WithdrawState {Null, Pending, Withdrawn}

    struct Withdraw {
        WithdrawState state;
        uint amount;
        address clientAddress;
    }

    mapping (uint=>Withdraw) public withdrawals;

}
