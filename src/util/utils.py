class Utils:
    @staticmethod
    def string_to_byte_array(name):
        if name is None:
            return None

        name = name.replace(" ", "")
        if len(name) > 16:
            name = name[:16]
        else:
            for x in range(0, 16 - len(name)):
                name += " "

        print name
        print str(len(name))

        return list(bytearray(name))

    @staticmethod
    def byte_array_to_string(byte_array):
        if byte_array is None:
            return None
        return ("".join(map(chr, byte_array))).replace(" ", "")

