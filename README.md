# Basic Blob Finder

> Identify Azure blobs using a list of account name and container name strings

This is a simple proof-of-concept tool to hunt for public Azure storage
containers and enumerate the blobs therein. It is naive in the implementation,
is single-threaded, and assumes you know what you are looking for.

## Usage

Create a file with account name and container name strings that you wish to enumerate. The
file should have one entry per line, and can be in one of two formats:

1. `name` - When a single string is specified, Basic Blob Finder will use the
   string as both the account name and the container name.
2. `account:container` - When a colon is used to separate two strings, the
   first string is used to test as the account name; the second is used as the
    container name.

Words that do not match the requirements for an account name or a container name
are skipped. See [Storage account overview](https://docs.microsoft.com/en-us/azure/storage/common/storage-account-overview#:~:text=When%20naming%20your%20storage%20account,can%20have%20the%20same%20name.)
and [Naming and Referencing Containers, Blobs, and Metadata](https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata)
for the naming requirement details.

See the file `namelist` for examples.

Basic Blob Finder will test if the account name exists using DNS. If the account
name exists, Basic Blob Finder will test for the container name using an HTTPS request. If
the account name and the container name exist, and if the container name is public, then
Basic Blob Finder will identify the disclosed blobs by URL, as shown here:

```
basicblobfinder (main) $ ./basicblobfinder.py
Test for the presence of Azure Blob resources.
This is a naive PoC to test for the presence of Azure Blob resources which could
certainly benefit from threading and other performance improvements.

Usage: ./basicblobfinder.py <name list file>

The name list file should be in the format storageaccount:containername or a
single string that is used as both the storage account and container name.
(ex. falsimentis:falsimentis-container or falsimentis). Invalid names are skipped.

basicblobfinder (main) $ cat namelist
falsimentis
falsi-mentis
fa
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
falsimentis:falsimentis-container
falsimentis:falsimentis-container2
invalidacct:nosuchcontainer
basicblobfinder (main) $ ./basicblobfinder.py namelist
Invalid storage account name falsi-mentis, skipping.
Invalid storage account name fa, skipping.
Invalid storage account name ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, skipping.

Valid storage account and container name: falsimentis:falsimentis-container
Blob data objects:
    https://falsimentis.blob.core.windows.net/falsimentis-container/01 Newborn Euselachii.wav
```

## Contact

[Joshua Wright](mailto:jwright@hasbog.com) | [@joswr1ght](https://twitter.com/joswr1ght)
