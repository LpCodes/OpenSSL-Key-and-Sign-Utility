Sure! Here's a sample README file for your OpenSSL Key and Sign Utility:

# OpenSSL Key and Sign Utility

The OpenSSL Key and Sign Utility is a Python script that provides a graphical user interface (GUI) for generating RSA key pairs, signing files, and verifying signatures using the OpenSSL command-line tool.

## Prerequisites

Before using this utility, make sure you have the following prerequisites installed on your system:

- Python 3: The utility is written in Python and requires Python 3 to be installed.
- OpenSSL: The utility uses the OpenSSL command-line tool for generating keys, signing files, and verifying signatures. Make sure OpenSSL is installed on your system and accessible from the command line.

## Installation

1. Clone or download the utility from the repository.
2. Install the required Python packages by running the following command in your terminal or command prompt:

   ```shell
   pip install PySimpleGUI
   ```

## Usage

To run the OpenSSL Key and Sign Utility, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where you saved the utility.
3. Run the following command to start the utility:

   ```shell
   python openssl_key_and_sign_utility.py
   ```

4. The utility's GUI window will open, providing the following options:

   - **Generate Keys**: Click this button to generate RSA key pairs. You need to specify the private key and public key directories where the generated keys will be saved.
   - **Sign**: Use this button to sign a file using a private key. Select the file to sign and specify the output signature file path.
   - **Verify**: Click this button to verify the signature of a file. Specify the directory containing the public key, the file to verify, and the signature file to verify.

   Note: The utility uses the SHA256 hashing algorithm for signing and verification.

5. After performing the desired operation, a popup message will appear indicating the status of the operation (success or failure). Additionally, the output window at the bottom of the GUI will display any error messages or output from the OpenSSL commands.

6. Close the utility by closing the GUI window or pressing Ctrl+C in the terminal or command prompt.


## Contributing

Contributions to this utility are welcome! If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue.
