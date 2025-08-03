document.addEventListener('DOMContentLoaded', function() {
    const cryptoTableBody = document.getElementById('crypto-table-body');

    async function fetchMarketData() {
        try {
            const response = await fetch('/api/market-data');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            // Clear loading message
            cryptoTableBody.innerHTML = ''; 

            // Handle both real API data and fallback data
            let processedData = data;
            
            // If this is Binance API data, filter for USDT pairs
            if (data.length > 0 && data[0].symbol && !data[0].symbol.endsWith('USDT')) {
                // This might be a different format, handle accordingly
                processedData = data.filter(coin => coin.symbol && coin.symbol.endsWith('USDT'));
            }
            
            // Sort by quote volume (or use a default sort)
            processedData.sort((a, b) => {
                const volumeA = parseFloat(a.quoteVolume || a.volume || 0);
                const volumeB = parseFloat(b.quoteVolume || b.volume || 0);
                return volumeB - volumeA;
            });

            // Take top 100
            const sortedData = processedData.slice(0, 100);

            if (sortedData.length === 0) {
                cryptoTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-warning">No market data available at the moment.</td></tr>';
                return;
            }

            sortedData.forEach((coin, index) => {
                try {
                    const price = parseFloat(coin.lastPrice || 0).toFixed(2);
                    const change = parseFloat(coin.priceChangePercent || 0);
                    const volume = parseFloat(coin.volume || 0).toLocaleString();
                    const marketCap = (parseFloat(coin.lastPrice || 0) * parseFloat(coin.weightedAvgPrice || coin.lastPrice || 0)).toLocaleString(undefined, { maximumFractionDigits: 0 });

                    const row = document.createElement('tr');
                    const symbolName = coin.symbol.replace('USDT', '');
                    row.dataset.symbol = symbolName;
                    
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${symbolName}</td>
                        <td>$${price}</td>
                        <td class="${change >= 0 ? 'text-success' : 'text-danger'}">${change.toFixed(2)}%</td>
                        <td>$${volume}</td>
                        <td>$${marketCap}</td>
                    `;
                    cryptoTableBody.appendChild(row);
                } catch (coinError) {
                    console.warn('Error processing coin data:', coin, coinError);
                }
            });
            
            // Add click listeners to rows
            document.querySelectorAll('#crypto-table tbody tr').forEach(row => {
                row.addEventListener('click', () => {
                    window.location.href = `/coin/${row.dataset.symbol}`;
                });
            });

            console.log(`✅ Market data loaded successfully: ${sortedData.length} coins`);

        } catch (error) {
            console.error("Could not fetch market data:", error);
            cryptoTableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Failed to load market data. Please try again later.</td></tr>';
        }
    }

    fetchMarketData();
    // Refresh data every 30 seconds
    setInterval(fetchMarketData, 30000);
});
