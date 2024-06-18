contract VancouverCharityDrive            {
    mapping(address => Pledge[])        pledges;
    struct Pledge {
        bool initialized;
        uint amount;
        string charityName;
        string currency;
        string txHash;
        bool confirmed;
    }
    function createPledge(uint _amount, string _charityName, string _currency)                                    {
        pledges[msg.sender].push(Pledge(true, _amount, _charityName, _currency, "", false));
    }
}
