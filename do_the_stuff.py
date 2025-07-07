import os

# Directory containing the files
directory = "./ldap_in/"

# The byte sequence you want to append
bytes_to_prepend = b"ldap://127.0.0.1:8888/ou=users,dc=example,dc=com"  # Example: ABCD



for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)

    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            original_data = f.read()

        with open(file_path, "wb") as f:
            f.write(bytes_to_prepend + original_data)


