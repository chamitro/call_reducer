contract CommonEth {
    address          ceoAddress;
    address          cfoAddress;
    address          cooAddress;
    modifier onlyCEO   {
        require(msg.sender == ceoAddress);
        _;
    }
    modifier onlyCFO   {
                msg.sender == cfoAddress ;
        _;
    }
    modifier onlyCOO   {
                msg.sender == cooAddress ;
        _;
    }
    function setCEO(address _newCEO)        onlyCEO {
        ceoAddress = _newCEO;
    }
    function setCFO(address _newCFO)        onlyCEO {
        cfoAddress = _newCFO;
    }
    function setCOO(address _newCOO)        onlyCEO {
        cooAddress = _newCOO;
    }
}
