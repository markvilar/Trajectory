python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/SLAM/Comparison-Georeferenced/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "RAW" \
    --keyframes "RAW-01-Keyframes.csv" \
    --frames "RAW-01-Frames.csv" \
    --map "RAW-01-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/SLAM/Comparison-Georeferenced/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "BLF" \
    --keyframes "BLF-04-Keyframes.csv" \
    --frames "BLF-04-Frames.csv" \
    --map "BLF-04-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/SLAM/Comparison-Georeferenced/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "HE" \
    --keyframes "HE-08-Keyframes.csv" \
    --frames "HE-08-Frames.csv" \
    --map "HE-08-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/SLAM/Comparison-Georeferenced/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "CLAHE" \
    --keyframes "CLAHE-04-Keyframes.csv" \
    --frames "CLAHE-04-Frames.csv" \
    --map "CLAHE-04-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/SLAM/Comparison-Georeferenced/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "UIENet" \
    --keyframes "UIENet-01-Keyframes.csv" \
    --frames "UIENet-01-Frames.csv" \
    --map "UIENet-01-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \
