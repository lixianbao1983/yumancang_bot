import logging

class ExecutionEngine:
    """
    工业级无状态执行引擎 (Stateless ExecutionEngine)
    【核心铁律】只负责订单对接与发送，绝对不自行维护、计算资金和仓位。
    """
    def __init__(self, is_simulated=True):
        self.is_simulated = is_simulated
        logging.info("⚡ 无状态执行引擎初始化成功。")

    def execute_real_order(self, symbol, side, qty, price):
        """
        全系统唯一的发单执行入口。
        不再自行修改内部状态，而是单纯返回标准的成交回报。
        """
        qty = float(qty)
        price = float(price)
        
        if self.is_simulated:
            # 模拟环境：默认全额撮合
            fee = qty * price * 0.0002  # 模拟万分之二手续费
            logging.info(f"⚡ [模拟执行成单] -> {side} {qty} {symbol} @ {price} | 预估手续费: {fee:.4f}")
            
            # 返回干净、标准的成交回报字典，供主循环和真理账本进行单向记账
            return {
                "status": "SUCCESS",
                "symbol": symbol,
                "side": side,
                "exec_qty": qty,
                "exec_price": price,
                "fee": fee
            }
        else:
            # 实盘环境：此处未来可无缝对接交易所真正的 API 发单请求
            # response = exchange.create_order(symbol, 'market', side, qty)
            # return response
            pass
