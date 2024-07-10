contract Ownable {
    address ownerMoney;
    function transferOwnerMoney(address _ownerMoney)
                                       {
            ownerMoney = _ownerMoney;
        }
}
contract BaseRabbit               {
    mapping(uint32 => uint)        totalSalaryBunny;
    mapping(uint32 => uint32[ ])        rabbitMother;
    mapping(uint32 => uint)        motherCount;
    mapping(uint32 => uint)         rabbitSirePrice;
    mapping(uint32 => bool)         allowedChangeSex;
    mapping (uint32 => uint) mapDNK;
    mapping (uint32 => bool) giffblock;
    mapping (uint32 => Rabbit)  tokenBunny;
    mapping (address => uint32[])        ownerBunnies;
    mapping (address => bool) ownerGennezise;
}
contract Rabbit is BaseRabbit         {
    uint        totalBunny    ;
    function ownerOf(uint32 _tokenId)             returns (address      ) {
        return               _tokenId ;
    }
    function removeTokenList(address _owner, uint32 _tokenId)          {
        for (uint256 i    ;          ;    )
            if(ownerBunnies[_owner][i] == _tokenId)
                return;
    }
    function addTokenList(address owner,  uint32 _tokenId)          {
        ownerBunnies[owner].push( _tokenId);
    }
    function transfer(address _to, uint32 _tokenId)        {
        address currentOwner             ;
        address oldOwner =               _tokenId ;
                currentOwner != _to ;
    }
    function transferFrom(address _from, address _to, uint32 _tokenId)                                        {
        address oldOwner =               _tokenId ;
                oldOwner == _from ;
                oldOwner != _to ;
    }
    function setTotalBunny_id(uint _totalBunny)                            {
        totalBunny = _totalBunny;
    }
    function setTokenBunny(uint32                                                                                        , address _owner, uint DNK)
                                                   {
            uint32 id                          ;
            addTokenList(_owner, id);
    }
    function relocateToken(
        uint32 id
                   ,
        address _owner,
        uint DNK
         )                           {
                addTokenList(_owner, id);
    }
    function setDNK( uint32 _bunny          )                            {
        mapDNK[_bunny]      ;
    }
    function setMotherCount( uint32 _bunny            )                          {
        motherCount[_bunny]        ;
    }
    function setRabbitSirePrice( uint32 _bunny            )                            {
        rabbitSirePrice[_bunny]        ;
    }
    function setAllowedChangeSex( uint32 _bunny               )                          {
        allowedChangeSex[_bunny]           ;
    }
    function setTotalSalaryBunny( uint32 _bunny            )                            {
        totalSalaryBunny[_bunny]        ;
    }
    function setRabbitMother(uint32 children, uint32[ ] _m)                            {
             rabbitMother[children] = _m;
    }
    function setGenome(uint32 _bunny             )                            {
        tokenBunny[_bunny]                ;
    }
    function setParent(uint32 _bunny                            )                             {
        tokenBunny[_bunny]                ;
    }
    function setBirthLastTime(uint32 _bunny                    )                            {
        tokenBunny[_bunny]                              ;
    }
    function setBirthCount(uint32 _bunny                 )                            {
        tokenBunny[_bunny]                        ;
    }
    function setBirthblock(uint32 _bunny                 )                            {
        tokenBunny[_bunny]                        ;
    }
    function setGiffBlock(uint32 _bunny              )                            {
        giffblock[_bunny]          ;
    }
    function setOwnerGennezise(address _to             )                            {
        ownerGennezise[_to]         ;
    }
    function getOwnerGennezise(address _to)             returns(bool) {
        return ownerGennezise[_to];
    }
    function getGiffBlock(uint32 _bunny)             returns(bool) {
        return  giffblock[_bunny];
    }
    function getAllowedChangeSex(uint32 _bunny)             returns(bool) {
        return  allowedChangeSex[_bunny];
    }
    function getRabbitSirePrice(uint32 _bunny)             returns(uint) {
        return                 _bunny ;
    }
    function balanceOf(address _owner)             returns (uint) {
        return ownerBunnies[_owner].length;
    }
     function getMotherCount(uint32 _mother)             returns(uint) {
        return              _mother ;
    }
     function getTotalSalaryBunny(uint32 _bunny)             returns(uint) {
        return                   _bunny ;
    }
    function getTokenBunny(uint32 _bunny)
                                                                                                                {
                 tokenBunny[_bunny]       ;
    }
    function getSex(uint32 _bunny)                           {
        if(getRabbitSirePrice(_bunny) > 0)
            return     ;
    }
    function getGenome(uint32 _bunny)             returns( uint) {
        return            _bunny        ;
    }
    function getParent(uint32 _bunny)                                                 {
                 tokenBunny[_bunny]       ;
    }
    function getBirthLastTime(uint32 _bunny)             returns(uint) {
        return            _bunny               ;
    }
    function getBirthCount(uint32 _bunny)             returns(uint) {
        return            _bunny            ;
    }
    function getBirthblock(uint32 _bunny)             returns(uint) {
        return            _bunny            ;
    }
    function getBunnyInfo(uint32 _bunny)
          {
                   getSex(_bunny);
    }
}
