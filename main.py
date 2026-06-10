import click
import json
import sys
from modules import crypto, media, runner, utils, converter
from tabulate import tabulate
from datetime import datetime

# Custom logic for mutually exclusive options
class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop('mutually_exclusive', []))
        help_text = kwargs.get('help', '')
        if self.mutually_exclusive:
            excl_str = ', '.join(self.mutually_exclusive)
            kwargs['help'] = f"{help_text} (Mutually exclusive with: {excl_str})"
        super(MutuallyExclusiveOption, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.name in opts:
            for other_name in self.mutually_exclusive:
                if other_name in opts:
                    raise click.UsageError(
                        f"Illegal usage: '{self.name}' and '{other_name}' cannot be used together."
                    )
        return super(MutuallyExclusiveOption, self).handle_parse_result(ctx, opts, args)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Ultimate Dev Toolbox - Your Swiss Army Knife for Development.
    
    A collection of useful tools for common developer tasks.
    """
    pass

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-n', '--number', default=1, type=int, help="Number of UUIDs to generate (max 200)")
def uuid(number):
    """Generates random UUID v4 strings."""
    if number > 200:
        click.secho("Error: Max limit is 200 UUIDs.", fg='red')
        return
    results = crypto.get_uuids(number)
    for u in results:
        click.echo(f"UUID: {u}")

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('data', required=False)
@click.option('-s', '--show', is_flag=True, 
              cls=MutuallyExclusiveOption, mutually_exclusive=['parse_path'],
              help="Display QR code in terminal")
@click.option('-f', '--file', 'file_path', type=click.Path(), 
              cls=MutuallyExclusiveOption, mutually_exclusive=['parse_path'],
              help="Save QR code to file")
@click.option('-p', '--parse', 'parse_path', type=click.Path(exists=True), 
              cls=MutuallyExclusiveOption, mutually_exclusive=['show', 'file_path'],
              help="Parse QR code from image file")
def qr(data, show, file_path, parse_path):
    """
    Generate, Show, or Parse QR codes.
    
    Examples:
    tool qr "https://google.com" -s
    tool qr -p "my_screenshot.png"
    """
    try:
        if parse_path:
            click.echo(f"Scanning QR File: {parse_path}...")
            result = media.parse_qr_code(parse_path)
            if result["success"]:
                click.secho("\n🎉 Success! Decoded QR Content:", fg='green', bold=True)
                click.secho(f"QR Data: {result['data']}", fg='cyan', underline=True)
            else:
                click.secho(f"QR Error: {result['message']}", fg='red')
            return

        if not data:
            raise click.UsageError("Missing data for QR generation. Use -p to parse instead.")

        if show or (not show and not file_path):
            media.show_qr_in_terminal(data)
        
        if file_path:
            path = media.generate_qr(data, file_path)
            click.echo(f"QR File Saved: {path}")
            
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.option('-n', '--now', is_flag=True, 
              cls=MutuallyExclusiveOption, mutually_exclusive=['readable', 'timestamp'],
              help="Get current time and timestamp")
@click.option('-r', '--readable', type=float, 
              cls=MutuallyExclusiveOption, mutually_exclusive=['now', 'timestamp'],
              help="Convert timestamp to readable date")
@click.option('-t', '--timestamp', type=str, 
              cls=MutuallyExclusiveOption, mutually_exclusive=['now', 'readable'],
              help="Convert date string to timestamp")
@click.option('--ms', is_flag=True, help="Use milliseconds for input/output")
def time(now, readable, timestamp, ms):
    """Time Utilities (Timestamp <-> Readable)."""
    if now:
        n = datetime.now()
        ts = n.timestamp()
        ts_val = int(ts * 1000) if ms else int(ts)
        click.echo(f"Unix Timestamp: {ts_val}")
        
        fmt = '%Y-%m-%d %H:%M:%S'
        if ms:
            fmt += '.%f'
        time_str = n.strftime(fmt)
        if ms:
            time_str = time_str[:-3]
        click.echo(f"Current Time:   {time_str}")
    elif readable:
        click.echo(f"Converted Time: {utils.format_timestamp(readable, ms=ms)}")
    elif timestamp:
        click.echo(f"Unix Timestamp: {utils.string_to_timestamp(timestamp, ms=ms)}")
    else:
        click.echo("Use -n, -r, or -t. See --help for info.")

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('input', required=False)
@click.option('-v', '--verify', 'key', type=str, help="Verify JWT signature with a secret key")
@click.option('-C', '--create', is_flag=True, cls=MutuallyExclusiveOption, mutually_exclusive=['verify'], help="Create a new JWT token")
@click.option('-F', '--file', type=click.Path(exists=True), help="Read JWT payload from JSON file (for creation)")
@click.option('-a', '--alg', type=str, default='HS256', help="Algorithm for JWT creation (default: HS256)")
def jwt(input, key, create, file, alg):
    """
    JWT Parsing, Verification, and Creation.
    
    Use cases:
    - Decode JWT payload: tool jwt <token>
    - Verify JWT: tool jwt <token> -v <secret>
    - Create JWT: tool jwt -C -F payload.json -v <secret>
    """
    try:
        if create:
            # Handle token creation
            if not key:
                raise click.UsageError("Need -v/--verify (secret key) is required for creation!")
            
            if file:
                # Read from file
                with open(file, 'r') as f:
                    payload = json.load(f)
            elif input:
                # Read from input argument (if valid json string)
                try:
                    payload = json.loads(input)
                except json.JSONDecodeError:
                    raise click.UsageError("Input must be valid JSON string or use -F/--file to read from file!")
            else:
                raise click.UsageError("Need either JSON string or -F/--file to specify payload!")
            
            token = crypto.create_jwt(payload, key, alg)
            
            if token.startswith("Error:"):
                click.secho(token, fg='red')
            else:
                click.echo(f"JWT Token: {token}")
        else:
            # Handle decode/verify
            if not input:
                raise click.UsageError("Need JWT token is required for decode/verify!")
            
            payload = crypto.decode_jwt(input, key)
            if isinstance(payload, dict):
                enhanced_payload = utils.format_jwt_times(payload)
                click.echo(json.dumps(enhanced_payload, indent=4))
            else:
                click.secho(payload, fg='red')
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('url')
def url(url):
    """Parse URL into components."""
    details = utils.parse_url_details(url)
    if "error" in details:
        click.secho(f"URL Error: {details['error']}", fg='red')
    else:
        click.echo(f"URL Components:")
        click.echo(json.dumps(details, indent=4))

@cli.command(context_settings=CONTEXT_SETTINGS)
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), help="Output file path (ignored for directory)")
@click.option('-d', '--delete', is_flag=True, help="Delete original file after conversion")
@click.option('-e', '--exclude', type=str, help="Exclude specific files (e.g., 'file1.docx|file2.pptx')")
def convert(input_path, output, delete, exclude):
    """
    Convert Word (.docx) or PowerPoint (.pptx) to PDF.
    
    Can convert a single file or an entire directory.
    """
    try:
        import os
        if os.path.isdir(input_path):
            click.echo(f"Scanning directory for conversion: {input_path}")
            results = converter.batch_convert(input_path, exclude, delete)
            for res in results:
                if "Success" in res:
                    click.secho(f"Convert Success: {res}", fg='green')
                else:
                    click.secho(f"Convert Error: {res}", fg='red')
        else:
            if input_path.endswith('.docx'):
                click.echo(f"Converting Word document to PDF: {input_path}")
                result = converter.word_to_pdf(input_path, output, delete)
            elif input_path.endswith('.pptx'):
                click.echo(f"Converting PowerPoint presentation to PDF: {input_path}")
                result = converter.ppt_to_pdf(input_path, output, delete)
            else:
                raise click.UsageError("Unsupported file format. Use .docx or .pptx.")

            if "Success" in result:
                click.secho(f"Convert Success: {result}", fg='green')
            else:
                click.secho(f"Convert Error: {result}", fg='red')
            
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')

@cli.command()
def menu():
    """Show available tools in a clean table"""
    table_data = [
        ["qr", "QR codes (gen/parse)", "tool qr -s \"data\""],
        ["time", "Time utilities", "tool time -n"],
        ["jwt", "JWT parse/verify/create", "tool jwt -C -F payload.json -v secret"],
        ["url", "Parse URL components", "tool url \"https://...\""],
        ["convert", "Word/PPT to PDF", "tool convert doc.docx"],
        ["uuid", "Generate UUIDs", "tool uuid -n 5"],
        ["menu", "Show this menu", "tool menu"]
    ]
    headers = ["Command", "Description", "Example"]
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == '__main__':
    cli()