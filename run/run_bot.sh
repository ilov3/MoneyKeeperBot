#!/bin/bash
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $CURRENT_DIR/../
python -m MoneyKeeperBot.app CURRENT_DIR/../MoneyKeeperBot/app.py