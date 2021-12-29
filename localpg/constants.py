"""Constant values and defaults used in multiple modules."""
from pathlib import Path

import pandas as pd
from pkg_resources import resource_filename

LOCALPG_PATH = Path(resource_filename("localpg", "/"))
REPO_ROOT = LOCALPG_PATH.parent
RESOURCES_DIR = LOCALPG_PATH / "resources"
LOG_DIR = RESOURCES_DIR / "logs"
SQL_DIR = RESOURCES_DIR / "sql"
DATA_DIR = RESOURCES_DIR / "data"
PARENT_LOGGER = "localpg"
DB_NAME = "dev"
PG_PORT_DEFAULT = 5432

BIDMC_PPG_PATH = DATA_DIR / "bidmc_csv"
