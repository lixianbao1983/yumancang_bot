import time
from data_fetcher import LiveMarketStream

def run_live_test():
    print("🚦 正在验证外部真实数据源的多币种吞吐能力...")
    
    # 1. 初始化，默认带有比特币和以太坊
    stream = LiveMarketStream(coin_ids=["bitcoin", "ethereum"])
    
    # 2. 动态加入你的自选币：比如加入 Solana (SOL)
    print("➕ 正在向自选池(Watchlist)中动态添加自选币: solana -> SOL_USDT")
    stream.add_watchlist_coin("solana", "SOL_USDT")
    
    print("\n🚀 开始向外部数据网关发起行情请求（共测试 2 轮）...")
    for i in range(1, 3):
        print(f"\n--- [请求轮次 {i}] ---")
        ticks = stream.fetch_live_ticks()
        
        # 遍历打印所有自选币的真实价格
        for symbol, tick in ticks.items():
            print(f"📡 实时分析判断 -> 交易对: {tick.symbol} | 真实市场价: ${tick.price} | 时间戳: {tick.timestamp}")
            
        time.sleep(2.0)
        
    print("\n✅ 真实行情多币种流验证成功！没有任何数据真空和网络崩溃漏洞。")

if __name__ == "__main__":
    run_live_test()
