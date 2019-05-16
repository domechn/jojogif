from video import VideoService
import click


@click.command()
@click.option('--path', default='', help='the path of vedio')
@click.option('--out-path', default='./', help='out path')
@click.option('--begin', default=0, help='from which time to start generate gif', type=float)
@click.option('--end', default=0, help='from which time to end generate gif', type=float)
@click.option('--size', default='', help='the size of gif')
@click.option('--jojo', default=False, help='add to be continued', type=bool)
def main(path, out_path: str, begin, end: float, size: str, jojo: bool):
    try:
        if not path:
            raise RuntimeError("error: path must not be None")
        width, height = parse_size(size)
    except RuntimeError as e:
        print(str(e))
        return
    vs = VideoService(path, begin, end, width, height)
    vs.to_images()
    vs.to_gif(jojo, out_path)


def parse_size(size: str):
    if not size:
        return 0, 0
    sizes = size.upper().split('X')
    if len(sizes) != 2:
        raise RuntimeError("size is invalid, ex: 200x200")
    return int(sizes[0]), int(sizes[1])


if __name__ == "__main__":
    main()
