# 🚀 Crypto Event Tracker & Notifier

An intelligent MCP (Model Context Protocol) server that tracks cryptocurrency events worldwide using AI-powered search and event extraction.

## 📋 Overview

The Crypto Event Tracker uses Brave Search API to find cryptocurrency events, conferences, launches, upgrades, and announcements. It automatically extracts event details including dates, locations, and categorizes them for easy tracking.

## ✨ Features

- 🔍 *Global Crypto Search* - Track events for ANY cryptocurrency mentioned online
- 📅 *Smart Date Extraction* - Parses multiple date formats (12/31/2024, January 15 2025, etc.)
- 🎯 *Event Categorization* - Automatically classifies events (conference, launch, upgrade, airdrop, etc.)
- 🌍 *Worldwide Coverage* - No geographic restrictions, finds events globally
- 🤖 *AI-Powered Agent* - Uses GPT-4 to intelligently search and format results
- ⚡ *Real-time Updates* - Searches recent articles (past week by default)
- 🔮 *Upcoming Events Only* - Filters out past events, shows only future dates

## 🏗️ Architecture

crypto-event-tracker/
├── .env                     
├── requirements.txt         
├── config.json             
├── server.py               
├── client.py               
└── tools/
    ├── __init__.py         
    └── search.py          


## 🛠️ Installation

### Prerequisites
- Python 3.9+
- Brave Search API key ([Get one here](https://brave.com/search/api/))
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. *Clone the repository*
bash
git clone https://github.com/yourusername/crypto-event-tracker.git
cd crypto-event-tracker


2. *Install dependencies*
bash
pip install -r requirements.txt


3. *Create .env file*
bash
touch .env


Add your API keys:
env
BRAVE_API_KEY=your_brave_api_key_here
OPENAI_API_KEY=your_openai_api_key_here


4. *Run the agent*
bash
python client.py


## 🎮 Usage

### Interactive Chat Mode
bash
python client.py


*Example queries:*

You: What Bitcoin events are coming up?
You: Search for Ethereum conferences
You: Any Solana airdrops happening?
You: Show me all crypto events this month
You: What's happening with Cardano?


### Available Tools

1. *search_crypto_events* - Search for any cryptocurrency events
python
   query: "Bitcoin conference 2025"
   count: 10  # optional


2. *search_specific_coin* - Search events for a specific coin
python
   coin_name: "Ethereum"
   count: 10  # optional


## 📊 Response Format
json
{
  "query": "Bitcoin events",
  "total_results": 10,
  "events_with_dates": [
    {
      "coin": "BITCOIN",
      "title": "Bitcoin Conference 2025",
      "date": "2025-05-15T00:00:00",
      "location": "Miami",
      "description": "Annual Bitcoin conference...",
      "category": "conference",
      "source": "https://..."
    }
  ],
  "events_without_dates": [
    {
      "coin": "BITCOIN",
      "title": "Taproot upgrade discussion",
      "description": "Community discussing...",
      "category": "announcement",
      "source": "https://..."
    }
  ]
}


## 📅 Supported Date Formats

The system automatically extracts dates in these formats:
- 12/31/2024 or 12-31-2024 (MM/DD/YYYY)
- 2024-12-31 (ISO format)
- January 15, 2025 (Month Day, Year)
- 15 January 2025 (Day Month Year)
- January 15 (Month Day - assumes current or next year)

## 🎯 Supported Event Categories

- 🎤 *Conference* - Crypto conferences, conventions, meetups
- 🚀 *Launch* - Token launches, mainnet releases
- ⬆️ *Upgrade* - Protocol upgrades, hard forks
- 🎁 *Airdrop* - Token airdrops, distributions
- 🏛️ *Summit* - Industry summits, gatherings
- 📢 *Announcement* - Major announcements, reveals
- 📌 *Other* - General crypto events

## 🪙 Supported Cryptocurrencies

The system tracks *40+ popular cryptocurrencies* including:

Bitcoin (BTC), Ethereum (ETH), Solana (SOL), Cardano (ADA), Ripple (XRP), Polkadot (DOT), Dogecoin (DOGE), Shiba Inu, Avalanche (AVAX), Polygon (MATIC), Chainlink (LINK), Litecoin (LTC), Uniswap (UNI), Cosmos (ATOM), Tron (TRX), Stellar (XLM), Monero (XMR), Algorand (ALGO), Fantom (FTM), NEAR Protocol, Aptos (APT), Sui, Optimism, Arbitrum, Base, Binance Coin (BNB), Tether (USDT), USDC, and many more!

## 🔧 Configuration

All settings can be customized in config.json:
- Search result limits
- Search freshness (past day, week, month, year)
- Date extraction patterns
- Event categories
- Supported cryptocurrencies

## 🔮 Future Features

- [ ] *Google Calendar Integration* - Auto-add events to your calendar
- [ ] *Gmail Notifications* - Email alerts for new events
- [ ] *Scheduled Monitoring* - Daily/weekly automated searches
- [ ] *Custom Alerts* - Set alerts for specific coins or event types
- [ ] *Web Dashboard* - Visual interface for event tracking
- [ ] *Multi-language Support* - Track events in different languages

## 🐛 Troubleshooting

### Common Issues

*API Key Errors:*

Make sure your .env file has valid API keys:
BRAVE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here


*Import Errors:*
bash
pip install -r requirements.txt


*Date Not Detected:*
The system looks for specific date patterns. Make sure event descriptions contain dates in supported formats.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Brave Search API](https://brave.com/search/api/) - Web search functionality
- [OpenAI GPT-4](https://openai.com/) - AI agent intelligence
- [Model Context Protocol](https://github.com/Pavilion-devs/pydantic-AI-MCP) - 

## 📧 Contact

Name: Mobolaji Opeyemi Bolatito

Email:opeblow2021@gmail.com

Project Link: (https://github.com/opeblow/crypto-event-tracker.git)

## ⚠️ Disclaimer

This tool is for informational purposes only. Always verify event details from official sources. Not financial advice.

---

*Made with ❤️ for the crypto community*