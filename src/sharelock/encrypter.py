
"""

Module for performing encryption.

"""



import sys


from pathlib import Path



import sharelock.dek as dek

import sharelock.kek as kek




class Encrypter:


    def __init__( self ):

        pass



    def encrypt( self, public_key_filename: str, output_filename: str, dek_filename: str ):

        """

        Perform Encryption on the data passed through stdin.


        Params:
        -------
        public_key_filename : str
            The filename that holds the Public Key Encryption Key
        output_filename : str
            The filename at which to write the encrypted data at ( set to '-' to write to stdout )
        dek_filename : str
            The filename that holds the encrypted Data Encryption Key

        """


        # read data to encrypt from stdin

        input_data = sys.stdin.buffer.read( )



        # load kek

        kek_context = kek.KEK( )

        public_kek = kek_context.load( public_key_filename )



        # generate DEK

        dek_context = dek.DEK( )

        dek_key = dek_context.generate( )



        # encrypt data

        encrypted_data, nonce = dek_context.encrypt( input_data, dek_key )



        # encrypt DEK using KEK

        encrypted_dek = kek_context.encrypt( dek_key, public_kek )



        # write encrypted data and DEK to files

        output_data = bytes( nonce ) + encrypted_data

        self.write_output_data( output_filename, output_data )


        try:

            Path( dek_filename ).resolve( ).write_bytes( encrypted_dek )


        except:

            print( f'Could not write encrypted DEK to file at "{ dek_filename }".', file = sys.stderr )

            exit( 1 )





    def write_output_data( self, output_filename: str, output_data: bytes ):

        """
        Write 'output_data' to the file at 'output_filename'.


        Params:
        -------
        output_filename : str
            The filename at which to write the data
        output_data : bytes
            The data to write to the file

        """


        if output_filename == '-':

            sys.stdout.buffer.write( output_data )

            return


        try:

            Path( output_filename ).resolve( ).write_bytes( output_data )

        except:

            print( f'Could not write encrypted data to file at "{ output_filename }".', file = sys.stderr )

            exit( 1 )





