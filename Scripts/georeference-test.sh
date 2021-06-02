python Python/run_georeferencing.py \
    --slam \
    "/home/martin/dev/Trajectory/Data/SLAM/Test-260521/" \
    --output \
    "/home/martin/dev/Trajectory/Data/Output/Test-260521/" \
    --gt \
    "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "RAW-Test" \
    --keyframes "RAW-Keyframes.csv" \
    --frames "RAW-Frames.csv" \
    --map "RAW-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --show_fig \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam \
    "/home/martin/dev/Trajectory/Data/SLAM/Test-260521/" \
    --output \
    "/home/martin/dev/Trajectory/Data/Output/Test-260521/" \
    --gt \
    "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "BLF-Test" \
    --keyframes "BLF-Keyframes.csv" \
    --frames "BLF-Frames.csv" \
    --map "BLF-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --show_fig \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam \
    "/home/martin/dev/Trajectory/Data/SLAM/Test-260521/" \
    --output \
    "/home/martin/dev/Trajectory/Data/Output/Test-260521/" \
    --gt \
    "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "HE-Test" \
    --keyframes "HE-Keyframes.csv" \
    --frames "HE-Frames.csv" \
    --map "HE-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --show_fig \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam \
    "/home/martin/dev/Trajectory/Data/SLAM/Test-260521/" \
    --output \
    "/home/martin/dev/Trajectory/Data/Output/Test-260521/" \
    --gt \
    "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "CLAHE-Test" \
    --keyframes "CLAHE-Keyframes.csv" \
    --frames "CLAHE-Frames.csv" \
    --map "CLAHE-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --show_fig \
    --save_fig \
    --save \

