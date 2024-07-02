

pragma solidity 0.5.0;

interface IERC20 {

    function transferFrom(address from, address to, uint256 value) external returns (bool);

}

pragma solidity 0.5.0;

library SafeMath {

}

pragma solidity 0.5.0;

contract ERC20 is IERC20{
    using SafeMath for uint256;

    function transferFrom(address from, address to, uint256 value) public returns (bool) {

        return true;
    }

}

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

pragma solidity 0.5.0;

contract PumaPayToken is ERC20{

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }
}

pragma solidity 0.5.0;

contract PayableOwnable {

}

pragma solidity 0.5.0;

contract PumaPayPullPayment is PayableOwnable{

    using SafeMath for uint256;

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

    }

}
