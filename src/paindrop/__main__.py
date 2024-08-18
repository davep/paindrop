##############################################################################
# Python imports.
from argparse import ArgumentParser, Namespace
from itertools import batched
from json import loads
from pathlib import Path
from typing import Any

##############################################################################
# Use requests.
import requests

##############################################################################
def log(*lines: str) -> None:
    """Log some text to the console."""
    for line in lines:
        print(line)

##############################################################################
def download_pins(token: str) -> list[dict[str, str]]:
    """Download the pins from Pinboard.

    Args:
        token: The Pinboard API token.

    Returns:
        The data exported from Pinboard.

    Note:
        If `token` matches the name of a file within the local filesystem,
        it will be read and parsed as JSON instead. This means it can act as
        a simple cache.
    """
    if Path(token).exists():
        return loads(Path(token).read_text())
    return requests.get(f"https://api.pinboard.in/v1/posts/all?auth_token={token}&format=json").json()

##############################################################################
def upload_raindrops(token: str, raindrops: list[dict[str, Any]]) -> None:
    """Upload converted raindrops to Raindops.

    Args:
        token: The Access token for Raindrop.
        raindrops: The raindrops to upload.
    """
    for progress, batch in enumerate(batched(raindrops, 100)):
        log(f"Uploading raindrop batch {progress}")
        requests.post(
            "https://api.raindrop.io/rest/v1/raindrops",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={"items": batch}
        )
        log(f"Finished raindrop batch {progress}")

##############################################################################
def to_raindrop(pin: dict[str, str], public: int, private: int) -> dict[str, Any]:
    """Convert a single pin into a raindrop.

    Args:
        pin: The pin to convert.
        public: The ID of the public collection.
        private: The ID of the private collection.

    Returns:
        The raindrop made from the pin.
    """
    raindrop = {
        "link": pin["href"],
        "title": pin["description"],
        "note": pin["extended"],
        "created": pin["time"],
        "lastUpdate": pin["time"],
        "tags": pin["tags"].split(),
    }
    if pin["toread"] == "no":
        raindrop["collection"] = {
            "$id": public if pin["shared"] == "yes" else private
        }
    return raindrop

##############################################################################
def convert(pins: list[dict[str, str]], public: int, private: int) -> list[dict[str, Any]]:
    """Convert a list of pins into a list of raindrops.

    Args:
        pins: The pins to convert.

    Returns:
        A list of raindrops for uploading.
    """
    return [to_raindrop(pin, public, private) for pin in pins]

##############################################################################
def find_collections(arguments: Namespace) -> tuple[int | None, int | None]:
    """Find the collections in Raindrop.

    Args:
        arguments: The command line arguments.

    Returns:
        A tuple of the public and private collection IDs, or `None` for
        either that can't be found.
    """
    collections = requests.get(
        "https://api.raindrop.io/rest/v1/collections",
        headers={
            "Authorization": f"Bearer {arguments.raindrop_token}"
        }
    ).json()
    public, private = None, None
    if collections["result"]:
        for collection in collections["items"]:
            match (collection["title"], collection["_id"]):
                case (arguments.public, _id):
                    public = _id
                case (arguments.private, _id):
                    private = _id
    return public, private

##############################################################################
def get_args() -> Namespace:
    """Get the command line arguments.

    Returns:
        The command line arguments.
    """
    parser = ArgumentParser(
        prog="paindrop",
        description="A tool for importing pins from Pinboard, into Raindrop",
    )

    parser.add_argument("pinboard_token")
    parser.add_argument("raindrop_token")
    parser.add_argument(
        "-u", "--public",
        default="Public",
        help="The name of the public collection in Raindrop"
    )
    parser.add_argument(
        "-r", "--private",
        default="Private",
        help="The name of the private collection in Raindrop"
    )

    return parser.parse_args()

##############################################################################
def main() -> None:
    """Main entry point for the utility."""
    arguments = get_args()
    log("Downloading pins from Pinboard")
    pins = download_pins(arguments.pinboard_token)
    log(f"Downloaded {len(pins)} pins from Pinboard")
    log("Finding Public and Private collections in Raindrop")
    public, private = find_collections(arguments)
    if public is None:
        log(f"Could not find public collection named '{arguments.public}'")
        exit(1)
    else:
        log(f"Found public collection named '{arguments.public}' ({public})")
    if private is None:
        log(f"Could not find private collection named '{arguments.private}'")
        exit(1)
    else:
        log(f"Found private collection named '{arguments.private}' ({private})")
    upload_raindrops(arguments.raindrop_token, convert(pins, public, private))

##############################################################################
# Allow running as a module.
if __name__ == "__main__":
    main()

### __main__.py ends here
