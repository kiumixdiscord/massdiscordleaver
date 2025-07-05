import sys
import subprocess
required_modules = ['aiohttp', 'requests']
missing_modules = []

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        missing_modules.append(module)

if missing_modules:
    print(f"Missing modules: {', '.join(missing_modules)}")
    print("Installing missing modules...")
    for module in missing_modules:
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])
    print("Modules installed successfully!")

import aiohttp
import asyncio
import tracemalloc
import requests

tracemalloc.start()
token = "Token_Here"
whitelist = []
friends_whitelist = []

async def mass_leave():
    headers = {'Authorization': token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://discordapp.com/api/v6/users/@me/guilds', headers=headers) as resp:
                if resp.status != 200:
                    print(f"Failed to get guilds: {resp.status}")
                    return
                guilds = await resp.json()
                
                for guild in guilds:
                    if guild["id"] in whitelist:
                        print(f'Skipped {guild["name"]} (whitelisted)')
                        continue
                    max_retries = 3
                    retry_delay = 2
                    
                    for attempt in range(max_retries):
                        try:
                            async with session.delete(f'https://discordapp.com/api/v6/users/@me/guilds/{guild["id"]}', headers=headers) as delete_resp:
                                if delete_resp.status == 204:
                                    print(f'Left {guild["name"]}')
                                    break
                                elif delete_resp.status == 429:
                                    if attempt < max_retries - 1:
                                        wait_time = retry_delay * (2 ** attempt)
                                        print(f'Rate limited for {guild["name"]}, waiting {wait_time}s before retry...')
                                        await asyncio.sleep(wait_time)
                                        continue
                                    else:
                                        print(f'Failed to leave {guild["name"]}: Rate limited (max retries reached)')
                                else:
                                    print(f'Failed to leave {guild["name"]}: Status {delete_resp.status}')
                                    break
                        except Exception as e:
                            print(f'Failed to leave {guild["name"]}: {str(e)}')
                            break
                    await asyncio.sleep(1)
                    
        except Exception as e:
            print(f'Error: {str(e)}')

async def remove_friends():
    headers = {'Authorization': token}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://discordapp.com/api/v6/users/@me/relationships', headers=headers) as resp:
                if resp.status != 200:
                    print(f"Failed to get friends: {resp.status}")
                    return
                relationships = await resp.json()
                friends = [rel for rel in relationships if rel.get("type") == 1]
                
                for friend in friends:
                    if friend["id"] in friends_whitelist:
                        print(f'Skipped {friend["user"]["username"]} (whitelisted)')
                        continue
                    max_retries = 3
                    retry_delay = 2
                    
                    for attempt in range(max_retries):
                        try:
                            async with session.delete(f'https://discordapp.com/api/v6/users/@me/relationships/{friend["id"]}', headers=headers) as delete_resp:
                                if delete_resp.status == 204:
                                    print(f'Removed friend {friend["user"]["username"]}')
                                    break
                                elif delete_resp.status == 429:
                                    if attempt < max_retries - 1:
                                        wait_time = retry_delay * (2 ** attempt)
                                        print(f'Rate limited for {friend["user"]["username"]}, waiting {wait_time}s before retry...')
                                        await asyncio.sleep(wait_time)
                                        continue
                                    else:
                                        print(f'Failed to remove {friend["user"]["username"]}: Rate limited (max retries reached)')
                                else:
                                    print(f'Failed to remove {friend["user"]["username"]}: Status {delete_resp.status}')
                                    break
                        except Exception as e:
                            print(f'Failed to remove {friend["user"]["username"]}: {str(e)}')
                            break
                    await asyncio.sleep(1)
                    
        except Exception as e:
            print(f'Error removing friends: {str(e)}')

async def main():
    print("Starting mass leave servers...")
    await mass_leave()
    print("\nStarting friend removal...")
    await remove_friends()
    print("Done!")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
