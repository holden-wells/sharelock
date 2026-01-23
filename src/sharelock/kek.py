

import sys

from pathlib import Path



import ecies

import coincurve

import eth_keys




import sharelock.shamir_secret_sharing as sss




class KEK:



    def __init__( self ):

        pass

    


    def generate( self, public_key_filename: str, shares: int, threshold: int, padding_byte: bytes = None, quiet: bool = False ):

        """

        Generate a new asymetric Key Encryption Key. The generated key shares must be shared each time this is done.


        Params:
        ------
        public_key_filename : str
            The filename at which the public key will be written
        shares : int
            The number of key shares the private key will be broken into
        threshold : int
            The number of key shares needed to reconstruct the private key
        padding_byte : bytes
            The bytes used to pad chunks of the key before it is split if needed

        """


        # create private/public key pair

        key_encryption_key = eth_keys.keys.PrivateKey( coincurve.utils.get_valid_secret( ) )



        private_key = key_encryption_key.to_bytes( )


        public_key = key_encryption_key.public_key.to_bytes( )


        
        # write public key to file

        try:

            Path( public_key_filename ).resolve( ).write_bytes( public_key )

        except:

            print( f'Could not write public key to file "{ public_key_filename }".', file = sys.stderr )

            exit( 1 )




        # split private key and print shares


        try:

            split_key = sss.split( private_key, shares, threshold, padding_byte )

        except Exception as e:

            print( f'Could not split private key: { e.args[ 0 ] }', file = sys.stderr )

            exit( 1 )



        sss.print_secrets( split_key, threshold = threshold, quiet = quiet )




    def encrypt( self, data: bytes, public_key: bytes ):

        """
        Encrypt data using the public key.

        
        Params:
        -------
        data : bytes
            The data to encrypt
        public_key : bytes
            The public key to encrypt with


        Returns:
        -------
        bytes
            The encrypted ciphertext

        """


        encrypted = ecies.encrypt( public_key, data )


        return encrypted





    def decrypt( self, data: bytes, private_key: bytes ):

        """
        Decrypt data using the private key.

        
        Params:
        -------
        data : bytes
            The data to decrypt
        public_key : bytes
            The private key to encrypt with


        Returns:
        -------
        bytes
            The original text

        """




        try:

            decrypted = ecies.decrypt( private_key, data )


        except:

            print( 'Could not perform decryption. Either the keys are wrong or the encrypted data has been modified.', file = sys.stderr )

            exit( 1 )



        return decrypted





    def load( self, public_key_filename: str ):

        """

        Load a public key from a file.


        Params:
        -------
        public_key_filename : str
            The filename that contains the public key


        Returns:
        -------
        bytes
            The public key

        """



        try:

            key_bytes = Path( public_key_filename ).resolve( ).read_bytes( )


        except:


            print( f'Could not read public key at "{ public_key_filename }".', file = sys.stderr )


            exit( 1 )



        return key_bytes



