pragma solidity 0.4.18;

contract VancouverCharityDrive            {

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

    function createPledge(uint _amount, string _charityName, string _currency) public               returns(bool) {
        pledges[msg.sender].push(Pledge(true, _amount, _charityName, _currency, "", false));
        PledgeCreated(msg.sender, _amount, companies[msg.sender].name);
        return true;
    }

}
