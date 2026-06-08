import httpx

EXCHANGE_RATE_API = "https://open.er-api.com/v6/latest/USD"
response = httpx.get(
    EXCHANGE_RATE_API,
    timeout=5.0
)
# print(response)
data = response.json()
# print(data)
live_rate = data["rates"]["NGN"]
print(live_rate * 1.10)