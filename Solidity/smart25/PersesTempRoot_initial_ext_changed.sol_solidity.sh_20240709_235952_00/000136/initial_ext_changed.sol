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
contract Rabbit is ERC721, BaseRabbit{
    uint public totalBunny = 0;
    string public constant name = "CryptoRabbits";
    string public constant symbol = "CRB";
    function ownerOf(uint32 _tokenId) public view returns (address owner) {
        return rabbitToOwner[_tokenId];
    }
    function approve(address _to, uint32 _tokenId) public returns (bool) {
        _to;
        _tokenId;
        return false;
    }
    function removeTokenList(address _owner, uint32 _tokenId) internal {
        require(isPauseSave());
        uint count = ownerBunnies[_owner].length;
        for (uint256 i = 0; i < count; i++) {
            if(ownerBunnies[_owner][i] == _tokenId)
            {
                delete ownerBunnies[_owner][i];
                if(count > 0 && count != (i-1)){
                    ownerBunnies[_owner][i] = ownerBunnies[_owner][(count-1)];
                    delete ownerBunnies[_owner][(count-1)];
                }
                ownerBunnies[_owner].length--;
                return;
            }
        }
    }
    function addTokenList(address owner,  uint32 _tokenId) internal {
        ownerBunnies[owner].push( _tokenId);
        rabbitToOwner[_tokenId] = owner;
    }
    function transfer(address _to, uint32 _tokenId) public {
        require(isPauseSave());
        address currentOwner = msg.sender;
        address oldOwner = rabbitToOwner[_tokenId];
        require(rabbitToOwner[_tokenId] == msg.sender);
        require(currentOwner != _to);
        require(_to != address(0));
        removeTokenList(oldOwner, _tokenId);
        addTokenList(_to, _tokenId);
        emit Transfer(oldOwner, _to, _tokenId);
    }
    function isPauseSave() public view returns(bool) {
        return !pauseSave;
    }
    function setTotalBunny() internal                   returns(uint) {
        require(isPauseSave());
        return totalBunny = totalBunny.add(1);
    }
    function setTotalBunny_id(uint _totalBunny) external                   {
        require(isPauseSave());
        totalBunny = _totalBunny;
    }
    function setTokenBunny(uint32 mother, uint32  sire, uint birthblock, uint birthCount, uint birthLastTime, uint genome, address _owner, uint DNK)
        external                   returns(uint32) {
            uint32 id = uint32(setTotalBunny());
            tokenBunny[id] = Rabbit(mother, sire, birthblock, birthCount, birthLastTime, genome);
            mapDNK[id] = DNK;
            addTokenList(_owner, id);
            emit NewBunny(id, DNK, block.number, 0);
            emit CreateChildren(mother, sire, id);
            setMotherCount(id, 0);
        return id;
    }
    function relocateToken(
        uint32 id,
        uint32 mother,
        uint32 sire,
        uint birthblock,
        uint birthCount,
        uint birthLastTime,
        uint genome,
        address _owner,
        uint DNK
         ) external                  {
                tokenBunny[id] = Rabbit(mother, sire, birthblock, birthCount, birthLastTime, genome);
                mapDNK[id] = DNK;
                addTokenList(_owner, id);
    }
    function setDNK( uint32 _bunny, uint dnk) external                   {
        require(isPauseSave());
        mapDNK[_bunny] = dnk;
    }
    function setMotherCount( uint32 _bunny, uint count) public                   {
        require(isPauseSave());
        motherCount[_bunny] = count;
    }
    function setRabbitSirePrice( uint32 _bunny, uint count) external                   {
        require(isPauseSave());
        rabbitSirePrice[_bunny] = count;
    }
    function setAllowedChangeSex( uint32 _bunny, bool canBunny) public                   {
        require(isPauseSave());
        allowedChangeSex[_bunny] = canBunny;
    }
    function setTotalSalaryBunny( uint32 _bunny, uint count) external                   {
        require(isPauseSave());
        totalSalaryBunny[_bunny] = count;
    }
    function setRabbitMother(uint32 children, uint32[5] _m) external                   {
             rabbitMother[children] = _m;
    }
    function setGenome(uint32 _bunny, uint genome)  external                  {
        tokenBunny[_bunny].genome = genome;
    }
    function setParent(uint32 _bunny, uint32 mother, uint32 sire)  external                   {
        tokenBunny[_bunny].mother = mother;
        tokenBunny[_bunny].sire = sire;
    }
    function setBirthLastTime(uint32 _bunny, uint birthLastTime) external                   {
        tokenBunny[_bunny].birthLastTime = birthLastTime;
    }
    function setBirthCount(uint32 _bunny, uint birthCount) external                   {
        tokenBunny[_bunny].birthCount = birthCount;
    }
    function setBirthblock(uint32 _bunny, uint birthblock) external                   {
        tokenBunny[_bunny].birthblock = birthblock;
    }
    function setGiffBlock(uint32 _bunny, bool blocked) external                   {
        giffblock[_bunny] = blocked;
    }
    function setOwnerGennezise(address _to, bool canYou) external                   {
        ownerGennezise[_to] = canYou;
    }
    function getOwnerGennezise(address _to) public view returns(bool) {
        return ownerGennezise[_to];
    }
    function getGiffBlock(uint32 _bunny) public view returns(bool) {
        return !giffblock[_bunny];
    }
    function getAllowedChangeSex(uint32 _bunny) public view returns(bool) {
        return !allowedChangeSex[_bunny];
    }
    function getRabbitSirePrice(uint32 _bunny) public view returns(uint) {
        return rabbitSirePrice[_bunny];
    }
    function balanceOf(address _owner) public view returns (uint) {
        return ownerBunnies[_owner].length;
    }
     function getMotherCount(uint32 _mother) public view returns(uint) {
        return  motherCount[_mother];
    }
     function getTotalSalaryBunny(uint32 _bunny) public view returns(uint) {
        return  totalSalaryBunny[_bunny];
    }
    function getTokenBunny(uint32 _bunny) public
    view returns(uint32 mother, uint32 sire, uint birthblock, uint birthCount, uint birthLastTime, uint genome) {
        mother = tokenBunny[_bunny].mother;
        sire = tokenBunny[_bunny].sire;
        birthblock = tokenBunny[_bunny].birthblock;
        birthCount = tokenBunny[_bunny].birthCount;
        birthLastTime = tokenBunny[_bunny].birthLastTime;
        genome = tokenBunny[_bunny].genome;
    }
    function getSex(uint32 _bunny) public view returns(bool) {
        if(getRabbitSirePrice(_bunny) > 0) {
            return true;
        }
        return false;
    }
    function getGenome(uint32 _bunny) public view returns( uint) {
        return tokenBunny[_bunny].genome;
    }
    function getParent(uint32 _bunny) public view returns(uint32 mother, uint32 sire) {
        mother = tokenBunny[_bunny].mother;
        sire = tokenBunny[_bunny].sire;
    }
    function getBirthLastTime(uint32 _bunny) public view returns(uint) {
        return tokenBunny[_bunny].birthLastTime;
    }
    function getBirthCount(uint32 _bunny) public view returns(uint) {
        return tokenBunny[_bunny].birthCount;
    }
    function getBirthblock(uint32 _bunny) public view returns(uint) {
        return tokenBunny[_bunny].birthblock;
    }
    function getBunnyInfo(uint32 _bunny) public view returns(
        uint32 mother,
        uint32 sire,
        uint birthblock,
        uint birthCount,
        uint birthLastTime,
        bool role,
        uint genome,
        bool interbreed,
        uint leftTime,
        uint lastTime,
        uint price,
        uint motherSumm
        ) {
            role = getSex(_bunny);
            mother = tokenBunny[_bunny].mother;
            sire = tokenBunny[_bunny].sire;
            birthblock = tokenBunny[_bunny].birthblock;
            birthCount = tokenBunny[_bunny].birthCount;
            birthLastTime = tokenBunny[_bunny].birthLastTime;
            genome = tokenBunny[_bunny].genome;
            motherSumm = getMotherCount(_bunny);
            price = getRabbitSirePrice(_bunny);
            lastTime = lastTime.add(birthLastTime);
            if(lastTime <= now) {
                interbreed = true;
            } else {
                leftTime                    ;
            }
    }
}
