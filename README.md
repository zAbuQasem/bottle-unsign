# bottle-unsign

bottle-unsign is a Python tool for encoding, decoding, and performing dictionary attacks on cookies using HMAC-based encryption.

## Features

- **Encode**: Encode a cookie using HMAC-based encryption with a specified key.
- **Decode**: Decode a cookie that was encoded using the same key.
- **Dictionary Attack**: Attempt to decode a cookie by testing multiple potential keys from a wordlist file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/bottle-unsign.git
   cd bottle-unsign
   ```

2. **Install dependencies:**

   ```bash
   pip install .
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

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.


## Acknowledgments

- This tool utilizes the `rich` library for colorful and interactive terminal output.
