from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import requests
from datetime import datetime

app = FastAPI(title="Bitcoin 30-Day Price Chart")


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Bitcoin Price Tracker</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Inter, Arial, sans-serif;
            background:
                radial-gradient(circle at top left, #1f2937, #0f172a 60%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
        }

        .card {
            width: 100%;
            max-width: 1100px;
            background: rgba(255,255,255,0.06);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 28px;
            box-shadow:
                0 10px 30px rgba(0,0,0,0.4);
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 20px;
        }

        .title {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .btc-icon {
            width: 54px;
            height: 54px;
            border-radius: 50%;
            background: linear-gradient(135deg, #f7931a, #ffb347);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
            color: white;
            box-shadow: 0 4px 14px rgba(247,147,26,0.5);
        }

        h1 {
            margin: 0;
            font-size: 2rem;
        }

        .subtitle {
            opacity: 0.75;
            margin-top: 4px;
        }

        .stats {
            text-align: right;
        }

        .price {
            font-size: 2rem;
            font-weight: 700;
            color: #4ade80;
        }

        .updated {
            opacity: 0.7;
            margin-top: 4px;
            font-size: 0.95rem;
        }

        .chart-container {
            background: rgba(255,255,255,0.04);
            border-radius: 18px;
            padding: 20px;
        }

        canvas {
            width: 100% !important;
            height: 500px !important;
        }

        .footer {
            margin-top: 18px;
            opacity: 0.65;
            font-size: 0.9rem;
            text-align: center;
        }

        @media (max-width: 700px) {
            .header {
                flex-direction: column;
                align-items: flex-start;
            }

            .stats {
                text-align: left;
            }

            h1 {
                font-size: 1.6rem;
            }

            .price {
                font-size: 1.6rem;
            }

            canvas {
                height: 350px !important;
            }
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <div class="title">
                <div class="btc-icon">₿</div>
                <div>
                    <h1>Bitcoin Price Tracker</h1>
                    <div class="subtitle">Last 30 days • USD Market Price</div>
                </div>
            </div>

            <div class="stats">
                <div class="price" id="currentPrice">$--</div>
                <div class="updated" id="updatedTime">Loading...</div>
            </div>
        </div>

        <div class="chart-container">
            <canvas id="btcChart"></canvas>
        </div>

        <div class="footer">
            Data source: CoinGecko API
        </div>
    </div>

    <script>
        async function loadChart() {
            const response = await fetch('/api/bitcoin');
            const data = await response.json();

            const labels = data.prices.map(p => p.date);
            const prices = data.prices.map(p => p.price);

            const current = prices[prices.length - 1];

            document.getElementById('currentPrice').innerText =
                '$' + current.toLocaleString();

            document.getElementById('updatedTime').innerText =
                'Updated: ' + new Date().toLocaleString();

            const ctx = document.getElementById('btcChart').getContext('2d');

            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, 'rgba(247,147,26,0.45)');
            gradient.addColorStop(1, 'rgba(247,147,26,0.02)');

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'BTC Price (USD)',
                        data: prices,
                        borderColor: '#f7931a',
                        backgroundColor: gradient,
                        borderWidth: 3,
                        fill: true,
                        pointRadius: 0,
                        tension: 0.35
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {
                        mode: 'index',
                        intersect: false
                    },
                    plugins: {
                        legend: {
                            labels: {
                                color: 'white'
                            }
                        },
                        tooltip: {
                            backgroundColor: '#111827',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: '#f7931a',
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return '$' +
                                        context.parsed.y.toLocaleString();
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: 'rgba(255,255,255,0.7)'
                            },
                            grid: {
                                color: 'rgba(255,255,255,0.05)'
                            }
                        },
                        y: {
                            ticks: {
                                color: 'rgba(255,255,255,0.7)',
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            },
                            grid: {
                                color: 'rgba(255,255,255,0.05)'
                            }
                        }
                    }
                }
            });
        }

        loadChart();
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return HTML


@app.get("/api/bitcoin")
def bitcoin_data():
    url = (
        "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        "?vs_currency=usd&days=30"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    prices = []

    for timestamp, price in data["prices"]:
        dt = datetime.fromtimestamp(timestamp / 1000)
        prices.append({
            "date": dt.strftime("%b %d"),
            "price": round(price, 2)
        })

    return JSONResponse({"prices": prices})