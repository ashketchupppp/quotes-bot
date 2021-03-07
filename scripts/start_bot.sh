#!/usr/bin/bash

# arguments should be in the following order:
# 1 : The MongoDB collection to use
# 2 : The discord token to use
# 3 : The discord guild to use
# 4 : The quotes channel to use
# 5 : The leave channel to use

python3 ../src/bot.py -d $1 -t $2 -g $3 -qc $4 -lc $5 
