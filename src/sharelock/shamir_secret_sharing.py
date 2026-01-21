
"""
This module handles splitting and combining Shamir Secret Sharing shares.

"""


import base64


from Crypto.Protocol.SecretSharing import Shamir



SHAMIR_SPLIT_LENGTH = 16



PADDING_BYTE = b'\x00'



# byte to protect data from being truncated when it ends in the padding byte

ALTERNATE_PADDING_BYTE = b'\x01'




def split( data: bytes, shares: int, threshold: int, padding_byte: bytes | None = PADDING_BYTE ):

    """
    Use Shamir's Secret Sharing to split 'data' into 'shares' keys.
    The combine() function requires 'threshold' of these keys to reconstruct the data.

    Since the Shamir.split function ( that this is built upon ) can only use 16 byte chunks,
    the last chunk will be right-padded with 'padding_byte', meaning that the combine function will remove all
    trailing 'padding_byte' bytes. Keep this in mind if the 'data' ends with that byte.


    Params:
    -------
    data : bytes
        The data to split. Each key's length will be similar to the length of this data.
    shares : int
        The number of secret shares to create from this 'data'.
    threshold : int
        The number of created secret shares to require to reconstruct the 'data'.
    padding_byte : bytes | None - default b'\x00'
        The byte with which to right-pad the last chunk to make Shamir.split work. 
        If set to None, use the default.


    Returns:
    -------
    list[ tuple[ int, bytes ] ]
        A list of tuples of ( share_index, share_value ) for reconstruction of the data.


    Raises:
    -------
    ValueError
        If the threshold is not <= number of shares.

    """



    padding_byte = PADDING_BYTE if padding_byte is None else padding_byte



    if shares <= 0:

        raise ValueError( f'Shares ({ shares }) must be > 0.' )



    if threshold <= 0:

        raise ValueError( f'Threshold ({ threshold }) must be > 0.' )



    if threshold > shares:

        raise ValueError( f'Threshold ({ threshold }) must be <= number of shares ({ shares }).' )




    data_shares = [ 
        ( index, b'' ) 
        for index in range( 1, shares + 1 ) 
    ]




    data = data + ALTERNATE_PADDING_BYTE



    for i in range( 0, len( data ), SHAMIR_SPLIT_LENGTH ):


        current_chunk = data[ i : i + SHAMIR_SPLIT_LENGTH ]


        current_chunk = current_chunk.ljust( SHAMIR_SPLIT_LENGTH, padding_byte )


        result = Shamir.split( threshold, shares, current_chunk, False )



        for ( index, share ) in result:


            share_index, share_value = data_shares[ index - 1 ]


            data_shares[ index - 1 ] = ( share_index, share_value + share )



    return data_shares








def combine( shares: list[ tuple[ int, bytes ] ], padding_byte: bytes | None = PADDING_BYTE ) -> bytes:

    """
    Combine key shares into the original data from which they were split.


    Params:
    ------
    shares : list[ tuple[ int, bytes ] ]
        The key shares. A list of tuples of share_index-share_value.
    padding_byte : bytes | None - default b'\x00'
        The byte with which to right-strip the result to undo the padding from the split( ) function.
        If set to None, use the default.


    Returns:
    ------
    bytes
        The original data that was split into the shares.

    """



    padding_byte = PADDING_BYTE if padding_byte is None else padding_byte




    if len( shares ) == 0 or len( shares[ 0 ] ) != 2:

        return b''




    result = b''




    for i in range( 0, len( shares[ 0 ][ 1 ] ), SHAMIR_SPLIT_LENGTH ):


        chunks = [ 
            ( index, share[ i : i + SHAMIR_SPLIT_LENGTH ] ) 
            for ( index, share ) in shares 
        ]


        combined_chunk = Shamir.combine( chunks, False )


        result += combined_chunk


    # remove the padding_byte bytes and the alternate padding byte

    unpadded_result = result.rstrip( padding_byte )[ : -1 ]


    return unpadded_result







def print_secrets( shares: list[ tuple[ int, bytes ] ], threshold: int | None = None, quiet = False ):

    """
    Write secret shares to stdout.


    Params:
    ------
    shares : list[ tuple[ int, bytes ] ]
        The key shares. A list of tuples of share_index-share_value.
    threshold : int | None - default None
        The number of shares needed to reconstruct the data.
        If set to None, do not print instructions for how many shares are needed for reconstruction.
    quiet : bool - default False
        If set to true, do not print user instructions - only print the shares.
        Useful for scripting.

    """


    threshold_text = f'( Any { threshold } shares are required for reconstruction )' if threshold is not None else ''



    if not quiet:

        print( f'Secret Shares: { threshold_text }' )



    padding_required = len( str( len( shares ) ) )



    for index, secret in shares:


        encoded_secret = base64.b64encode( secret ).decode( )


        print( f'{ str( index ).ljust( padding_required ) } - { encoded_secret }' )



