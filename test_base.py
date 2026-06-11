import time
from engine_base import MarketDataStream, PositionTracker

def run_test():
    print("🚦 正在验证 trading_bot 目录下的底层基础底座...")
    stream = MarketDataStream(symbol="BTC_USDT", initial_price=100.0)
    tracker = PositionTracker(symbol="BTC_USDT")
    
    for i in range(1, 4):
        tick = stream.next_tick()
        tracker.update_mark_price(tick.price)
        
        print(f"\n[Tick {i}] 实时市价: {tick.price} | 持仓均价: {tracker.entry_price} | 浮动盈亏: {tracker.unrealized_pnl:.2f}")
        
        if i == 1:
            print(f"   👉 模拟成交回报：BUY 买入 1.0 个单位")
            tracker.process_execution("BUY", tick.price, 1.0)
        elif i == 3:
            print(f"   👉 模拟成交回报：SELL 全平仓位")
            tracker.process_execution("SELL", tick.price, tracker.quantity)
            
        time.sleep(0.1)
    print("\n✅ 基础模块数据结构验证成功！")

if __name__ == "__main__":
    run_test()
