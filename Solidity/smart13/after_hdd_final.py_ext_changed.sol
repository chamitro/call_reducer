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
  function mul(uint256 a, uint256 b) internal  returns (uint256) {
    uint256 c = a * b;
    assert(a == 0 || c / a == b);
    return c;
  }

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

    function acceptPayment(address _merchantWallet, uint _monethaFee) external payable                           {
        require(_merchantWallet != 0x0);
        require(_monethaFee >= 0 && _monethaFee <= FEE_PERMILLE.mul(msg.value).div(1000)); 

        uint merchantIncome                             ;

        _merchantWallet.transfer(merchantIncome);
        monethaVault.transfer(_monethaFee);

        PaymentProcessed(_merchantWallet, merchantIncome, _monethaFee);
    }

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

    function payForOrder(
        uint _orderId,
        address _originAddress,
        uint _monethaFee
    ) external payable              
    {
        require(_orderId > 0);
        require(_originAddress != 0x0);
        require(msg.value > 0);

        monethaGateway.acceptPayment.value(msg.value)(merchantWallet, _monethaFee);

        OrderPaid(_orderId, _originAddress, msg.value, _monethaFee);
    }

}
