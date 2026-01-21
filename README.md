


# Sharelock
---
* Command line tool to create encrypted files whose decryption key is split and shared between multiple individuals.
* The program uses Shamir's Secret Sharing, meaning that you can specify the number of keys and how many keys are required to decrypt the data.
* This program is mainly useful in situations where high security is required.
    * For example, a database dump could be piped into this program.
        * The dump would be encrypted with a split key shared among some number of database administrators.
        * If one or two administrator keys were compromised, the data would still be secure.
        * The tradeoff is that the number of compromised administrators for a succesful attack is the same number that would be needed to restore the backup.


## Security Warning
---
* This tool is in early development.
* Although it uses established cryptographic libraries to handle encryption/decryption, it has not been independently audited.
* Use this software to protect sensitive data at your own risk.


## Install
---

### Pip
```bash

pip install sharelock

# Verify installation
sharelock -h

```

### From source
```bash
git clone https://www.github.com/holden-wells/sharelock.git

cd sharelock

pip install .

# Verify installation
sharelock -h
```



## How it works
---
* Sharelock has three main modes:


### Generation
1. Generate Private/Public Key Encryption Key Pair
2. Save the Public key to a file
3. Split the Private key using Shamir's Secret Sharing and write to stdout
* This split key pieces should be securely distributed to their responsible parties.
* Whatever threshold is specified at key creation time is the number of key pieces required to decrypt the data.


### Encryption
1. Take in a file on stdin
2. Generate a Symetric Data Encryption Key
3. Encrypt stdin using the Data Encryption Key and write to an output file
4. Encrypt the Data Encryption Key using the Key Encryption Key's Public Key
5. Write the encrypted Data Encryption Key to an output file


### Decryption
1. Take in a file via cli args
2. Take in key shares on stdin
3. Combine the key shares to derive the Private Key Encryption Key
4. Decrypt the Data Encryption Key using the Private Key
5. Decrypt the Encrypted Data File using the Decrypted Data Encryption Key




## Basic Usage
---


### Generate
```
usage: sharelock.py generate [-h] [-k KEK_FILE] -s SHARES -t THRESHOLD [-q QUIET]

options:
  -h, --help            show this help message and exit
  -k, --kek-file KEK_FILE
                        Path to Public Key Encryption Key file
  -s, --shares SHARES   The number of key shares to break the generate Key Encryption Key into
  -t, --threshold THRESHOLD
                        The number of key shares required to perform decryption ( Should be <= the
                        number of shares )
  -q, --quiet QUIET     Whether or not to print additional instructions to the user.
```
* Command for generating a random Key Encryption Key
* The value of 'SHARES' is how many keys will be created to be shared with responsible individuals
    * These key shares will only ever be printed to stdout once and there is no way to recover them or the encrypted data if too many of them are lost
* The Public Key Encryption Key will be written to the file supplied with '-k'.



### Encrypt
```
usage: sharelock.py encrypt [-h] -o OUTPUT_FILE [-d DEK_FILE] [-k KEK_FILE]

options:
  -h, --help            show this help message and exit
  -o, --output-file OUTPUT_FILE
                        File to which to write encrypted data ( use - for stdout )
  -d, --dek-file DEK_FILE
                        Path at which Data Encryption Key file will be written
  -k, --kek-file KEK_FILE
                        Path to Public Key Encryption Key file
```
* Command for encrypting a file on stdin.
* The "-d" and "-k" arguments are optional overrides and will use a default file name if left empty.
* This will generate the output file at "-o" and the DEK file at "-d" and requires the public key file at "-k"



### Decrypt
```
usage: sharelock.py decrypt [-h] -i INPUT_FILE [-d DEK_FILE]

options:
  -h, --help            show this help message and exit
  -i, --input-file INPUT_FILE
                        File from which to read encrypted data and attempt decryption
  -d, --dek-file DEK_FILE
                        Path from which to read the encrypted Data Encryption Key
```
* Command for decrypting a file and writing its contents to stdout.
* The "-d" argument is an optional override and will use a default file name if left empty.



## Planned Updates
---
* 0.2.0
    * Ability to roll Key Encryption Keys in case of lost or stolen key
* 0.3.0
    * Stricter file integrity checks
* 1.0.0
    * Use a basic file format that stores the Public Key Encryption Key and Data Encryption Key with the data
    * Ability to use a keyring that stores public keys per user.
        * Ability to add or remove a public key by name




Licensed under the MIT License - see [LICENSE](./LICENSE) for details.
Third-party licenses: see [THIRDPARTYLICENSES](./THIRDPARTYLICENSES)


