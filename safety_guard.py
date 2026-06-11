# ~/trading_bot/safety_guard.py

import json
import os

class SafetyGuard:
    """
    实盘安全层（最终防爆系统）
    """

    def __init__(self,
                 max_drawdown=-1000,
                 max_loss_streak=5):

        self.max_drawdown = max_drawdown
        self.max_loss_streak = max_loss_streak

        self.locked = False
        self.loss_streak = 0

    # =========================
    # 1. 总权益风控
    # =========================
    def check_equity(self, equity):
        if equity <= self.max_drawdown:
            self.locked = True
            print(f"🚨 [SAFETY] 最大回撤触发，系统冻结")
            return False
        return True

    # =========================
    # 2. 连续亏损风控
    # =========================
    def update_trade_result(self, pnl):
        if pnl < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

        if self.loss_streak >= self.max_loss_streak:
            self.locked = True
            print(f"🚨 [SAFETY] 连续亏损触发，系统冻结")
            return False

        return True

    # =========================
    # 3. 全局交易开关
    # =========================
    def allow_trade(self):
        return not self.locked

    def unlock(self):
        self.locked = False
        self.loss_streak = 0
        print("🟢 [SAFETY] 系统已解锁")
