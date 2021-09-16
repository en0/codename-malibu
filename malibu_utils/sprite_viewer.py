import pkg_resources
from argparse import ArgumentParser
from os.path import join as join_path
from yaml import safe_load


def get_opts():
    ap = ArgumentParser()
    ap.add_argument("SPRITE", type=str, help="The location of the sprite file to load.")
    return ap.parse_args()


def sprite_path(sprite_name):
    return join_path("assets", "sprites", f"{sprite_name}.yaml")


def sheet_path(sheet_name):
    ...


def main():
    opts = get_opts()
    with pkg_resources.resource_stream("malibu", sprite_path(opts.SPRITE)) as fd:
        sprite_desc = safe_load(fd)


if __name__ == "__main__":
    main()
