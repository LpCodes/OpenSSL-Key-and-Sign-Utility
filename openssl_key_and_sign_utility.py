import os
import subprocess
import PySimpleGUI as sg


# Function to generate keys
def generate_keys(private_key_dir, public_key_dir):
    """
    Generate a pair of RSA private and public keys.

    Args:
        private_key_dir (str): Directory to save the private key.
        public_key_dir (str): Directory to save the public key.

    Returns:
        bool or str: True if successful, error message if failed.
    """
    try:
        private_key_file = os.path.join(private_key_dir, "private_key.pem")
        public_key_file = os.path.join(public_key_dir, "public_key.pem")
        subprocess.run(
            ["openssl", "genpkey", "-algorithm", "RSA", "-out", private_key_file],
            check=True,
        )
        subprocess.run(
            [
                "openssl",
                "pkey",
                "-in",
                private_key_file,
                "-pubout",
                "-out",
                public_key_file,
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        return str(e.stderr)  # Return error message


# Function to sign a file
def sign_file(file_to_sign, signature_file, private_key_file):
    """
    Sign a file using a private key.

    Args:
        file_to_sign (str): Path to the file to be signed.
        signature_file (str): Path to save the signature file.
        private_key_file (str): Path to the private key.

    Returns:
        bool or str: True if successful, error message if failed.
    """
    try:
        subprocess.run(
            [
                "openssl",
                "dgst",
                "-sha256",
                "-sign",
                private_key_file,
                "-out",
                signature_file,
                file_to_sign,
            ],
            check=True,
        )
        return True
    except subprocess.CalledProcessError as e:
        return str(e.stderr)  # Return error message


# Function to verify a signature
def verify_signature(public_key_file, signature_file_to_verify, file_to_verify):
    """
    Verify the signature of a file.

    Args:
        public_key_file (str): Path to the public key.
        signature_file_to_verify (str): Path to the signature file.
        file_to_verify (str): Path to the file to be verified.

    Returns:
        bool or str: True if the verification is successful, error message if failed.
    """
    try:
        result = subprocess.run(
            [
                "openssl",
                "dgst",
                "-sha256",
                "-verify",
                public_key_file,
                "-signature",
                signature_file_to_verify,
                file_to_verify,
            ],
            capture_output=True,
            check=True,
        )
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        return str(e.stderr)  # Return error message


# GUI layout
layout = [
    [
        sg.Frame('Key Generation', layout=[
            [sg.Text("Private Key Directory:"), sg.Input(key="-PRIVATE_KEY_DIR-"), sg.FolderBrowse()],
            [sg.Text("Public Key Directory:"), sg.Input(key="-PUBLIC_KEY_DIR-"), sg.FolderBrowse()],
            [sg.Button("Generate Keys", key="-GENERATE_KEYS-")]
        ])
    ],
    [sg.Text('_' * 100, size=(80, 1))],  # Add a horizontal separator
    [
        sg.Frame('File Signing', layout=[
            [sg.Text("File to Sign:"), sg.Input(key="-FILE_TO_SIGN-"), sg.FileBrowse()],
            [sg.Text("Signature File:"), sg.Input(key="-SIGNATURE_FILE-"), sg.FileSaveAs(), sg.Button("Sign", key="-SIGN-")]
        ])
    ],
    [sg.Text('_' * 100, size=(80, 1))],  # Add another horizontal separator
    [
        sg.Frame('Signature Verification', layout=[
            [sg.Text("Verify Key Directory:"), sg.Input(key="-VERIFY_KEY_DIR-"), sg.FolderBrowse()],
            [sg.Text("File to Verify:"), sg.Input(key="-FILE_TO_VERIFY-"), sg.FileBrowse()],
            [sg.Text("Signature File to Verify:"), sg.Input(key="-SIGNATURE_FILE_TO_VERIFY-"), sg.FileBrowse()],
            [sg.Button("Verify", key="-VERIFY-")]
        ])
    ],
    [sg.Output(size=(80, 20))],
]

# Create the window
window = sg.Window("OpenSSL Key and Sign Utility", layout,finalize=True)


# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == "-GENERATE_KEYS-":
        private_key_dir = values["-PRIVATE_KEY_DIR-"]
        public_key_dir = values["-PUBLIC_KEY_DIR-"]
        result = generate_keys(private_key_dir, public_key_dir)
        if result is True:
            sg.popup("Keys generated successfully!")
        else:
            sg.popup(f"Error generating keys: {result}")
    elif event == "-SIGN-":
        file_to_sign = values["-FILE_TO_SIGN-"]
        signature_file = values["-SIGNATURE_FILE-"]
        private_key_file = os.path.join(private_key_dir, "private_key.pem")  # Added this line
        result = sign_file(file_to_sign, signature_file, private_key_file)
        if result is True:
            sg.popup("File signed successfully!")
        else:
            sg.popup(f"Error signing file: {result}")
    elif event == "-VERIFY-":
        verify_key_dir = values["-VERIFY_KEY_DIR-"]
        file_to_verify = values["-FILE_TO_VERIFY-"]
        signature_file_to_verify = values["-SIGNATURE_FILE_TO_VERIFY-"]
        public_key_file_to_verify = os.path.join(verify_key_dir, "public_key.pem")
        result = verify_signature(
            public_key_file_to_verify, signature_file_to_verify, file_to_verify
        )
        if result is True:
            sg.popup("Signature verification successful!")
        else:
            sg.popup("Signature verification failed!")

# Close the window
window.close()
