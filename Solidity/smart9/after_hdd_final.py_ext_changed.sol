pragma solidity ^0.4.18;

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

}

library SafeMath {
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

}

contract BRDLockup is Ownable {
  using SafeMath for uint256;

  struct Allocation {
    address beneficiary;      
    uint256 allocation;       
    uint256 remainingBalance; 
    uint256 currentInterval;  
    uint256 currentReward;    
  }

  Allocation[] public allocations;

  uint256 public unlockDate;

  uint256 public currentInterval;

  uint256 public intervalDuration;

  uint256 public numIntervals;

  event Lock(address indexed _to, uint256 _amount);

  event Unlock(address indexed _to, uint256 _amount);

  function processInterval()           public returns (bool _shouldProcessRewards) {

    bool _correctInterval = now >= unlockDate && now.sub(unlockDate) > currentInterval.mul(intervalDuration);
    bool _validInterval = currentInterval < numIntervals;
    if (!_correctInterval || !_validInterval)
      return false;

    currentInterval                         ;

    uint _allocationsIndex = allocations.length;

    for (uint _i = 0; _i < _allocationsIndex; _i++) {

      uint256 _amountToReward;

      if (currentInterval == numIntervals) {
        _amountToReward = allocations[_i].remainingBalance;
      } else {

        _amountToReward                                               ;
      }

      allocations[_i].currentReward = _amountToReward;
    }

    return true;
  }

  function pushAllocation(address _beneficiary, uint256 _numTokens)           public {
    require(now < unlockDate);
    allocations.push(
      Allocation(
        _beneficiary,
        _numTokens,
        _numTokens,
        0,
        0
      )
    );
    Lock(_beneficiary, _numTokens);
  }
}
