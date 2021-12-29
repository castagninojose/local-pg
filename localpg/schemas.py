PKEY_USER_ID = "subject"

SPARSE_COLS = ["cvp", "abp", "art", "i", "mcl", "iii"]

BIDMC_PPG_COLS = [
    "ds",
    "subject",
    "resp",
    "pleth",
    "v",
    "avr",
    "ii",
]


MAPPER_PG = {
    "BidmcPggRespiration": {
        "ORDER_SCHEMA": BIDMC_PPG_COLS,
        "SCHEMA": BIDMC_PPG_COLS,
        "KEY_COLS": ["ds", "subject"],
    }
}
