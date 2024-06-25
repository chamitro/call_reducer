pragma solidity ^0.4.19;

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

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}

library SafeMath32 {

  function mul(uint32 a, uint32 b) internal pure returns (uint32) {
    if (a == 0) {
      return 0;
    }
    uint32 c = a * b;
    assert(c / a == b);
    return c;
  }

  function sub(uint32 a, uint32 b) internal pure returns (uint32) {
    assert(b <= a);
    return a - b;
  }

  function add(uint32 a, uint32 b) internal pure returns (uint32) {
    uint32 c = a + b;
    assert(c >= a);
    return c;
  }
}

library SafeMath16 {

  function mul(uint16 a, uint16 b) internal pure returns (uint16) {
    if (a == 0) {
      return 0;
    }
    uint16 c = a * b;
    assert(c / a == b);
    return c;
  }

  function sub(uint16 a, uint16 b) internal pure returns (uint16) {
    assert(b <= a);
    return a - b;
  }

  function add(uint16 a, uint16 b) internal pure returns (uint16) {
    uint16 c = a + b;
    assert(c >= a);
    return c;
  }
}

contract ERC721 {
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);

}
contract PreSell is ERC721{
    using SafeMath for uint256;
    struct Coach{
        uint256 drawPrice;
        uint256 emoteRate;
        uint256 sellPrice;
        uint8   isSell;
        uint8   category;
    }
    event initialcoach(uint _id);
    event drawcoach(uint _id,address _owner);
    event purChase(uint _id, address _newowner, address _oldowner);
    event inviteCoachBack(address _from,address _to, uint _fee);
    Coach[] public originCoach;
    Coach[] public coaches; 
    mapping(uint=>address) coachToOwner;
    mapping(uint=>uint) public coachAllnums;
    mapping(address=>uint) ownerCoachCount;
    mapping (uint => address) coachApprovals;

    function _transfer(address _from, address _to, uint256 _tokenId) private {
        require(_to != _from);
        ownerCoachCount[_to] = ownerCoachCount[_to].add(1) ;
        ownerCoachCount[_from] = ownerCoachCount[_from].sub(1);
        coachToOwner[_tokenId] = _to;
        emit Transfer(_from, _to, _tokenId);
    }

}
