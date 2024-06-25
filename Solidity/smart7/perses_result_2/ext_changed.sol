library SafeMath {
  function add(uint256             ) internal                        {
  }
}
contract Exchange         {
    using SafeMath for uint256;
    mapping(address => mapping(address => uint256))        balanceOf;
    function checkBalances(address addr                     , address soldToken                                                                               ) private
                                 {
                 balanceOf[soldToken][addr]               .add             ;
      }
}
