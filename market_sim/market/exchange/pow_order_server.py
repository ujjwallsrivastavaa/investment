import asyncio
import json
from market_sim.pow.proof_of_work import ProofOfWork
from market_sim.market.exchange.matching_engine import MatchingEngine

class PoWOrderServer:
    def __init__(self, symbol, host='127.0.0.1', port=8888, difficulty_bits=18):
        self.engine = MatchingEngine(symbol)
        self.host = host
        self.port = port
        self.pow = ProofOfWork(difficulty_bits)

    async def handle_client(self, reader, writer):
        data = await reader.read(4096)
        order = json.loads(data.decode())
        # Compose data string as in agent
        if 'price' in order:
            pow_data = f"{order['symbol']}|{order['side']}|{order['quantity']}|{order['price']}|{order['created_at']}|{order['agent_id']}"
        else:
            pow_data = f"{order['symbol']}|{order['side']}|{order['quantity']}|{order['created_at']}|{order['agent_id']}"
        if self.pow.validate(pow_data, order['pow_nonce']):
            # Here you could call self.engine.process_order(order) if you want to process it
            response = {"status": "accepted"}
        else:
            response = {"status": "rejected"}
        writer.write(json.dumps(response).encode())
        await writer.drain()
        writer.close()

    async def run(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"PoWOrderServer running on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    import asyncio

    symbol = "AAPL"  # Or get from sys.argv or config
    server = PoWOrderServer(symbol)
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("Server stopped.")