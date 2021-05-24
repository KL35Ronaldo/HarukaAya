#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2021 Akito Mizukito (Haruka Aita)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import sys
import yaml
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Set, Any

from telethon import TelegramClient
import telegram.ext as tg


class HarukaConfig(BaseModel):
    """
    Haruka configuration class
    """

    api_id: int
    api_hash: str
    bot_token: str
    database_url: str
    load: List[str]
    no_load: List[str]
    del_cmds: Optional[bool] = False
    strict_antispam: Optional[bool] = False
    workers: Optional[int] = 4
    owner_id: int
    sudo_users: Set[int]
    whitelist_users: Set[int]
    message_dump: Optional[int] = 0
    spamwatch_api: Optional[str] = ""
    spamwatch_client: Optional[Any] = None
    telethon_client: Optional[Any] = None
    updater: Optional[Any] = None
    dispatcher: Optional[Any] = None


logging.basicConfig(
    format=
    "[%(levelname)s %(asctime)s] Module '%(module)s', function '%(funcName)s' at line %(lineno)d -> %(message)s",
    level=logging.INFO)
logging.info("Starting haruka...")

if sys.version_info < (3, 8, 0):
    logging.error(
        "Your Python version is too old for Haruka to run, please update to Python 3.8 or above"
    )
    exit(1)

try:
    config_file = dict(
        yaml.load(open('config.yml', 'r'), Loader=yaml.SafeLoader))
except Exception as error:
    logging.error(
        f"Could not load config file due to a {type(error).__name__}: {error}")
    exit(1)

if not config_file['is_example_config_or_not'] == "not_sample_anymore":
    logging.warning(
        "Please make sure that your configuration file is correct, refusing to start"
    )
    exit(1)
config_file.pop("is_example_config_or_not")

try:
    CONFIG = HarukaConfig(**config_file)
except ValidationError as validation_error:
    logging.error(
        f"Something went wrong when parsing config.yml: {validation_error}")
    exit(1)

CONFIG.sudo_users.add(CONFIG.owner_id)

try:
    CONFIG.updater = tg.Updater(CONFIG.bot_token, workers=CONFIG.workers)
    CONFIG.dispatcher = CONFIG.updater.dispatcher
    CONFIG.telethon_client = TelegramClient("haruka", CONFIG.api_id,
                                            CONFIG.api_hash)

    # We import it now to ensure that all previous variables have been set
    from haruka.modules.helper_funcs.handlers import CustomCommandHandler, CustomMessageHandler
    tg.CommandHandler = CustomCommandHandler
    tg.MessageHandler = CustomMessageHandler
except Exception as telegram_error:
    logging.error(
        f"Could not initialize Telegram client due to a {type(telegram_error).__name__}: {telegram_error}"
    )
    exit(1)
