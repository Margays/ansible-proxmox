import semver
import argparse
from pathlib import Path


def find_galaxy_config() -> Path:
    path = Path(__file__).parent
    while path != Path("/"):
        galaxy_config = path.joinpath("galaxy.yml")
        if galaxy_config.exists():
            return galaxy_config

        path = path.parent

    raise FileNotFoundError("galaxy.yml not found")


def load_galaxy_config(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_galaxy_config(path: Path, config: dict) -> None:
    with open(path, "w") as f:
        yaml.dump(config, f)


def main() -> None:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--type", choices=["major", "minor", "patch"], required=True)
    args = arg_parser.parse_args()

    galaxy_config = find_galaxy_config()
    config = load_galaxy_config(galaxy_config)
    version = semver.VersionInfo.parse(config["version"])

    match args.type:
        case "patch":
            new_version = version.bump_patch()
        case "minor":
            new_version = version.bump_minor()
        case "major":
            new_version = version.bump_major()

    config["version"] = str(new_version)
    save_galaxy_config(galaxy_config, config)


if __name__ == "__main__":
    main()
