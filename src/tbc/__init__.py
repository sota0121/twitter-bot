from email.policy import default
import sys
from typing import Optional

import click

from tbc.tbclib.constants import *
from tbc.tbclib.make_tweets_list import TweetTableMaker
from tbc.tbclib.send_tweet import send_tweet, send_tweet_from_cli
from tbc.tbclib.config_parser import *


# Command Collection
# https://click.palletsprojects.com/en/8.0.x/commands/
# https://click.palletsprojects.com/en/8.0.x/commands/#merging-multi-commands


# tbc
@click.group(name='tbc')
def main() -> None:
    click.echo("Welcome to tbc !!!")


# tbc bot
@main.group(
    name='bot',
    help="bot operation command"
)
def bot() -> None:
    click.echo("bot sub command !!!")


# tbc bot send
@bot.command()
@click.option(
    "-m",
    "--msg",
    type=str,
    help=(
        "[Option] Message to send"
        "e.g. tbc send -m \"Hello Twitter!\""
    )
)
@click.option(
    "-i",
    "--img-file",
    type=str,
    help=(
        "[Option] Image file path to upload"
        "e.g. tbc send -i ./test.jpg"
    )
)
@click.option(
    "-c",
    "--config",
    type=str,
    default=".tbcconfig.yml",
    help=(
        "[Option] config file path\n"
        "default: .tbcconfig.yml\n"
        "e.g. tbc --config .tbcconfig.yml send ..."
    )
)
def send(msg: Optional[str]=None,
         img_file: Optional[str]=None,
         config: Optional[str]=None) -> None:
    """send tweet command"""
    # Parse config args
    cfg: TbcConfig = TbcConfig()
    if config is not None:
        click.echo(f"load : {config}")
        cfg = CfgParser.load(config)

    # Check values
    if not cfg.twitter_tokens_exist():
        print(MSG_ERR_NOT_FOUND_APIKEY)
        sys.exit(1)

    # Parse message args
    if msg is None:
        print("No message is set.")
    else:
        _msg_text = msg
        try:
            if img_file is None:
                send_tweet_from_cli(cfg, _msg_text)
            else:
                send_tweet_from_cli(cfg, _msg_text, img_file)
            print("successfully tweeted")
        except Exception as e:
            print(f"something is wrong ... ({repr(e)})")


# tbc config
@main.group(
    name="config",
    help="config operation command"
)
def config() -> None:
    click.echo("tbc config !!!")


# tbc config get
@config.command(name="get")
@click.option(
    "-k",
    "--keyname",
    type=str,
    help=(
        "select key name of\n"
        "config values\n"
    )
)
def cfg_get(keyname: str) -> None:
    """tbc config get"""
    cfg_obj: TbcConfig = CfgParser.load(CfgParser.default_cfg_name())
    target_val = cfg_obj.get_val(keyname)
    print(f"{keyname}={target_val}")


# tbc config list
@config.command(name="list")
def cfg_list() -> None:
    """tbc config list"""
    cfg_obj: TbcConfig = CfgParser.load(CfgParser.default_cfg_name())
    for k, v in cfg_obj.get_all_items():
        print(k, "=", v)

# @click.option(
#     "-s",
#     "--secret",
#     type=str,
#     help=(
#         "config file path that secrets keys are written"
#         "e.g. tbc config --secret ./env.yml"
#     )
# )
# def config(secret: Optional[str]=None) -> None:
#     """config operation"""
#     # Parse args
#     # -- config secret
#     if secret is not None:
#         click.echo(f"load : {secret}")
#         CfgParser(secret)


if __name__ == "__main__":
    main()
