# Mass Server Leave & Friend Remover


Script made for leaving all of your Discord servers and removing all friends.

## Features

- Leave all Discord servers automatically
- Remove all friends from your friend list
- Whitelist support for servers and friends you want to keep
- Rate limiting protection with automatic retries
- Error handling and detailed logging

## Installation

The script will automatically install required modules (aiohttp, requests) when you run it.

Alternatively, you can install them manually:
```bash
pip install aiohttp requests
```

## Usage

1. Replace the token on line 25 with your Discord token
2. **Optional:** Add server IDs to the `whitelist` on line 26 for servers you want to keep
3. **Optional:** Add user IDs to the `friends_whitelist` on line 27 for friends you want to keep
4. Run the script: `python main.py`

The script will:
1. First leave all servers (except whitelisted ones)
2. Then remove all friends (except whitelisted ones)

## Configuration

### Server Whitelist
To keep certain servers, add their guild IDs to the whitelist:
```python
whitelist = ["123456789012345678", "987654321098765432"]
```

### Friends Whitelist
To keep certain friends, add their user IDs to the friends whitelist:
```python
friends_whitelist = ["123456789012345678", "987654321098765432"]
```

## Important Notes

- **Use at your own risk**
- Make sure your token is valid
- The script includes rate limiting protection
- Actions are irreversible - make sure to configure whitelists properly
- Keep your token private and never share it
