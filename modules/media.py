import qrcode

def generate_qr(data, filename):
    img = qrcode.make(data)
    img.save(filename)
    return filename

def show_qr_in_terminal(data):
    # Use the QRCode class to control the output
    qr = qrcode.QRCode()
    qr.add_data(data)
    
    # 'tty' or 'ascii' output creates a string that works in terminal
    # This prints white and black blocks directly
    qr.print_ascii(invert=True)

