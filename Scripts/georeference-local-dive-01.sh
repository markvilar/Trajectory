python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "Local-Segment-01" \
    --keyframes "Segment-01-Keyframes.csv" \
    --frames "Segment-01-Frames.csv" \
    --map "Segment-01-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \
    --win \
    --win_length 15 \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "Local-Segment-02" \
    --keyframes "Segment-02-Keyframes.csv" \
    --frames "Segment-02-Frames.csv" \
    --map "Segment-02-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \
    --win \
    --win_length 15 \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "Local-Segment-03" \
    --keyframes "Segment-03-Keyframes.csv" \
    --frames "Segment-03-Frames.csv" \
    --map "Segment-03-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \
    --win \
    --win_length 15 \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --gt \
        "/home/martin/dev/Trajectory/Data/Navigation/Ground-Truth-Dive-01.csv" \
    --name "Local-Segment-04" \
    --keyframes "Segment-04-Keyframes.csv" \
    --frames "Segment-04-Frames.csv" \
    --map "Segment-04-Map.msg" \
    --threshold 0.3 \
    --bias 0.6 \
    --save_fig \
    --save \
    --win \
    --win_length 15 \

