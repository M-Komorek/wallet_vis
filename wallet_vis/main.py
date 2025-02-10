import json
import logging
import logging.config
import os

import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke

from wallet_vis.constants import (
    LOGGING_CONFIG_FILE_PATH,
    OUTPUT_DIR_NAME,
    PIE_CHART_PATH,
)
from wallet_vis.wallet import Wallet


def setup_logging(config_path: str) -> None:
    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            logging.config.dictConfig(config)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger(__name__).exception(f"Failed to load logging config: {e}")


def configure_dark_theme():
    plt.style.use("dark_background")
    plt.rcParams.update(
        {
            "figure.facecolor": "#121212",
            "axes.facecolor": "#121212",
            "axes.edgecolor": "#606060",
            "axes.labelcolor": "#FFFFFF",
            "text.color": "#FFFFFF",
            "xtick.color": "#CCCCCC",
            "ytick.color": "#CCCCCC",
            "grid.color": "#4A4A4A",
            "font.size": 9,
        }
    )


def generate_colors(num_colors: int) -> list:
    cmap = plt.colormaps["tab20"]
    return [cmap(i % 20) for i in range(num_colors)]


def create_bar_chart(ax, labels, values, colors, accent_color: str):
    bars = ax.barh(
        labels, values, color=colors, height=0.7, edgecolor="#606060", linewidth=0.8
    )
    ax.set_xlabel("Total Value", fontsize=12, labelpad=10)
    ax.set_title("Total Value by Asset", fontsize=14, pad=15, weight="semibold")
    ax.grid(axis="x", linestyle=":", alpha=0.8)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for bar in bars:
        ax.text(
            350,
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():,.2f}",
            va="center",
            color=accent_color,
            fontsize=9,
            fontweight="semibold",
            path_effects=[withStroke(linewidth=2, foreground="#121212")],
        )


def create_pie_chart(ax, values, labels, colors, accent_color: str):
    _, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct=lambda p: f"{p:.1f}%",
        startangle=180,
        colors=colors,
        wedgeprops={"edgecolor": "#404040", "linewidth": 1, "linestyle": "-"},
        textprops={"fontsize": 9, "color": "#E0E0E0"},
        pctdistance=0.8,
    )
    ax.set_title("Asset Distribution", fontsize=14, pad=15, weight="semibold")
    ax.axis("equal")
    text_outline = [withStroke(linewidth=2, foreground="#121212")]
    for text, autotext in zip(texts, autotexts):
        text.set_path_effects(text_outline)
        autotext.set_path_effects(text_outline)
        autotext.set_color(accent_color)
        autotext.set_weight("bold")


def save_figure(fig, path: str, logger):
    try:
        fig.savefig(
            path,
            facecolor=fig.get_facecolor(),
            bbox_inches="tight",
            dpi=120,
            transparent=False,
        )
        logger.info(f"Chart saved to {path}")
    except Exception as e:
        logger.exception(f"Failed to save chart: {e}")


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

    configure_dark_theme()
    fig, (ax_bar, ax_pie) = plt.subplots(ncols=2, figsize=(16, 8), facecolor="#121212")
    colors = generate_colors(len(labels))
    accent_color = "#FFFFFF"
    create_bar_chart(ax_bar, labels, values, colors, accent_color)
    create_pie_chart(ax_pie, values, labels, colors, accent_color)
    save_figure(fig, PIE_CHART_PATH, logger)
    plt.close(fig)


if __name__ == "__main__":
    main()
