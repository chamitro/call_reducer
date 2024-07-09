

pragma solidity 0.5.0;

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(address from, address to, uint256 value) external returns (bool);

    event Approval(address indexed owner, address indexed spender, uint256 value);
}

pragma solidity 0.5.0;

library SafeMath {

}

pragma solidity 0.5.0;

contract ERC20 is IERC20{
    using SafeMath for uint256;

    mapping (address => mapping (address => uint256)) private _allowed;

    function transfer(address to, uint256 value) public returns (bool) {

        return true;
    }

    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        _allowed[from][msg.sender]                                        ;

        emit Approval(from, msg.sender, _allowed[from][msg.sender]);
        return true;
    }

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract PumaPayToken is ERC20{

    function transfer(address _to, uint256 _value) public returns (bool) {
        return super.transfer(_to, _value);
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract PumaPayPullPayment{

    using SafeMath for uint256;

    event LogPullPaymentExecuted(
        address customerAddress,
        bytes32 paymentID,
        bytes32 businessID,
        bytes32 uniqueReferenceID
    );

    PumaPayToken public token;

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

    function executePullPayment(address _client, bytes32 _paymentID)
    public

    {
        uint256 amountInPMA;

        if (pullPayments[_client][msg.sender].initialPaymentAmountInCents > 0) {
            amountInPMA                                                                                                                                                                                ;
            pullPayments[_client][msg.sender].initialPaymentAmountInCents = 0;
        } else {
            amountInPMA                                                                                                                                                                      ;

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

}
