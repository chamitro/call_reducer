contract Ownable {
    address ownerCEO;
    address ownerMoney;
    address privAddress;
    address addressAdmixture;
    function transferOwnership(address add) public           {
        if (add != address(0)) {
            ownerCEO = add;
        }
    }
    function transferOwnerMoney(address _ownerMoney) public            {
        if (_ownerMoney != address(0)) {
            ownerMoney = _ownerMoney;
        }
    }
}
contract Whitelist is Ownable{
    mapping(address => bool) public whitelist;
    mapping(uint  => address)   whitelistCheck;
    uint public countAddress = 0;
    event WhitelistedAddressAdded(address addr);
    event WhitelistedAddressRemoved(address addr);
    function addAddressToWhitelist(address addr)                 public returns(bool success) {
        if (!whitelist[addr]) {
            whitelist[addr] = true;
            countAddress = countAddress + 1;
            whitelistCheck[countAddress] = addr;
            emit WhitelistedAddressAdded(addr);
            success = true;
        }
    }
    function getWhitelistCheck(uint key)                 view public returns(address) {
        return whitelistCheck[key];
    }
    function getInWhitelist(address addr) public view returns(bool) {
        return whitelist[addr];
    }
}
library SafeMath {
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}
contract BaseRabbit is Whitelist{
    event EmotherCount(uint32 mother, uint summ);
    event SalaryBunny(uint32 bunnyId, uint cost);
    event CreateChildren(uint32 matron, uint32 sire, uint32 child);
    event BunnyDescription(uint32 bunnyId, string name);
    event CoolduwnMother(uint32 bunnyId, uint num);
    event Referral(address from, uint32 matronID, uint32 childID, uint currentTime);
    event Approval(address owner, address approved, uint32 tokenId);
    event Transfer(address from, address to, uint32 tokenId);
    event NewBunny(uint32 bunnyId, uint dnk, uint256 blocknumber, uint breed);
    using SafeMath for uint256;
    bool pauseSave = false;
    bool public promoPause = false;
    function setPromoPause() public                   {
        promoPause = !promoPause;
    }
    mapping(uint32 => uint) public totalSalaryBunny;
    mapping(uint32 => uint32[5]) public rabbitMother;
    mapping(uint32 => uint) public motherCount;
    mapping(uint32 => uint)  public rabbitSirePrice;
    mapping(uint32 => bool)  public allowedChangeSex;
    mapping (uint32 => uint) mapDNK;
    mapping (uint32 => bool) giffblock;
    mapping (uint32 => Rabbit)  tokenBunny;
    uint public tokenBunnyTotal;
    mapping (uint32 => address) public rabbitToOwner;
    mapping (address => uint32[]) public ownerBunnies;
    mapping (address => bool) ownerGennezise;
    struct Rabbit {
        uint32 mother;
        uint32 sire;
        uint birthblock;
        uint birthCount;
        uint birthLastTime;
        uint genome;
    }
}
contract ERC721 {
    function ownerOf(uint32 _tokenId) public view returns (address owner);
    function approve(address _to, uint32 _tokenId) public returns (bool success);
    function transfer(address _to, uint32 _tokenId) public;
    function transferFrom(address _from, address _to, uint32 _tokenId) public returns (bool);
    function balanceOf(address _owner) public view returns (uint balance);
}
    function balanceOf(address _owner) public view returns (uint) {
        return ownerBunnies[_owner].length;
    }
