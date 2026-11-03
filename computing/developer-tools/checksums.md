# MD5

## Introduction

MD5 (Message Digest Algorithm 5) is a widely used cryptographic hash function that produces a 128-bit (32-character hexadecimal) hash value. It is commonly used to verify the integrity of files by comparing the original and downloaded file's hash values.

⚠️ Note: MD5 is considered **cryptographically insecure** and should not be used for security-sensitive applications such as password hashing or digital signatures.

## Generate MD5 Checksum of a File

```bash
# Linux/macOS
md5sum myfile.txt

# Windows (PowerShell)
Get-FileHash myfile.txt -Algorithm MD5
```

```text
# output
d41d8cd98f00b204e9800998ecf8427e  myfile.txt
```

## Verifying File Integrity

```bash
# Create a checksum file
md5sum myfile.txt > myfile.txt.md5

# Verify it later
md5sum -c myfile.txt.md5 # myfile.txt: OK
```

## Tips & Best Practices

- Always compare MD5 checksums when downloading large files (e.g., ISOs, datasets).
- For security-sensitive use cases, use `sha256sum` or `sha512sum` instead.
- Some software distribution sites provide `.md5`, `.sha256`, or `.asc` files for verification—check those before executing or installing.

## Alternatives to MD5

| Algorithm | Use Case                | Security  |
| --------- | ----------------------- | --------- |
| SHA-1     | Legacy, weak            | ❌ Weak   |
| SHA-256   | General-purpose hashing | ✅ Strong |
| SHA-512   | Higher security need    | ✅ Strong |
| BLAKE2    | Fast and secure         | ✅ Strong |
