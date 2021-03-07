#!/bin/bash
sudo docker run -v mongodata:/data/db -p 27017:27017 --name mongodb -d mongo
