pragma solidity 0.4.18;

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  function transferOwnership(address newOwner)           public {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

contract Restricted is Ownable {

    event MonethaAddressSet(
        address _address,
        bool _isMonethaAddress
    );

    mapping (address => bool) public isMonethaAddress;

    function setMonethaAddress(address _address, bool _isMonethaAddress)           public {
        isMonethaAddress[_address] = _isMonethaAddress;

        MonethaAddressSet(_address, _isMonethaAddress);
    }
}

contract SafeDestructible is Ownable {
    function destroy()           public {
        require(this.balance == 0);
        selfdestruct(owner);
    }
}

contract Pausable is Ownable {
  event Pause();
  event Unpause();

  bool public paused = false;

  function pause()                         public {
    paused = true;
    Pause();
  }

  function unpause()                      public {
    paused = false;
    Unpause();
  }
}

contract Contactable is Ownable{

    string public contactInformation;

    function setContactInformation(string info)           public {
         contactInformation = info;
     }
}

contract MerchantWallet is Pausable, SafeDestructible, Contactable, Restricted {

    string  VERSION = "0.3";

    address public merchantAccount;

    bytes32 public merchantIdHash;

    mapping (string=>string) profileMap;

    mapping (string=>string) paymentSettingsMap;

    mapping (string=>uint32) compositeReputationMap;

    uint8 public  REPUTATION_DECIMALS = 4;

    function MerchantWallet(address _merchantAccount, string _merchantId) public {
        require(_merchantAccount != 0x0);
        require(bytes(_merchantId).length > 0);

        merchantAccount = _merchantAccount;
        merchantIdHash = keccak256(_merchantId);
    }

    function setProfile(
        string profileKey,
        string profileValue,
        string repKey,
        uint32 repValue
    ) external          
    {
        profileMap[profileKey] = profileValue;

        if (bytes(repKey).length != 0) {
            compositeReputationMap[repKey] = repValue;
        }
    }

    function setPaymentSettings(string key, string value) external           {
        paymentSettingsMap[key] = value;
    }

    function setCompositeReputation(string key, uint32 value) external             {
        compositeReputationMap[key] = value;
    }

    function withdraw(uint amount) external {

    }

    function sendTo(address beneficiary, uint amount) external                            {

    }

    function changeMerchantAccount(address newAccount) external                            {
        merchantAccount = newAccount;
    }
}

contract Destructible is Ownable {

  function destroy()           public {
    selfdestruct(owner);
  }

  function destroyAndSend(address _recipient)           public {
    selfdestruct(_recipient);
  }
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

  function add(uint256 a, uint256 b) internal  returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
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

    function MonethaGateway(address _monethaVault, address _admin) public {
        require(_monethaVault != 0x0);
        monethaVault = _monethaVault;

    }

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

    function setMonethaAddress(address _address, bool _isMonethaAddress) public {
        require(msg.sender == admin || msg.sender == owner);

        isMonethaAddress[_address] = _isMonethaAddress;

        MonethaAddressSet(_address, _isMonethaAddress);
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

    function PrivatePaymentProcessor(
        string _merchantId,
        MonethaGateway _monethaGateway,
        MerchantWallet _merchantWallet
    ) public
    {
        require(bytes(_merchantId).length > 0);

        merchantIdHash = keccak256(_merchantId);

    }

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

    function refundPayment(
        uint _orderId,
        address _clientAddress,
        string _refundReason
    ) external payable                          
    {
        require(_orderId > 0);
        require(_clientAddress != 0x0);
        require(msg.value > 0);
        require(WithdrawState.Null == withdrawals[_orderId].state);

        withdrawals[_orderId] = Withdraw({
            state: WithdrawState.Pending,
            amount: msg.value,
            clientAddress: _clientAddress
            });

        PaymentRefunding(_orderId, _clientAddress, msg.value, _refundReason);
    }

    function withdrawRefund(uint _orderId)
    external              
    {
        Withdraw storage withdraw = withdrawals[_orderId];
        require(WithdrawState.Pending == withdraw.state);

        address clientAddress = withdraw.clientAddress;
        uint amount = withdraw.amount;

        withdraw.state = WithdrawState.Withdrawn;

        clientAddress.transfer(amount);

        PaymentWithdrawn(_orderId, clientAddress, amount);
    }

}
