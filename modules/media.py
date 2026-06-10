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

import os
from PIL import Image, UnidentifiedImageError
from pyzbar.pyzbar import decode

def parse_qr_code(image_path):
    """
    Validates an image file and attempts to extract QR code data.
    Returns a dictionary with success status and a clear data/error message.
    """
    # 1. Check if the file physically exists
    if not os.path.exists(image_path):
        return {
            "success": False, 
            "message": f"❌ File Error: The path '{image_path}' does not exist."
        }
    
    try:
        # 2. Try to open the file as an image
        with Image.open(image_path) as img:
            # Force Pillow to load the data to ensure it's a valid, uncorrupted image
            img.verify() 
        
        # Re-open after verify() because verify() closes/invalidates the file handler
        with Image.open(image_path) as img:
            # 3. Scan the validated image for QR codes
            decoded_objects = decode(img)
            
            # If the image is valid but pyzbar found 0 QR codes inside it
            if not decoded_objects:
                return {
                    "success": False, 
                    "message": "🔍 Scan Notice: That is a valid image, but no QR code could be found inside it."
                }
            
            # 4. Success! Extract the raw data payload from the first detected QR code
            qr_data = decoded_objects[0].data.decode('utf-8')
            return {
                "success": True, 
                "data": qr_data
            }

    except UnidentifiedImageError:
        # Triggers if the file exists, but it's a .txt, .pdf, or completely corrupted image
        return {
            "success": False, 
            "message": "❌ Format Error: The file is not a valid image format (PNG, JPG, etc.)."
        }
        
    except Exception as e:
        # Catch-all for rare system errors (like zbar library binary missing)
        return {
            "success": False, 
            "message": f"💥 System Error: Internal scanner malfunction.\nDetails: {str(e)}"
        }

