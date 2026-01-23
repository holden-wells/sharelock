
"""

This program encrypts/decrypts a file whose key is split and shared between multiple individuals.

"""



import sys


import argparse



import sharelock.kek as kek


import sharelock.encrypter as encrypter


import sharelock.decrypter as decrypter





__version__ = '0.1.2'




DEFAULT_PUBLIC_KEY_FILE = 'KEK.bin'


DEFAULT_DEK_FILE = 'DEK.bin'





def create_parser( ) -> argparse.ArgumentParser:
    """
    Set up an ArgumentParser with all available command line arguments.
    """


    parser = argparse.ArgumentParser( 
        prog = 'sharelock',
        description = 'Utility to encrypt a file with a key shared among multiple individuals.',
    )


    subparser = parser.add_subparsers( dest = 'mode' )



    encrypt_parser = subparser.add_parser(
        'encrypt',
        help = 'Commands for encrypting data',
    )


    decrypt_parser = subparser.add_parser(
        'decrypt',
        help = 'Commands for decrypting data',
    )


    generate_parser = subparser.add_parser(
        'generate',
        help = 'Commands for generating Key Encryption Keys',
    )



    decrypt_parser.add_argument(
        '-i',
        '--input-file',
        required = True,
        help = 'File from which to read encrypted data and attempt decryption',
    )


    decrypt_parser.add_argument(
        '-d',
        '--dek-file',
        help = 'Path from which to read the encrypted Data Encryption Key',
        default = DEFAULT_DEK_FILE,
    )



    encrypt_parser.add_argument(
        '-o',
        '--output-file',
        required = True,
        help = 'File to which to write encrypted data ( use - for stdout )',
    )



    encrypt_parser.add_argument(
        '-d',
        '--dek-file',
        help = 'Path at which Data Encryption Key file will be written',
        default = DEFAULT_DEK_FILE,
    )



    encrypt_parser.add_argument(
        '-k',
        '--kek-file',
        help = 'Path to Public Key Encryption Key file',
        default = DEFAULT_PUBLIC_KEY_FILE,
    )



    generate_parser.add_argument(
        '-k',
        '--kek-file',
        help = 'Path to Public Key Encryption Key file',
        default = DEFAULT_PUBLIC_KEY_FILE,
    )


    generate_parser.add_argument(
        '-s',
        '--shares',
        help = 'The number of key shares to break the generate Key Encryption Key into',
        type = int,
        required = True,
    )


    generate_parser.add_argument(
        '-t',
        '--threshold',
        help = 'The number of key shares required to perform decryption ( Should be <= the number of shares )',
        type = int,
        required = True,
    )


    generate_parser.add_argument(
        '-q',
        '--quiet',
        help = 'Whether or not to print additional instructions to the user.',
        action = 'store_true',
        default = False,
    )



    return parser






def main( ):



    parser = create_parser( )



    args = parser.parse_args( )




    if args.mode == 'generate':

        generator = kek.KEK( )


        generator.generate( 
            public_key_filename = args.kek_file,
            shares = args.shares,
            threshold = args.threshold,
            quiet = args.quiet,
        )


        exit( 0 )



    if args.mode == 'encrypt':

        encrypt_context = encrypter.Encrypter( )


        encrypt_context.encrypt(
            public_key_filename = args.kek_file,
            output_filename = args.output_file,
            dek_filename = args.dek_file,
        )


        exit( 0 )



    if args.mode == 'decrypt':


        decrypt_context = decrypter.Decrypter( )


        decrypt_context.decrypt(
            encrypted_data_filename = args.input_file,
            encrypted_dek_filename = args.dek_file,
        )


        exit( 0 )



    print( 'Unknown execution mode "{ args.mode }".', file = sys.stderr )


    exit( 1 )





if __name__ == '__main__':

    main( )





