with open("seed1", "wb") as f:
    f.write(b"\x05\x01\x00")            # Client hello
    f.write(b"-=^..^=-")
    f.write(b"\x05\x00")                # Server selects no-auth
    f.write(b"-=^..^=-")
    f.write(b"\x05\x01\x00\x03\x0bwikipedia\x00\x50")  # Connect request

