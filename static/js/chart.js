document.addEventListener('DOMContentLoaded', async function() {
    const chartContainer = document.getElementById('chart-container');
    
    // Create the chart
    const chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 500,
        layout: {
            backgroundColor: '#1c1c1c',
            textColor: 'rgba(255, 255, 255, 0.9)',
        },
        grid: {
            vertLines: { color: 'rgba(197, 203, 206, 0.2)' },
            horzLines: { color: 'rgba(197, 203, 206, 0.2)' },
        },
        crosshair: { mode: LightweightCharts.CrosshairMode.Normal },
        rightPriceScale: { borderColor: 'rgba(197, 203, 206, 0.8)' },
        timeScale: { borderColor: 'rgba(197, 203, 206, 0.8)' },
    });

    const candleSeries = chart.addCandlestickSeries({
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderDownColor: '#ef5350',
        borderUpColor: '#26a69a',
        wickDownColor: '#ef5350',
        wickUpColor: '#26a69a',
    });

    // Fetch data and apply it to the chart
    try {
        const response = await fetch(`/api/kline-data/${coinSymbol}`);
        if (!response.ok) {
            throw new Error('Failed to fetch chart data');
        }
        const data = await response.json();
        candleSeries.setData(data);
        chart.timeScale().fitContent();
    } catch (error) {
        console.error('Error fetching K-line data:', error);
        // Display an error message on the chart
    }

    // Resize chart with window
    window.addEventListener('resize', () => {
        chart.resize(chartContainer.clientWidth, 500);
    });
});
