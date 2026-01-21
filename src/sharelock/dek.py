
"""

This module handles Data Encryption Key operations.

This includes generating, loading, and using Data Encryption Keys

"""



import sys



from Crypto.Random import get_random_bytes


from Crypto.Cipher import AES



NONCE_LENGTH = 16



class DEK:


    def __init__( self ):

        pass



    def generate( self, key_bytes: int = 32 ):

        """
        Generate an AES DEK with 'key_bytes' bytes.

        Params:
        -------
        key_bytes : int - default 32
            How many bytes the key should be. Should always be a power of 2.
        """

        try:


            return get_random_bytes( key_bytes )


        except:

            print( 'Could not generate Data Encryption Key of size "{ key_bytes }".', file = sys.stderr )

            exit( 1 )





    def encrypt( self, data: bytes, key: bytes ):
        """
        Encrypt data using the DEK.

        
        Params:
        -------
        data : bytes
            The data to encrypt
        key : bytes
            The key to encrypt with


        Returns:
        -------
        ciphertext: bytes
            The encrypted data
        nonce: bytes
            The nonce ( required for decryption )

        """


        cipher = AES.new( key, AES.MODE_GCM )


        ciphertext = cipher.encrypt( data )


        return ciphertext, cipher.nonce

    



    def decrypt( self, data: bytes, key: bytes, nonce: bytes ):

        """
        Decrypt data using the DEK

        
        Params:
        -------
        data : bytes
            The data to decrypt
        key : bytes
            The decryption key
        nonce : bytes
            The nonce ( created at encryption )


        Returns:
        -------
        bytes
            The decrypted data

        """


        cipher = AES.new( key, AES.MODE_GCM, nonce = nonce )


        try:

            result = cipher.decrypt( data )

        except:


            print( f'Could not decrypt data using DEK. The encrypted file may have been modified.', file = sys.stderr )


            exit( 1 )


        return result







