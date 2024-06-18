

pragma solidity 0.5.0;

interface IERC20 {

    function transferFrom(address from, address to, uint256 value) external returns (bool);

    event Transfer(address indexed from, address indexed to, uint256 value);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

pragma solidity 0.5.0;

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

    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a);
        uint256 c = a - b;

        return c;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a);

        return c;
    }

}

pragma solidity 0.5.0;

contract ERC20 is IERC20 {
    using SafeMath for uint256;

    mapping (address => uint256) private _balances;

    mapping (address => mapping (address => uint256)) private _allowed;

    uint256 private _totalSupply;

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _allowed[from][msg.sender] = _allowed[from][msg.sender].sub(value);

        emit Approval(from, msg.sender, _allowed[from][msg.sender]);
        return true;
    }

    function _transfer(address from, address to, uint256 value) internal {
        require(to != address(0));

        _balances[from] = _balances[from].sub(value);
        _balances[to] = _balances[to].add(value);
        emit Transfer(from, to, value);
    }

}

pragma solidity 0.5.0;

library Roles {
    struct Role {
        mapping (address => bool) bearer;
    }

    function add(Role storage role, address account) internal {
        require(account != address(0));
        require(!has(role, account));

        role.bearer[account] = true;
    }

    function has(Role storage role, address account) internal view returns (bool) {
        require(account != address(0));
        return role.bearer[account];
    }
}

pragma solidity 0.5.0;

contract MinterRole {
    using Roles for Roles.Role;

    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);

    Roles.Role private _minters;

    modifier onlyMinter() {

        _;
    }

}

pragma solidity 0.5.0;

contract ERC20Mintable is ERC20, MinterRole {

}

pragma solidity 0.5.0;

contract PumaPayToken is ERC20Mintable {

    string public name = "PumaPay";
    string public symbol = "PMA";
    uint8 public decimals = 18;

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
}

pragma solidity 0.5.0;

contract PayableOwnable {
    address payable private _owner;

    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

    function owner() public view returns (address payable) {
        return _owner;
    }

    modifier onlyOwner() {

        _;
    }

}

pragma solidity 0.5.0;

