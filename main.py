import click
from modules import crypto, media, runner, utils
from tabulate import tabulate
from datetime import datetime
from PIL import Image
from pyzbar.pyzbar import decode

@click.group()
def cli():
    """Ultimate Dev Toolbox"""
    pass

@cli.command()
@click.option('-n', '--number', default=1, type=int, help="Number of UUIDs to generate (max 200)")
def uuid(number):
    """Generates random UUID v4 strings"""
    if number > 200:
        click.secho("Error: Max limit is 200 UUIDs to prevent terminal crash.", fg='red')
        return
        
    results = crypto.get_uuids(number)
    for u in results:
        click.echo(u)

@cli.command()
@click.argument('token')
def jwt_parse(token):
    click.echo(crypto.decode_jwt(token))

@cli.command()
@click.argument('data')
@click.argument('name')
def qr(data, name):
    path = media.generate_qr(data, name)
    click.echo(f"QR saved to {path}")

@cli.command()
@click.argument('files', nargs=-1)
def run_all(files):
    runner.run_concurrently(files)

@cli.command()
@click.argument('ts', type=float)
def time(ts):
    click.echo(utils.format_timestamp(ts))
    
@cli.command()
@click.argument('data')
def qr_show(data):
    """Displays QR code directly in the terminal"""
    media.show_qr_in_terminal(data)

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
def qr_parse(image_path):
    """Parses/Scans a QR code image file and extracts its data"""
    click.echo(f"Scanning {image_path}...")
    
    # Call the logic from your media module
    result = media.parse_qr_code(image_path)
    
    if result["success"]:
        click.secho("\n🎉 Success! Decoded Content:", fg='green', bold=True)
        # Highlight it so it stands out in the terminal
        click.secho(result["data"], fg='cyan', underline=True)
    else:
        click.secho(result["message"], fg='red')

@cli.command()
def menu():
    """Custom help menu with a clean table"""
    table_data = [
        ["tool uuid", "Generates a unique UUID v4 string.", "tool uuid"],
        ["tool qr-show", "Displays a QR code in the terminal.", "tool qr-show \"https://google.com\""],
        ["tool qr", "Generates a QR code and saves a file.", "tool qr \"data\" \"my_code.png\""],
        ["tool qr-parse", "Scans an image file and extracts data.", "tool qr-parse \"my_code.png\""], # New Row
        ["tool jwt-parse", "Decodes a JWT token string.", "tool jwt-parse <your_token>"],
        ["tool time", "Parse TS / Gen Now (-g) / Convert Date (-c)", "tool time -g"],
        ["tool run-all", "Runs multiple Python files concurrently.", "tool run-all script1.py script2.py"],
        ["tool menu", "Shows this help table.", "tool menu"]
    ]
    
    headers = ["Command", "Description", "Example Usage"]
    
    # 'grid' or 'fancy_grid' looks best in modern terminals
    click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))

@cli.command()
@click.option('-g', '--generate', is_flag=True, help="Generate current timestamp")
@click.option('-c', '--convert', type=str, help="Convert date string to timestamp")
@click.argument('ts', type=float, required=False)
def time(generate, convert, ts):
    """Manage timestamps and dates"""
    if generate:
        now_obj = datetime.now()
        timestamp = int(now_obj.timestamp())
        # This will show both!
        click.echo(f"Current Timestamp: {timestamp}")
        click.echo(f"Current Time:      {now_obj.strftime('%Y-%m-%d %H:%M:%S')}")
    
    elif convert:
        result = utils.string_to_timestamp(convert)
        click.echo(f"Timestamp: {result}")
    
    elif ts:
        click.echo(f"Date: {utils.format_timestamp(ts)}")
    
    else:
        click.echo("Error: Use -g to generate, -c to convert, or provide a timestamp.")

if __name__ == '__main__':
    cli()