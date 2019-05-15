from video import VideoService
import click


@click.command()
@click.option('--path', default='', help='the path of vedio')
@click.option('--begin', default=0, help='from which time to start generate gif')
@click.option('--end', default=0, help='from which time to end generate gif')
def main(path: str, begin: float, end: float):
    if not path:
        print("error: path must not be None")
        return
    vs = VideoService(path, begin=begin, end=end)
    vs.to_gif()


if __name__ == "__main__":
    main()
