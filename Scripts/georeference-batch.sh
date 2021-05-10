# -----------------------------------------------------------------------------
# ---- Dive 1 -----------------------------------------------------------------
# -----------------------------------------------------------------------------

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-01-Keyframes.csv" \
    --frames "Segment-01-Frames.csv" \
    --map "Segment-01-Map.msg" \
    --pos "Segment-01-Positions.csv" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-02-Keyframes.csv" \
    --frames "Segment-02-Frames.csv" \
    --pos "Segment-02-Positions.csv" \
    --map "Segment-02-Map.msg" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-03-Keyframes.csv" \
    --frames "Segment-03-Frames.csv" \
    --pos "Segment-03-Positions.csv" \
    --map "Segment-03-Map.msg" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-04-Keyframes.csv" \
    --frames "Segment-04-Frames.csv" \
    --pos "Segment-04-Positions.csv" \
    --map "Segment-04-Map.msg" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-05-Keyframes.csv" \
    --frames "Segment-05-Frames.csv" \
    --pos "Segment-05-Positions.csv" \
    --map "Segment-05-Map.msg" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-06-Keyframes.csv" \
    --frames "Segment-06-Frames.csv" \
    --pos "Segment-06-Positions.csv" \
    --map "Segment-06-Map.msg" \
    --aps "Dive-01-ROV-APS.csv" \
    --gyro "Dive-01-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

# -----------------------------------------------------------------------------
# ---- Dive 2 -----------------------------------------------------------------
# -----------------------------------------------------------------------------

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-07-Keyframes.csv" \
    --frames "Segment-07-Frames.csv" \
    --pos "Segment-07-Positions.csv" \
    --map "Segment-07-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-08-Keyframes.csv" \
    --frames "Segment-08-Frames.csv" \
    --pos "Segment-08-Positions.csv" \
    --map "Segment-08-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-09-Keyframes.csv" \
    --frames "Segment-09-Frames.csv" \
    --pos "Segment-09-Positions.csv" \
    --map "Segment-09-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-10-Keyframes.csv" \
    --frames "Segment-10-Frames.csv" \
    --pos "Segment-10-Positions.csv" \
    --map "Segment-10-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-11-Keyframes.csv" \
    --frames "Segment-11-Frames.csv" \
    --pos "Segment-11-Positions.csv" \
    --map "Segment-11-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-12-Keyframes.csv" \
    --frames "Segment-12-Frames.csv" \
    --pos "Segment-12-Positions.csv" \
    --map "Segment-12-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-13-Keyframes.csv" \
    --frames "Segment-13-Frames.csv" \
    --pos "Segment-13-Positions.csv" \
    --map "Segment-13-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

python Python/run_georeferencing.py \
    --slam "/home/martin/dev/Trajectory/Data/SLAM/CLAHE/" \
    --navi "/home/martin/dev/Trajectory/Data/Navigation/" \
    --output "/home/martin/dev/Trajectory/Output/" \
    --keyframes "Segment-14-Keyframes.csv" \
    --frames "Segment-14-Frames.csv" \
    --pos "Segment-14-Positions.csv" \
    --map "Segment-14-Map.msg" \
    --aps "Dive-02-ROV-APS.csv" \
    --gyro "Dive-02-ROV-Gyroscope.csv" \
    --threshold 0.3 \
    --bias 0.0 \
    --save \

