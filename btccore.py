from bitcoinrpc import BitcoinRPC
import config

async def handle_rpc_call(func, *args):
    try:
        async with BitcoinRPC.from_config(config.BITCOIN_RPC_AUTH['url'], (config.BITCOIN_RPC_AUTH['user'], config.BITCOIN_RPC_AUTH['password'])) as rpc:
            return await rpc.acall(func, args)
        
    except Exception as e:
        return {'error': str(e)}