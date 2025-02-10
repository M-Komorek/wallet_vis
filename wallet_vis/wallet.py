import logging
import xmlschema
from typing import Any, Dict, List
import yfinance

from wallet_vis.constants import SCHEMA_FILE_PATH, STOCK_FILE_PATH


class FinancialAsset:
    def __init__(
        self, ticker: str, amount: int, long_name: str, stock_price: float
    ) -> None:
        self.ticker = ticker
        self.amount = amount
        self.long_name = long_name
        self.stock_price = stock_price
        self.value = amount * stock_price


class Wallet:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Wallet...")
        self.financial_assets = self._load_financial_assets()
        self.logger.info("Wallet initialization succeeded")

    def _load_financial_assets(self) -> List[FinancialAsset]:
        financial_assets: List[FinancialAsset] = []

        stocks = self._read_stocks_xml()
        for stock in stocks:
            ticker = stock.get("Ticker")
            amount = stock.get("Amount")

            if ticker is None or amount is None:
                self.logger.error("Ticker or Amount missing in stock data")
                raise

            try:
                ticker_obj = yfinance.Ticker(ticker)
                y_asset_info = ticker_obj.info

                long_name = y_asset_info.get("longName", ticker)
                ask_price = y_asset_info.get("ask")
                if ask_price is None:
                    self.logger.error(f"Ask price not available for ticker {ticker}")
                    raise ValueError(f"Ask price not available for ticker {ticker}")

                financial_assets.append(
                    FinancialAsset(ticker, amount, long_name[:20], float(ask_price))
                )

            except Exception as e:
                self.logger.exception(f"Failed to download data for {ticker}: {e}")
                raise

        return financial_assets

    def _read_stocks_xml(self) -> List[Dict[str, Any]]:
        try:
            schema = xmlschema.XMLSchema(SCHEMA_FILE_PATH)
        except Exception as e:
            self.logger.exception(f"Failed to load XML schema: {e}")
            raise

        if not schema.is_valid(STOCK_FILE_PATH):
            self.logger.error("XML does not validate against the schema")
            raise ValueError("Invalid XML file")

        try:
            stocks_xml_as_dict = schema.to_dict(STOCK_FILE_PATH)
            stocks = stocks_xml_as_dict.get("Stock")

            if stocks is None:
                self.logger.error("No 'Stock' element found in the XML")
                raise ValueError("Missing Stock element")

            if isinstance(stocks, dict):
                stocks = [stocks]

            return stocks

        except Exception as e:
            self.logger.exception(f"Error parsing XML file: {e}")
            raise
