pragma solidity 0.4.18;

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

contract Restricted is Ownable {

    event MonethaAddressSet(
        address _address,
        bool _isMonethaAddress
    );

    mapping (address => bool) public isMonethaAddress;

}

contract SafeDestructible is Ownable {

}

contract Pausable is Ownable {
  event Pause();
  event Unpause();

  bool public paused = false;

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

    function changeMerchantAccount(address newAccount) external                            {
        merchantAccount = newAccount;
    }
}

contract Destructible is Ownable {

}

library SafeMath {

}

contract MonethaGateway is Pausable, Contactable, Destructible, Restricted {

    using SafeMath for uint256;

    string  VERSION = "0.4";

    uint public  FEE_PERMILLE = 15;

    address public monethaVault;

    address public admin;

    event PaymentProcessed(address merchantWallet, uint merchantIncome, uint monethaIncome);

    function changeMonethaVault(address newVault) external                         {
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
