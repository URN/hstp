import argparse

import hstp.audioboom


def main():
    parser = argparse.ArgumentParser(
        prog='python -m audioboom-downloader',
        description='Download Audioboom podcasts'
    )

    parser.add_argument("id", help="The ID of the audioboom channel")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-o", "--output", help="output directory", default=".")

    args = parser.parse_args()

    c = audioboom.Channel(args.id)

    c.get_episodes()
    c.get_playlists()

    c.save(args.output)


if __name__ == "__main__":
    main()
