import pkg_resources
from argparse import ArgumentParser
from os.path import join as join_path
from malibu_lib.sprite import load_spec


def get_opts():
    ap = ArgumentParser()
    ap.add_argument("--asset-package", type=str, default="malibu")
    ap.add_argument("SPRITE", type=str, help="The location of the sprite file to load.")
    return ap.parse_args()


def sprite_path(sprite_name):
    return join_path("assets", "sprites", f"{sprite_name}.yaml")


def sheet_path(sheet_name):
    ...


def main():
    opts = get_opts()
    with pkg_resources.resource_stream(opts.asset_package, sprite_path(opts.SPRITE)) as fd:
        spec = load_spec(fd)
    print(spec)


if __name__ == "__main__":
    main()