contract PumaPayPullPayment is PayableOwnable {

    using SafeMath for uint256;

    event LogExecutorAdded(address executor);
    event LogExecutorRemoved(address executor);
    event LogSetConversionRate(string currency, uint256 conversionRate);

    event LogPaymentRegistered(
        address customerAddress,
        bytes32 paymentID,
        bytes32 businessID,
        bytes32 uniqueReferenceID
    );
    event LogPaymentCancelled(
        address customerAddress,
        bytes32 paymentID,
        bytes32 businessID,
        bytes32 uniqueReferenceID
    );
    event LogPullPaymentExecuted(
        address customerAddress,
        bytes32 paymentID,
        bytes32 businessID,
        bytes32 uniqueReferenceID
    );

    uint256 constant private DECIMAL_FIXER = 10 ** 10; 
    uint256 constant private FIAT_TO_CENT_FIXER = 100;    
    uint256 constant private OVERFLOW_LIMITER_NUMBER = 10 ** 20; 

    uint256 constant private ONE_ETHER = 1 ether;         
    uint256 constant private FUNDING_AMOUNT = 1 ether;  
    uint256 constant private MINIMUM_AMOUNT_OF_ETH_FOR_OPERATORS = 0.15 ether; 

    PumaPayToken public token;

    mapping(string => uint256) private conversionRates;
    mapping(address => bool) public executors;
    mapping(address => mapping(address => PullPayment)) public pullPayments;

    struct PullPayment {
        bytes32 paymentID;                      
        bytes32 businessID;                     
        bytes32 uniqueReferenceID;              
        string currency;                        
        uint256 initialPaymentAmountInCents;    
        uint256 fiatAmountInCents;              
        uint256 frequency;                      
        uint256 numberOfPayments;               
        uint256 startTimestamp;                 
        uint256 nextPaymentTimestamp;           
        uint256 lastPaymentTimestamp;           
        uint256 cancelTimestamp;                
        address treasuryAddress;                
    }

    modifier isExecutor() {
        require(executors[msg.sender], "msg.sender not an executor");
        _;
    }

    modifier executorExists(address _executor) {
        require(executors[_executor], "Executor does not exists.");
        _;
    }

    modifier executorDoesNotExists(address _executor) {
        require(!executors[_executor], "Executor already exists.");
        _;
    }

    modifier paymentExists(address _client, address _pullPaymentExecutor) {

        _;
    }

    modifier paymentNotCancelled(address _client, address _pullPaymentExecutor) {
        require(pullPayments[_client][_pullPaymentExecutor].cancelTimestamp == 0, "Pull Payment is cancelled.");
        _;
    }

    modifier isValidPullPaymentExecutionRequest(address _client, address _pullPaymentExecutor, bytes32 _paymentID) {
        require(
            (pullPayments[_client][_pullPaymentExecutor].initialPaymentAmountInCents > 0 ||
        (now >= pullPayments[_client][_pullPaymentExecutor].startTimestamp &&
        now >= pullPayments[_client][_pullPaymentExecutor].nextPaymentTimestamp)
            ), "Invalid pull payment execution request - Time of execution is invalid."
        );
        require(pullPayments[_client][_pullPaymentExecutor].numberOfPayments > 0,
            "Invalid pull payment execution request - Number of payments is zero.");

        require((pullPayments[_client][_pullPaymentExecutor].cancelTimestamp == 0 ||
        pullPayments[_client][_pullPaymentExecutor].cancelTimestamp > pullPayments[_client][_pullPaymentExecutor].nextPaymentTimestamp),
            "Invalid pull payment execution request - Pull payment is cancelled");
        require(keccak256(
            abi.encodePacked(pullPayments[_client][_pullPaymentExecutor].paymentID)
        ) == keccak256(abi.encodePacked(_paymentID)),
            "Invalid pull payment execution request - Payment ID not matching.");
        _;
    }

    modifier isValidDeletionRequest(bytes32 _paymentID, address _client, address _pullPaymentExecutor) {
        require(_client != address(0), "Invalid deletion request - Client address is ZERO_ADDRESS.");
        require(_pullPaymentExecutor != address(0), "Invalid deletion request - Beneficiary address is ZERO_ADDRESS.");
        require(_paymentID.length != 0, "Invalid deletion request - Payment ID is empty.");
        _;
    }

    modifier isValidAddress(address _address) {
        require(_address != address(0), "Invalid address - ZERO_ADDRESS provided");
        _;
    }

    modifier validConversionRate(string memory _currency) {
        require(bytes(_currency).length != 0, "Invalid conversion rate - Currency is empty.");
        require(conversionRates[_currency] > 0, "Invalid conversion rate - Must be higher than zero.");
        _;
    }

    modifier validAmount(uint256 _fiatAmountInCents) {
        require(_fiatAmountInCents > 0, "Invalid amount - Must be higher than zero");
        _;
    }

    function executePullPayment(address _client, bytes32 _paymentID)
    public
    paymentExists(_client, msg.sender)
    isValidPullPaymentExecutionRequest(_client, msg.sender, _paymentID)
    {
        uint256 amountInPMA;

        if (pullPayments[_client][msg.sender].initialPaymentAmountInCents > 0) {
            amountInPMA = calculatePMAFromFiat(
                pullPayments[_client][msg.sender].initialPaymentAmountInCents,
                pullPayments[_client][msg.sender].currency
            );
            pullPayments[_client][msg.sender].initialPaymentAmountInCents = 0;
        } else {
            amountInPMA = calculatePMAFromFiat(
                pullPayments[_client][msg.sender].fiatAmountInCents,
                pullPayments[_client][msg.sender].currency
            );

            pullPayments[_client][msg.sender].nextPaymentTimestamp =
            pullPayments[_client][msg.sender].nextPaymentTimestamp + pullPayments[_client][msg.sender].frequency;
            pullPayments[_client][msg.sender].numberOfPayments = pullPayments[_client][msg.sender].numberOfPayments - 1;
        }

        pullPayments[_client][msg.sender].lastPaymentTimestamp = now;
        token.transferFrom(
            _client,
            pullPayments[_client][msg.sender].treasuryAddress,
            amountInPMA
        );

        emit LogPullPaymentExecuted(
            _client,
            pullPayments[_client][msg.sender].paymentID,
            pullPayments[_client][msg.sender].businessID,
            pullPayments[_client][msg.sender].uniqueReferenceID
        );
    }

    function calculatePMAFromFiat(uint256 _fiatAmountInCents, string memory _currency)
    internal
    view
    validConversionRate(_currency)
    validAmount(_fiatAmountInCents)
    returns (uint256) {
        return ONE_ETHER.mul(DECIMAL_FIXER).mul(_fiatAmountInCents).div(conversionRates[_currency]).div(FIAT_TO_CENT_FIXER);
    }

}
