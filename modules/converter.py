import os
from docx2pdf import convert as docx_to_pdf_convert
import comtypes.client

def word_to_pdf(input_path, output_path=None, delete_original=False):
    """Convert Word (.docx) to PDF"""
    if not os.path.exists(input_path):
        return f"Error: File {input_path} not found."
    
    try:
        docx_to_pdf_convert(input_path, output_path)
        if delete_original:
            os.remove(input_path)
        return f"Success: Converted to {output_path or input_path.replace('.docx', '.pdf')}"
    except Exception as e:
        return f"Error: {str(e)}"

def ppt_to_pdf(input_path, output_path=None, delete_original=False):
    """Convert PowerPoint (.pptx) to PDF"""
    if not os.path.exists(input_path):
        return f"Error: File {input_path} not found."
    
    input_path = os.path.abspath(input_path)
    if not output_path:
        output_path = os.path.splitext(input_path)[0] + ".pdf"
    else:
        output_path = os.path.abspath(output_path)

    powerpoint = None
    try:
        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        presentation = powerpoint.Presentations.Open(input_path, WithWindow=False)
        presentation.SaveAs(output_path, 32)
        presentation.Close()
        
        if delete_original:
            os.remove(input_path)
            
        return f"Success: Converted to {output_path}"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        if powerpoint:
            powerpoint.Quit()

def batch_convert(directory, exclude_pattern=None, delete_original=False):
    """Convert all .docx and .pptx in a directory to PDF"""
    if not os.path.isdir(directory):
        return f"Error: {directory} is not a valid directory."

    results = []
    exclude_list = exclude_pattern.split('|') if exclude_pattern else []
    
    for filename in os.listdir(directory):
        if filename in exclude_list:
            continue
            
        file_path = os.path.join(directory, filename)
        if filename.endswith('.docx'):
            results.append(word_to_pdf(file_path, delete_original=delete_original))
        elif filename.endswith('.pptx'):
            results.append(ppt_to_pdf(file_path, delete_original=delete_original))
            
    return results
