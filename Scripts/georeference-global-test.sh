python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/Segment-01/" \
    --gt "/home/martin/dev/Trajectory/Data/Navigation/Groundtruth-Dive-01.csv" \
    --keyframes "Segment-01-Keyframes.csv" \
    --frames "Segment-01-Frames.csv" \
    --map "Segment-01-Map.msg" \
    --threshold 0.3 \
    --bias 0.0 \
    --show_fig \
