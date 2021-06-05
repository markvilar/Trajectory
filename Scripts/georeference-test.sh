python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/Comparison/" \
    --output "/home/martin/dev/Trajectory/Data/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "CLAHE" \
    --keyframes "CLAHE-04-Keyframes.csv" \
    --frames "CLAHE-04-Frames.csv" \
    --map "CLAHE-04-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save \
    --save_fig \
    --show_fig \
