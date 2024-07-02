pragma solidity 0.4.18;

contract Ownable {

}

contract VancouverCharityDrive is Ownable {

    mapping(address => Pledge[]) public pledges; 

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

        return true;
    }

}
