python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/Debug/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-02.csv" \
    --name "Global-Test-Segment-05" \
    --keyframes "Segment-05-Keyframes.csv" \
    --frames "Segment-05-Frames.csv" \
    --map "Segment-05-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --show_fig \
