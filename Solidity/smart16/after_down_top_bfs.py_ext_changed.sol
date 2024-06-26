pragma solidity 0.4.18;

contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}

contract VancouverCharityDrive is Ownable {

    mapping(address => Pledge[]) public pledges; 
    mapping(address => CompanyInfo) public companies; 
    address[] public participatingCompanies;

    event PledgeCreated(address indexed pledger, uint256 amount, string companyName);
    event PledgeUpdated(address indexed pledger, uint256 amount, string companyName);
    event PledgeConfirmed(address indexed pledger, uint256 amount, string companyName, string txHash);

    struct CompanyInfo {
        bool initialized;
        string name;
        string email;
        string description;
    }

    struct Pledge {
        bool initialized;
        uint amount; 
        string charityName; 
        string currency; 
        string txHash; 
        bool confirmed;
    }

    function whitelistCompany(address _companyAddress, string _companyName, string _companyEmail, string _description) public onlyOwner returns(bool) {
        companies[_companyAddress] = CompanyInfo(true, _companyName, _companyEmail, _description);
        participatingCompanies.push(_companyAddress);
        return true;
    }

    function createPledge(uint _amount, string _charityName, string _currency) public               returns(bool) {
        pledges[msg.sender].push(Pledge(true, _amount, _charityName, _currency, "", false));
        PledgeCreated(msg.sender, _amount, companies[msg.sender].name);
        return true;
    }

    function updatePledge(uint _amount, string _charityName, string _currency, uint _pledgeIndex) public               returns(bool) {
        Pledge storage pledge = pledges[msg.sender][_pledgeIndex];
        require(pledge.initialized == true && pledge.confirmed == false);
        pledge.currency = _currency;
        pledge.amount = _amount;
        pledge.charityName = _charityName;
        return true;
    }

    function confirmPledge(uint _pledgeIndex, string _txHash) public               returns(bool) {
        Pledge storage pledge = pledges[msg.sender][_pledgeIndex];
        require(pledge.initialized == true && pledge.confirmed == false);
        pledge.txHash = _txHash;
        pledge.confirmed = true;
        PledgeConfirmed(msg.sender, pledge.amount, companies[msg.sender].name, _txHash);
        return true;
    }

}
