library SafeMath {
  function mul(uint256  , uint256  )               returns (uint256)
                {
    }
  function div(uint256  , uint256  )               returns (uint256) {
  }
}
contract SimpleAuction {
    using SafeMath for *;
    function bid()                {
                                       msg.value.div(10).mul(9) ;
    }
}
