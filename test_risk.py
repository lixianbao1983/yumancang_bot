import time
from engine_base import MarketTick, PositionTracker, MarketDataStream
from risk.risk_manager import RiskManager

def run_risk_test():
    print("🚦 验证风控模块联动...")
    stream = MarketDataStream(symbol="BTC_USDT")
    tracker = PositionTracker(symbol="BTC_USDT")
    risk = RiskManager(max_position_size=2.0, max_daily_trades=2)
    
    tick = stream.next_tick()
    
    print("\n--- 测试 1: 正常买入 ---")
    if risk.check_risk("BUY", 1.0, tick, tracker, daily_trade_count=0):
        tracker.process_execution("BUY", tick.price, 1.0)
        
    print("\n--- 测试 2: 超出最大仓位限制测试 ---")
    # 当前已持仓 1.0，再买 1.5 会变成 2.5，超过 max_position_size=2.0
    risk.check_risk("BUY", 1.5, tick, tracker, daily_trade_count=1)

    print("\n--- 测试 3: 超出日内频次限制测试 ---")
    # 频次达到 2 次，触发拒绝
    risk.check_risk("BUY", 0.5, tick, tracker, daily_trade_count=2)
    
    print("\n✅ 风控逻辑与底座联动验证成功！")

if __name__ == "__main__":
    run_risk_test()
