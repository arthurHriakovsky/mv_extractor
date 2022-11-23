import numpy as np
import subprocess
import os
import cv2


def ffmpeg_encode(frame1: np.ndarray, frame2: np.ndarray, temp_dir: str, motion_vectors_executable: str):
    """
    Returns motion-vectors that were generated using FFmpeg.

    :param frame1: A frame as a Numpy array.
    :param frame2: A frame as a Numpy array.
    :param temp_dir: A directory to save temporary files to.
    """
    cv2.imwrite(f'{temp_dir}/0.png', frame1)
    cv2.imwrite(f'{temp_dir}/1.png', frame2)
    subprocess.run(['ffmpeg', '-i', f'%d.png', '-input_format', 'yuv420p', '-c:v', 'h264',
                    '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', f'{temp_dir}/out.mp4'])
    motion_data = subprocess.run([motion_vectors_executable, f'{temp_dir}/out.mp4'],
                                 stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    os.remove(f'{temp_dir}/out.mp4')
    motion_data = motion_data.stdout.decode().strip().split('\n')
    vectors = []
    for i in range(1, len(motion_data)):
        frame_num, _, block_width, block_height, src_x, src_y, dst_x, dst_y, _ = eval(motion_data[i])
        vectors.append((src_x, src_y, dst_x, dst_y))
    return vectors


frame1 = cv2.imread('0.png')
frame2 = cv2.imread('1.png')
temp_dir_path = '/home/txp1/lab_projects/mv_of_2_frames/temp/'
mv_extraction_executable = '/home/txp1/lab_projects/mv_of_2_frames/motionVectors'
a = ffmpeg_encode(frame1, frame2, temp_dir_path, mv_extraction_executable)
cv2.imshow('image', frame1)
cv2.waitKey(10000)
cv2.destroyAllWindows()