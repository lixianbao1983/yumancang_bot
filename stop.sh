#!/bin/bash

echo "Stopping trading bot..."

python3 -c "from state_manager import StateManager; s=StateManager(); s.set('running', False)"

echo "STOP signal sent."
