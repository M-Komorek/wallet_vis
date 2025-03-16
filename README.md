# wallet_vis
WalletVis is a Python-based tool for visualizing wallet or portfolio data. It integrates data retrieval from financial sources (via [yfinance](https://pypi.org/project/yfinance/)), and plotting using [matplotlib](https://pypi.org/project/matplotlib/).

![Sample portfolio](https://github.com/M-Komorek/wallet_vis/blob/main/output/portfolio_distribution.png)

## 🚀 Features
- Data Fetching: Retrieves live and historical market data using yfinance.
- Visualization: Generates clear and informative visualizations with matplotlib.
- Lightweight Storage: Simple XML file.

## 🛠️ Usage
- Python 3.11 or later is recommended.
``` bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
chmod +x run.sh
```
Once configured, add your stocks to `data/stocks.xml` and run the tool from the command line:
./run.sh

``` bash
```
