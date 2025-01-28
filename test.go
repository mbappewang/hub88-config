var eur float64 // 定义一个浮点数变量 eur

// 如果 hub88 下注的接口返回的赔率大于下注的赔率。
oddsDiff := math.Abs(realTimeDdds-order.Totalodds) / realTimeDdds // 计算实时赔率与订单赔率的差异百分比

if oddsDiff >= 0.1 { // 如果赔率差异大于等于 0.1
    loggerSvc.Error( // 记录错误日志
        msg: "cashOutBetOrder",
        zap.Float64(key: "oddsDiff", oddsDiff), // 记录赔率差异
        zap.Float64(key: "realTimeDdds", realTimeDdds), // 记录实时赔率
        zap.Float64(key: "order.Totalodds", order.Totalodds) // 记录订单赔率
    )
    eur = decimal.NewFromFloat(order.EUR).Truncate(precision: 2).InexactFloat64() // 将订单中的欧元金额截取到小数点后两位
} else {
    // hub88 请求 cashout
    // 请求的 cashout 金额为欧元。
    // cashOutRequestAmount := fmt.Sprintf("%.2f",helper.Decimal(cashOutAmount))
    cashOutRequestAmount := decimal.NewFromFloat(cashOutAmount).Truncate(precision: 2).String() // 将 cashout 金额截取到小数点后两位并转换为字符串
    eur, _, _, err = CoinToEur(order.OriginCurrendyType, cashOutRequestAmount, loggerSvc) // 将原始货币类型转换为欧元
    if err != nil { // 如果转换过程中发生错误
        loggerSvc.Error( // 记录错误日志
            msg: "cashOutBetOrder",
            zap.String(key: "err", err.Error()) // 记录错误信息
        )
        return constants.ErrinternalServererror, cashOutAmount, err // 返回内部服务器错误、cashout 金额和错误信息
    }
    // 向 hub88 发送 cashout 请求。
    req := CashOutRequest{
        CashOutAmount: eur, // 设置 cashout 请求的金额为欧元
    }
}