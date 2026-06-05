import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

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

def parse_qr_code(image_path):
    """
    Reads a QR code image file and returns the decoded string data.
    """
    try:
        # Open the image file using Pillow
        img = Image.open(image_path)
        
        # Decode the QR code from the image
        decoded_objects = decode(img)
        
        if not decoded_objects:
            return {"success": False, "message": "No QR code detected in the image."}
        
        # Extract the raw data payload from the first detected QR code
        qr_data = decoded_objects[0].data.decode('utf-8')
        return {"success": True, "data": qr_data}

    except FileNotFoundError:
        return {"success": False, "message": f"Error: The file '{image_path}' could not be found."}
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}

