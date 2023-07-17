import os
import subprocess

import PySimpleGUI as sg

# GUI layout
layout = [
    [sg.Text('Private Key Directory:'), sg.Input(key='-PRIVATE_KEY_DIR-'), sg.FolderBrowse()],
    [sg.Text('Public Key Directory:'), sg.Input(key='-PUBLIC_KEY_DIR-'), sg.FolderBrowse()],
    [sg.Text('File to Sign:'), sg.Input(key='-FILE_TO_SIGN-'), sg.FileBrowse()],
    [sg.Button('Generate Keys', key='-GENERATE_KEYS-')],
    [sg.Text('Signature File:'), sg.Input(key='-SIGNATURE_FILE-'), sg.FileSaveAs(), sg.Button('Sign', key='-SIGN-')],
    [sg.Text('Verify Key Directory:'), sg.Input(key='-VERIFY_KEY_DIR-'), sg.FolderBrowse()],
    [sg.Text('File to Verify:'), sg.Input(key='-FILE_TO_VERIFY-'), sg.FileBrowse()],
    [sg.Text('Signature File to Verify:'), sg.Input(key='-SIGNATURE_FILE_TO_VERIFY-'), sg.FileBrowse()],
    [sg.Button('Verify', key='-VERIFY-')],
    [sg.Output(size=(80, 20))]
]

# Create the window
window = sg.Window('OpenSSL Key and Sign Utility', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-GENERATE_KEYS-':
        try:
            private_key_dir = values['-PRIVATE_KEY_DIR-']
            public_key_dir = values['-PUBLIC_KEY_DIR-']
            private_key_file = os.path.join(private_key_dir, 'private_key.pem')
            public_key_file = os.path.join(public_key_dir, 'public_key.pem')
            subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-out', private_key_file], check=True)
            subprocess.run(['openssl', 'pkey', '-in', private_key_file, '-pubout', '-out', public_key_file], check=True)
            sg.popup('Keys generated successfully!')
        except subprocess.CalledProcessError as e:
            sg.popup(f'Error generating keys: {e.stderr}')
    elif event == '-SIGN-':
        try:
            file_to_sign = values['-FILE_TO_SIGN-']
            signature_file = values['-SIGNATURE_FILE-']
            subprocess.run(['openssl', 'dgst', '-sha256', '-sign', private_key_file, '-out', signature_file, file_to_sign], check=True)
            sg.popup('File signed successfully!')
        except subprocess.CalledProcessError as e:
            sg.popup(f'Error signing file: {e.stderr}')
    elif event == '-VERIFY-':
        try:
            verify_key_dir = values['-VERIFY_KEY_DIR-']
            file_to_verify = values['-FILE_TO_VERIFY-']
            signature_file_to_verify = values['-SIGNATURE_FILE_TO_VERIFY-']
            public_key_file_to_verify = os.path.join(verify_key_dir, 'public_key.pem')
            result = subprocess.run(
                ['openssl', 'dgst', '-sha256', '-verify', public_key_file_to_verify, '-signature', signature_file_to_verify,
                 file_to_verify], capture_output=True, check=True)
            if result.returncode == 0:
                sg.popup('Signature verification successful!')
            else:
                sg.popup('Signature verification failed!')
        except subprocess.CalledProcessError as e:
            sg.popup(f'Error verifying signature: {e.stderr}')

# Close the window
window.close()
