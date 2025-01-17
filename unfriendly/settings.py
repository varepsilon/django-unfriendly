from django.conf import settings

#
# UNFRIENDLY_SECRET is used for encryption/decryption
# Note: AES keys must be either 16, 24, or 32 bytes long
#
UNFRIENDLY_SECRET = getattr(settings, 'UNFRIENDLY_SECRET',
                        getattr(settings, 'SECRET_KEY', 'hush'*8)[0:32])


#
# UNFRIENDLY_ENFORCE_CHECKSUM whether or not the decrypted data is validated
# against a crc checksum to detect tampering
#
UNFRIENDLY_ENFORCE_CHECKSUM = getattr(settings,
                                      'UNFRIENDLY_ENFORCE_CHECKSUM', True)
