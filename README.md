# CameraWebots
Reading images from Nao v6 in Webots.

# How to start
0.1 Download appropriate WebotsLoLa version:

git clone https://github.com/Starkit-SPL/WebotsLoLa.git 

0.2 Download application for reading images:

git clone https://github.com/Starkit-SPL/CameraWebots.git

1. Start in Webots world 'WebotsLoLa/worlds/naorobocup.wbt'

2. In terminal:

ros2 run nao_lola nao_lola

3. In another terminal:

cd CameraWebots/

python3 client.py
