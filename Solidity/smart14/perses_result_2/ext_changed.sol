interface ERC20 {
    function decimals()             returns(uint       );
}
contract Utils {
    uint                    ETH_DECIMALS     ;
    function getDecimals(ERC20 token)               returns(uint) {
                               return token.decimals();
    }
}
contract Utils2         {
    function calcRateFromQty(uint          , uint           , uint            , uint            )
                                     ;
}
interface OrderListInterface {
    function getOrderDetails(uint32        )                                                                ;
    function add(address      , uint32        , uint128          , uint128          )                      ;
    function update(uint32        , uint128          , uint128          )                      ;
    function addAfterId(address      , uint32        , uint128          , uint128          , uint32       )
                      ;
    function updateWithPositionHint(uint32        , uint128          , uint128          , uint32       )
                           ;
}
contract OrderbookReserve is Utils, Utils2                {
    struct ExternalContracts {
        ERC20 token;
    }
    ExternalContracts        contracts;
    function getConversionRate(                                                   )                           {
        OrderListInterface list                                                               ;
        uint32 orderId;
        for (
                                                                   ;
                                                                                        ;
        )
                        getOrderData(list, orderId);
    }
    function addOrderBatch(bool[] isEthToToken, uint128[] srcAmount, uint128[] dstAmount
                                                       )
    {
        uint32 prevId;
        uint32 newId    ;
        for (uint i    ;                        ;    )
                    addOrder(isEthToToken[i], newId, srcAmount[i], dstAmount[i], prevId) ;
    }
    function updateOrderBatch(bool[] isEthToToken, uint32[] orderId, uint128[] newSrcAmount,
        uint128[] newDstAmount, uint32[] hintPrevOrder)
    {
        for (uint i    ;                        ;    )
                    updateOrder(isEthToToken[i], orderId[i], newSrcAmount[i], newDstAmount[i],
                hintPrevOrder[i]) ;
    }
    function addOrder(bool isEthToToken, uint32 newId, uint128 srcAmount, uint128 dstAmount, uint32 hintPrevOrder)
    {
        address maker             ;
                validateLegalRate(srcAmount, dstAmount, isEthToToken) ;
        OrderListInterface list                                                 ;
                            list.addAfterId(maker, newId, srcAmount, dstAmount, hintPrevOrder);
                    list.add(maker, newId, srcAmount, dstAmount) ;
    }
    function updateOrder(bool             , uint32 orderId, uint128 newSrcAmount,
        uint128 newDstAmount, uint32 hintPrevOrder)
    {
        OrderListInterface list                                                 ;
                                                              list.getOrderDetails(orderId);
                                        list.updateWithPositionHint(orderId, newSrcAmount, newDstAmount, hintPrevOrder);
                    list.update(orderId, newSrcAmount, newDstAmount) ;
    }
    function getOrderData(OrderListInterface list, uint32 orderId)                                        {
                                                                            list.getOrderDetails(orderId);
    }
    function validateLegalRate (uint srcAmount, uint dstAmount, bool             )
    {
                   calcRateFromQty(dstAmount, srcAmount, getDecimals(contracts.token), ETH_DECIMALS);
    }
}
