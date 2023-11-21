from threading import Thread
from typing import List

import cv2
import numpy as np

from inference.core.interfaces.camera.entities import StatusUpdate
from inference.core.interfaces.camera.multiplexer import StreamMultiplexer
from inference.core.interfaces.camera.video_source import VideoSource
from inference.core.utils.preprocess import letterbox_image

SOURCES_LOOKUP = {
    "hippos": "https://zssd-hippo.hls.camzonecdn.com/CamzoneStreams/zssd-hippo/chunklist.m3u8",
    "pandas": "https://zssd-panda.hls.camzonecdn.com/CamzoneStreams/zssd-panda/chunklist.m3u8",
    "elephants": "https://elephants.hls.camzonecdn.com/CamzoneStreams/elephants/chunklist.m3u8",
    "penguins": "https://zssd-penguin.hls.camzonecdn.com/CamzoneStreams/zssd-penguin/chunklist.m3u8",
    "polar-bears": "https://polarplunge.hls.camzonecdn.com/CamzoneStreams/polarplunge/chunklist.m3u8",
    "giraffes": "https://zssd-kijami.hls.camzonecdn.com/CamzoneStreams/zssd-kijami/chunklist.m3u8",
}

LOCAL_LOOKUP = {
    "0": "rtsp://localhost:8554/live0.stream",
    "1": "rtsp://localhost:8554/live1.stream",
    "2": "rtsp://localhost:8554/live2.stream",
    "3": "rtsp://localhost:8554/live3.stream",
    "4": "rtsp://localhost:8554/live4.stream",
    "5": "rtsp://localhost:8554/live5.stream",
    "6": "rtsp://localhost:8554/live6.stream",
    "7": "rtsp://localhost:8554/live7.stream",
    "8": "rtsp://localhost:8554/live8.stream",
}

STOP = False


def main() -> None:
    stream_uris = list(LOCAL_LOOKUP.values())
    cameras = [VideoSource.init(uri, status_update_handlers=[]) for uri in stream_uris]
    for camera in cameras:
        camera.start()
    multiplexer = StreamMultiplexer(sources=cameras)
    control_thread = Thread(target=command_thread, args=(cameras,))
    control_thread.start()
    previous_frames = [
        np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(len(cameras))
    ]
    while not STOP:
        new_frames = multiplexer.get_frames()
        for i in range(len(new_frames)):
            if new_frames[i] is not None:
                previous_frames[i] = letterbox_image(
                    image=new_frames[i][-1], desired_size=(640, 480)
                )
        top_row = np.concatenate(
            [
                previous_frames[0],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[1],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[2],
            ],
            axis=1,
        )
        mid_row = np.concatenate(
            [
                previous_frames[3],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[4],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[5],
            ],
            axis=1,
        )
        bottom_row = np.concatenate(
            [
                previous_frames[6],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[7],
                np.zeros((480, 10, 3), dtype=np.uint8),
                previous_frames[8],
            ],
            axis=1,
        )
        image = np.concatenate(
            [
                top_row,
                np.zeros((10, 1940, 3), dtype=np.uint8),
                mid_row,
                np.zeros((10, 1940, 3), dtype=np.uint8),
                bottom_row,
            ],
            axis=0,
        )
        cv2.imshow("Stream", image)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    control_thread.join()


def command_thread(cameras: List[VideoSource]) -> None:
    global STOP
    while not STOP:
        idx, key = input().split(",")
        idx = int(idx)
        if key == "q":
            continue
        elif key == "i":
            print(cameras[idx].describe_source())
        elif key == "t":
            for c in cameras:
                c.terminate()
            STOP = True
        elif key == "p":
            cameras[idx].pause()
        elif key == "m":
            cameras[idx].mute()
        elif key == "r":
            cameras[idx].resume()
        elif key == "re":
            cameras[idx].restart()


def dump_status_update(status_update: StatusUpdate) -> None:
    print(status_update)


if __name__ == "__main__":
    main()
