python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/Debug/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "Local-Test-Segment-01" \
    --keyframes "Segment-01-Keyframes.csv" \
    --frames "Segment-01-Frames.csv" \
    --map "Segment-01-Map.msg" \
    --threshold 0.3 \
    --bias 1.1 \
    --show_fig \
    --save_fig \
    --save \
    --win \
    --win_length 20 \
