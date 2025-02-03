
import logging
import logging.config
import json

import matplotlib.pyplot as plt

from wallet import Wallet


def setup_logging(config_path='logging_config.json'):
    with open(config_path, 'r') as file:
        config = json.load(file)
        logging.config.dictConfig(config)


def main():
    setup_logging()
    wallet = Wallet()

    labels = [fa.long_name for fa in wallet.financial_assets]
    values = [fa.value for fa in wallet.financial_assets]


    plt.figure(figsize=(10,10))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Financial Assets Distribution")
    plt.axis('equal')  
    plt.savefig("portfolio_distribution.png")


if __name__ == "__main__":
    main()
