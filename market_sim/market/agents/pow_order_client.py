import asyncio
import json
import time
from market_sim.pow.proof_of_work import ProofOfWork

async def send_order(order, host='127.0.0.1', port=8888, difficulty_bits=18):
    pow = ProofOfWork(difficulty_bits)
    if 'price' in order:
        data = f"{order['symbol']}|{order['side']}|{order['quantity']}|{order['price']}|{order['created_at']}|{order['agent_id']}"
    else:
        data = f"{order['symbol']}|{order['side']}|{order['quantity']}|{order['created_at']}|{order['agent_id']}"
    nonce, hash_val, elapsed = pow.mine(data)
    order['pow_nonce'] = nonce
    order['pow_hash'] = hash_val
    order['pow_time'] = elapsed

    reader, writer = await asyncio.open_connection(host, port)
    writer.write(json.dumps(order).encode())
    await writer.drain()
    response = await reader.read(4096)
    print("Server response:", response.decode())
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    order = {
        "symbol": "AAPL",
        "side": "buy",
        "quantity": 10,
        "created_at": time.time(),
        "agent_id": "agent_1"
    }
    asyncio.run(send_order(order))