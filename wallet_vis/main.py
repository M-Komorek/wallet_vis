
import logging
import logging.config
import json
import os

import matplotlib.pyplot as plt

from wallet_vis.constants import LOGGING_CONFIG_FILE_PATH, OUTPUT_DIR_NAME, PIE_CHART_PATCH
from wallet_vis.wallet import Wallet


def setup_logging(config_path):
    with open(config_path, 'r') as file:
        config = json.load(file)
        logging.config.dictConfig(config)


def main():
    os.makedirs(OUTPUT_DIR_NAME, exist_ok=True)
    setup_logging(LOGGING_CONFIG_FILE_PATH)

    wallet = Wallet()

    labels = [fa.long_name for fa in wallet.financial_assets]
    values = [fa.value for fa in wallet.financial_assets]

    plt.figure(figsize=(10,10))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Financial Assets Distribution")
    plt.axis('equal')  
    plt.savefig(PIE_CHART_PATCH)


if __name__ == "__main__":
    main()
