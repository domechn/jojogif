from video import VideoService


def main():
    vs = VideoService('test.mp4')
    vs.to_gif()


if __name__ == "__main__":
    main()
