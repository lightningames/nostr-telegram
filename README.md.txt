## bitcoin p2p orderbook

A simple telegram bot with sat to fiat conversions and ticker features. 
Add to any chatroom and let people post their p2p bid/asks which will be broadcast every 12 hrs. 

Features: 
- admin controls (done)
- coingecko cron job for price updates (done)
- sats to fiat converter (done)
- Allow users on group to use bot privately.  (done)

Potential Features to add: 
-  Expiring orders after a certain age (e.g. 90 days)

Datasources: 
- Coingecko API Data for rates and fiat conversions

Commands: 
-   /all    - List Open Offers. 
-   /add    - Add an Offer, Ex: /add Buy 0.05 btc, %Coinbase ATM/Cash.
-   /del    - Delete an offer. Ex: /del [offer_number]
-   /rates  - Get latest BTC to Fiat Rates from Coingecko
-   /table  - Sats to BTC conversion table
-   /btc   - ex. /btc 0.1337 HKD, converts 0.1337 btc to fiat
-   /sats   - ex. /sats 20000 HKD, converts 20k sats to fiat
-   /fiat   - ex. /fiat 1000 HKD, converts 1k fiat to sats
-   /gettx - <txid> get L1 transaction status
-   /fees  -  <size>  Fee suggestions.
-   /get_block_height   - get bitcoin block height
-   /get_mempool_stats  - L1 mempool stats


Create and Edit your config.yml with credentials. 

# Docker
  
 TODO: Dockerfile does the following: 
  
  - setup environment
  - sets up mongodb
  - installs requirements
  - initializes db with python dbtools script
  - runs telegram bot
  
