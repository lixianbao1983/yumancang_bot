import time
import os
import sys

# 动态对齐 Python 根寻址路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from execution.gate_executor import GateExecutor
from risk.risk_gate import RiskGate
from signals.ai_signal import AISignalEngine
from state_manager import StateManager

def start_trading_loop():
    print("====== 🤖 AI Autonomous Trading Loop V2 (Halt Gate Ready) ======")
    
    # 实例化当前根目录下的组件真身
    trader = GateExecutor()
    gatekeeper = RiskGate()
    state = StateManager()
    ai_brain = AISignalEngine()
    
    # 🟢 严格对齐你 V2 方案的全局退出状态管理控制
    while state.get("running", True):
        try:
            print("\n---------------------------------------------------------")
            print("[System Heartbeat] Checking multi-agent risk state...")
            
            # 🟢 严格对齐你 V2 方案的熔断拦截机制 (通过 StateManager 校验全局是否挂起)
            if not state.get("trading_enabled", True):
                print("⚠️ [Risk Halt] Trading is currently halted by state_manager switch.")
                time.sleep(5)
                continue
                
            print("[System Heartbeat] Querying OpenClaw Core Brain for consensus...")
            ai_decision = ai_brain.execute_autonomous_decision()
            action = ai_decision.get("action", "HOLD")
            reason = ai_decision.get("reason", "No reason.")
            
            print(f"🧠 [AI Brain Output] Action: {action} | Reason: {reason}")
            
            if action == "HOLD":
                time.sleep(5)
                continue
                
            # 动态对齐实盘数据执行包
            target_order = {
                "symbol": "BTC/USDT",
                "side": action,
                "qty": 0.0005,
                "price": 65000.0
            }
            
            # 过多层风控拦截网
            is_allowed, risk_reason = gatekeeper.allow(
                symbol=target_order["symbol"],
                side=target_order["side"],
                qty=target_order["qty"],
                price=target_order["price"]
            )
            
            if not is_allowed:
                print(f"❌ [Risk Blocked] Order rejected: {risk_reason}")
                time.sleep(2)
                continue
                
            # 物理流向真实执行层
            print("🚀 [Risk Passed] Routing to Gate.io Broker...")
            result = trader.execute_real_order(
                symbol=target_order["symbol"],
                side=target_order["side"],
                qty=target_order["qty"],
                price=target_order["price"]
            )
            print(f"📝 [Broker Result]: {result}")
            
        except Exception as e:
            print(f"⚠️ [Loop Exception Caught]: {e}")
            
        # 🔹 V2 全局强制时序 Cooldown 刷新速度，彻底截断高频刷单
        time.sleep(5)

if __name__ == "__main__":
    start_trading_loop()
