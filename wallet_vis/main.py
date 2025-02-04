import json
import logging
import logging.config
import os

import matplotlib.pyplot as plt

from wallet_vis.constants import LOGGING_CONFIG_FILE_PATH, OUTPUT_DIR_NAME, PIE_CHART_PATH
from wallet_vis.wallet import Wallet


def setup_logging(config_path: str) -> None:
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            logging.config.dictConfig(config)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).exception(f"Failed to load logging config: {e}")


def main():
    os.makedirs(OUTPUT_DIR_NAME, exist_ok=True)
    setup_logging(LOGGING_CONFIG_FILE_PATH)
    logger = logging.getLogger(__name__)
    
    try:
        wallet = Wallet()
    except Exception as e:
        logger.exception(f"Failed to initialize wallet: {e}")
        return

    if not wallet.financial_assets:
        logger.error("No financial assets to display.")
        return

    labels = [fa.long_name for fa in wallet.financial_assets]
    values = [fa.value for fa in wallet.financial_assets]

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(18, 8))
    
    ax1.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
    ax1.set_title("Financial Assets Distribution")
    ax1.axis('equal')
    
    bars = ax2.barh(labels, values, color='skyblue')
    ax2.set_xlabel("Value")
    ax2.set_title("Value of Each Financial Asset")
    
    for bar in bars:
        width = bar.get_width()
        ax2.text(width, bar.get_y() + bar.get_height() / 2, f' {width:.2f}', 
                 va='center', ha='left', color='blue', fontsize=9)

    try:
        fig.tight_layout()
        fig.savefig(PIE_CHART_PATH)
        logger.info(f"Combined chart saved to {PIE_CHART_PATH}")
    except Exception as e:
        logger.exception(f"Failed to save combined chart: {e}")
    plt.close(fig)

if __name__ == "__main__":
    main()

