"""Logic to create and populate DB"""
import logging
from typing import Dict

import muttlib
import pandas as pd
from muttlib.dbconn import get_client
from muttlib.utils import convert_to_snake_case
from pangres import upsert
from sqlalchemy import create_engine

from localpg.cfg import PARENT_LOGGER, PG_CFG, get_uri_db_pg
from localpg.constants import BIDMC_PPG_PATH
from localpg.schemas import MAPPER_PG, SPARSE_COLS, BIDMC_PPG_COLS


logger = logging.getLogger(f"{PARENT_LOGGER}.{__name__}")


def get_bidmc_ppg_data():
    """Fetch & prepare dataset for loading.

    Returns
    -------
    df : pd.DataFrame
        BIDMC Signals' dataset for all subjects.

    """
    dfs = []
    for s in range(1, 54):  # 54 subjects
        filepath = BIDMC_PPG_PATH / f"bidmc_{s}_Signals.csv"
        frame = pd.read_csv(filepath, skipinitialspace=True)
        frame["subject"] = str(s)
        dfs.append(frame)

    df = pd.concat(dfs).reset_index(drop=True)
    df.rename(convert_to_snake_case, axis=1, inplace=True)
    df.rename({"time [s]": "ds"}, axis=1, inplace=True)
    df.drop(columns=SPARSE_COLS, inplace=True)  # too much nulls
    df.drop_duplicates(subset=["ds", "subject"], inplace=True)
    return df


def get_db_client(creds: Dict[str, str]) -> muttlib.dbconn.BaseClient:
    """Get db client using get_client method from muttlib.dbconn.

    Parameters
    ----------
    creds : dict
        Credentials that contains a structure like this:
            username: user
            password: pwd
            host: localhost
            port: 5432
            database: db_name
            db_type: db (see muttlib documentation).

    Returns
    -------
    db_cli : Client object
        Client object of certain database (like pg, oracle, etc)

    """
    _, db_cli = get_client(creds)
    return db_cli


def insert_df_to_postgres(df: pd.DataFrame, table: str):
    """Prepare and insert dataframe to postgresql.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to be inserted.
    table : str
        Table name.

    """
    breakpoint()
    logger.info(f"Insert {table} into DB")
    engine = create_engine(get_uri_db_pg(PG_CFG))
    df = df[MAPPER_PG[table]["ORDER_SCHEMA"]]
    df.columns = MAPPER_PG[table]["SCHEMA"]
    logger.info(f"DF to be loaded \n {df} ")
    logger.info(f"DF columns \n {df.columns} ")
    df = df[df[MAPPER_PG[table]["KEY_COLS"][1]].notna()]
    logger.info(f"Going to insert {table} DF: \n {df.head()}")
    df = df.set_index(MAPPER_PG[table]["KEY_COLS"])
    upsert(engine=engine, df=df, table_name=table, if_row_exists="update")
    logging.info(f"{len(df)} rows inserted in {table}")
    logging.info("Load process finished.")


if __name__ == "__main__":
    df = get_bidmc_ppg_data()
    insert_df_to_postgres(df, "BidmcPggRespiration")
