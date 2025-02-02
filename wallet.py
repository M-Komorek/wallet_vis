import logging
import xmlschema
import sys
import yfinance

from typing import List, Dict


STOCK_FILE_PATCH = "stocks.xml"
SCHEMA_FILE_PATCH = "static/stocks.xsd"


class FinancialAsset:
    def __init__(self, ticker: str, amount: int, long_name: str, stock_price: int) -> None:
        self.ticker = ticker
        self.amount = amount
        self.long_name = long_name
        self.stock_price = stock_price
        self.value = amount*stock_price


class Wallet:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.info("Wallet init begins")
        self.financial_assets = self._load_financial_assets()
        self.logger.info("Wallet init succed")


    def _load_financial_assets(self):
        financial_assets: List[FinancialAsset] = []

        stocks = self._read_stocks_xml()
        for stock in stocks:
            try:
                y_asset_info = yfinance.Ticker(stock["Ticker"]).info
                financial_assets.append(FinancialAsset(stock["Ticker"], stock["Amount"], y_asset_info["longName"], y_asset_info["ask"]))
            except Exception:
                self.logger.error(f"Failed to download data for {stock['Ticker']}")
                sys.exit(1)

        return financial_assets
                

    def _read_stocks_xml(self) -> List[Dict[str, int]]:
        schema = xmlschema.XMLSchema('static/stocks.xsd')

        if schema.is_valid('stocks.xml'):
            self.logger.info("XML validated successfully")
            stocks_xml_as_dict = schema.to_dict('stocks.xml')
            return stocks_xml_as_dict["Stock"]
        else:
            self.logger.error("XML does not validate")
            sys.exit(1)


