
"""

Module for performing decryption.

"""



import sys


import base64


from pathlib import Path




import sharelock.shamir_secret_sharing as sss


import sharelock.kek as kek


import sharelock.dek as dek






class Decrypter:



    def __init__( self ):

        pass




    def decrypt( self, encrypted_data_filename: str, encrypted_dek_filename: str ):

        """

        Perform decryption on an encrypted file. Writes the decrypted data to stdout.


        Params:
        -------
        encrypted_data_filename : str
            The filename at which resides the encrypted ( with the DEK ) data.
        encrypted_dek_filename : str
            The filename at which resides the encrypted ( with the KEK ) DEK.

        """



        # read dek and encrypted data from file

        try:

            encrypted_data = Path( encrypted_data_filename ).resolve( ).read_bytes( )

        except:

            print( f'Could not read encrypted data from file at "{ encrypted_data_filename }".', file = sys.stderr )

            exit( 1 )


        try:

            encrypted_dek = Path( encrypted_dek_filename ).resolve( ).read_bytes( )

        except:

            print( f'Could not read encrypted DEK from file at "{ encrypted_dek_filename }".', file = sys.stderr )

            exit( 1 )





        # read shares from stdin

        input_shares = self.read_shares( )



        # get private key from shares

        private_kek = sss.combine( input_shares )



        # decrypt dek

        kek_context = kek.KEK( )


        decrypted_dek_file = kek_context.decrypt( encrypted_dek, private_kek )


        decrypted_dek = decrypted_dek_file




        # decrypt data and write to stdout


        dek_context = dek.DEK( )


        encrypted_data, nonce = self.parse_encrypted_data( encrypted_data )


        decrypted_data = dek_context.decrypt( encrypted_data, decrypted_dek, nonce )


        sys.stdout.buffer.write( decrypted_data )




    def read_shares( self ):

        """

        Read key shares from stdin and decode them.

        """


        try:

            shares_text = sys.stdin.read( )


            base64_encoded_shares = shares_text.split( '\n' )

        except:

            print( 'Could not decode stdin as valid key shares. Key shares should be in the form:', file = sys.stderr )

            print( '{ index } - { base64 encoded share value }', file = sys.stderr )

            print( 'With one entry on each line.', file = sys.stderr )


            exit( 1 )



        shares = [ ]




        for encoded_share in base64_encoded_shares:


            if len( encoded_share.strip( ) ) == 0:

                continue


            shares.append( self.decode_share( encoded_share ) )



        return shares




    def decode_share( self, encoded_share: str ):
        """
        Decode a single encoded share.


        Params:
        -------
        encoded_share : str
            An encoded share value.
            In the form: { share number } - { base64 encoded share }
        """



        splitted = encoded_share.split( '-' )



        index = int( splitted[ 0 ].strip( ) )


        share_value = '-'.join( splitted[ 1: ] ).strip( )


        share = base64.b64decode( share_value ) 


        return ( index, share )





    def parse_encrypted_data( self, encrypted_data: bytes ):

        """

        Separate the encrypted data from its nonce.


        Params:
        ------
        encrypted_data : bytes
            The input data to separate

        """


        nonce = encrypted_data[ : dek.NONCE_LENGTH ]


        encrypted_data = encrypted_data[ dek.NONCE_LENGTH : ]


        return ( encrypted_data, nonce )


