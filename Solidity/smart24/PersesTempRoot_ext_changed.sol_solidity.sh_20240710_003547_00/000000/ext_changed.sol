pragma solidity ^0.4.18;
contract CommonEth {
    enum  Modes {LIVE, TEST}
    Modes public mode = Modes.LIVE;
    address internal ceoAddress;
    address internal cfoAddress;
    address internal cooAddress;
    modifier onlyCEO() {
        require(msg.sender == ceoAddress);
        _;
    }
    modifier onlyLiveMode() {
        require(mode == Modes.LIVE || msg.sender == ceoAddress || msg.sender == cooAddress || msg.sender == cfoAddress);
        _;
    }
    function setCEO(address _newCEO) public onlyCEO {
        ceoAddress = _newCEO;
    }
    function setCFO(address _newCFO) public onlyCEO {
        cfoAddress = _newCFO;
    }
    function setCOO(address _newCOO) public onlyCEO {
        cooAddress = _newCOO;
    }
}
