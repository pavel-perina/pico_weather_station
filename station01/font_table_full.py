font_data = bytearray( \
    b'\x00\x00\x00\x00\x00\x00' \
    b'\x00\x3E\x45\x51\x45\x3E' \
    b'\x00\x3E\x7B\x6F\x7B\x3E' \
    b'\x00\x1C\x3E\x7C\x3E\x1C' \
    b'\x00\x18\x3C\x7E\x3C\x18' \
    b'\x00\x18\x5E\x6E\x5E\x18' \
    b'\x00\x18\x5C\x6E\x5C\x18' \
    b'\x00\x00\x18\x18\x00\x00' \
    b'\xFF\xFF\xE7\xE7\xFF\xFF' \
    b'\x00\x18\x24\x24\x18\x00' \
    b'\xFF\xE7\xDB\xDB\xE7\xFF' \
    b'\x70\x88\x88\x8D\x73\x07' \
    b'\x00\x0E\x51\xF1\x51\x0E' \
    b'\x00\x60\x60\x3F\x02\x04' \
    b'\x60\x60\x3F\xC5\xCA\x7C' \
    b'\x00\x2A\x1C\x36\x1C\x2A' \
    b'\x00\x3E\x3E\x1C\x1C\x08' \
    b'\x00\x08\x1C\x1C\x3E\x3E' \
    b'\x00\x14\x36\x7F\x36\x14' \
    b'\x00\x00\x5F\x00\x5F\x00' \
    b'\x00\x06\x09\x7F\x01\x7F' \
    b'\x40\x9A\xA5\xA5\x59\x02' \
    b'\x00\xE0\xE0\xE0\xE0\xE0' \
    b'\x00\x94\xB6\xFF\xB6\x94' \
    b'\x00\x08\x0C\xFE\x0C\x08' \
    b'\x00\x10\x30\x7F\x30\x10' \
    b'\x08\x08\x08\x3E\x1C\x08' \
    b'\x08\x1C\x3E\x08\x08\x08' \
    b'\x00\x0F\x08\x08\x08\x08' \
    b'\x08\x1C\x08\x08\x1C\x08' \
    b'\x00\x60\x78\x7E\x78\x60' \
    b'\x00\x06\x1E\x7E\x1E\x06' \
    b'\x00\x00\x00\x00\x00\x00' \
    b'\x00\x00\x00\x5F\x00\x00' \
    b'\x00\x00\x07\x00\x07\x00' \
    b'\x00\x14\x7F\x14\x7F\x14' \
    b'\x00\x24\x2A\x6B\x2A\x12' \
    b'\x00\x22\x15\x2A\x54\x22' \
    b'\x00\x36\x49\x56\x20\x50' \
    b'\x00\x00\x0B\x07\x00\x00' \
    b'\x00\x00\x3E\x41\x00\x00' \
    b'\x00\x00\x00\x41\x3E\x00' \
    b'\x00\x08\x2A\x1C\x2A\x08' \
    b'\x00\x08\x08\x3E\x08\x08' \
    b'\x00\x00\xA0\x60\x00\x00' \
    b'\x00\x08\x08\x08\x08\x08' \
    b'\x00\x00\x60\x60\x00\x00' \
    b'\x00\x60\x30\x18\x0C\x06' \
    b'\x00\x3E\x51\x49\x45\x3E' \
    b'\x00\x00\x42\x7F\x40\x00' \
    b'\x00\x62\x51\x49\x49\x46' \
    b'\x00\x22\x49\x49\x49\x36' \
    b'\x00\x18\x14\x52\x7F\x50' \
    b'\x00\x27\x45\x45\x45\x39' \
    b'\x00\x3C\x4A\x49\x49\x30' \
    b'\x00\x01\x01\x79\x05\x03' \
    b'\x00\x36\x49\x49\x49\x36' \
    b'\x00\x06\x49\x49\x29\x1E' \
    b'\x00\x00\x6C\x6C\x00\x00' \
    b'\x00\x00\xAC\x6C\x00\x00' \
    b'\x00\x08\x14\x22\x41\x00' \
    b'\x00\x14\x14\x14\x14\x14' \
    b'\x00\x00\x41\x22\x14\x08' \
    b'\x00\x06\x01\x51\x09\x06' \
    b'\x00\x3E\x41\x5D\x55\x5E' \
    b'\x00\x7E\x11\x11\x11\x7E' \
    b'\x00\x7F\x49\x49\x49\x36' \
    b'\x00\x3E\x41\x41\x41\x22' \
    b'\x00\x7F\x41\x41\x22\x1C' \
    b'\x00\x7F\x49\x49\x49\x41' \
    b'\x00\x7F\x09\x09\x09\x01' \
    b'\x00\x3E\x41\x41\x51\x72' \
    b'\x00\x7F\x08\x08\x08\x7F' \
    b'\x00\x00\x41\x7F\x41\x00' \
    b'\x00\x30\x40\x40\x40\x3F' \
    b'\x00\x7F\x08\x14\x22\x41' \
    b'\x00\x7F\x40\x40\x40\x40' \
    b'\x00\x7F\x06\x18\x06\x7F' \
    b'\x00\x7F\x06\x08\x30\x7F' \
    b'\x00\x3E\x41\x41\x41\x3E' \
    b'\x00\x7F\x09\x09\x09\x06' \
    b'\x00\x3E\x41\x51\x21\x5E' \
    b'\x00\x7F\x09\x09\x19\x66' \
    b'\x00\x26\x49\x49\x49\x32' \
    b'\x00\x01\x01\x7F\x01\x01' \
    b'\x00\x3F\x40\x40\x40\x3F' \
    b'\x00\x07\x18\x60\x18\x07' \
    b'\x00\x7F\x20\x18\x20\x7F' \
    b'\x00\x63\x14\x08\x14\x63' \
    b'\x00\x03\x0C\x78\x0C\x03' \
    b'\x00\x61\x51\x49\x45\x43' \
    b'\x00\x00\x7F\x41\x41\x00' \
    b'\x00\x06\x0C\x18\x30\x60' \
    b'\x00\x00\x41\x41\x7F\x00' \
    b'\x00\x04\x02\x01\x02\x04' \
    b'\x80\x80\x80\x80\x80\x80' \
    b'\x00\x00\x00\x01\x02\x00' \
    b'\x00\x20\x54\x54\x54\x78' \
    b'\x00\x7F\x28\x44\x44\x38' \
    b'\x00\x38\x44\x44\x44\x28' \
    b'\x00\x38\x44\x44\x28\x7F' \
    b'\x00\x38\x54\x54\x54\x18' \
    b'\x00\x08\x7E\x09\x01\x02' \
    b'\x00\x18\xA4\xA4\xA8\x7C' \
    b'\x00\x7F\x08\x04\x04\x78' \
    b'\x00\x00\x44\x7D\x40\x00' \
    b'\x00\x40\x80\x84\x7D\x00' \
    b'\x00\x7F\x10\x28\x44\x00' \
    b'\x00\x00\x41\x7F\x40\x00' \
    b'\x00\x7C\x04\x78\x04\x78' \
    b'\x00\x7C\x08\x04\x04\x78' \
    b'\x00\x38\x44\x44\x44\x38' \
    b'\x00\xFC\x28\x44\x44\x38' \
    b'\x00\x38\x44\x44\x28\xFC' \
    b'\x00\x44\x78\x44\x04\x08' \
    b'\x00\x48\x54\x54\x54\x24' \
    b'\x00\x04\x3F\x44\x40\x20' \
    b'\x00\x3C\x40\x40\x20\x7C' \
    b'\x00\x1C\x20\x40\x20\x1C' \
    b'\x00\x3C\x40\x30\x40\x3C' \
    b'\x00\x44\x28\x10\x28\x44' \
    b'\x00\x1C\xA0\xA0\xA0\x7C' \
    b'\x00\x44\x64\x54\x4C\x44' \
    b'\x00\x08\x36\x41\x41\x00' \
    b'\x00\x00\x00\x7F\x00\x00' \
    b'\x00\x00\x41\x41\x36\x08' \
    b'\x00\x02\x01\x02\x04\x02' \
    b'\x00\x78\x44\x42\x44\x78' \
    b'\x00\xBE\xC1\xC1\x41\x22' \
    b'\x00\x3C\x41\x40\x21\x7C' \
    b'\x00\x38\x54\x56\x55\x18' \
    b'\x00\x20\x56\x55\x56\x78' \
    b'\x00\x20\x55\x54\x55\x78' \
    b'\x00\x20\x55\x56\x54\x78' \
    b'\x00\x20\x54\x55\x54\x78' \
    b'\x00\xB8\xC4\xC4\x44\x28' \
    b'\x00\x38\x56\x55\x56\x18' \
    b'\x00\x38\x55\x54\x55\x18' \
    b'\x00\x38\x55\x56\x54\x18' \
    b'\x00\x00\x45\x7C\x41\x00' \
    b'\x00\x00\x46\x7D\x42\x00' \
    b'\x00\x00\x45\x7E\x40\x00' \
    b'\x00\x7C\x13\x12\x13\x7C' \
    b'\x00\x7C\x12\x13\x12\x7C' \
    b'\x00\x7E\x4A\x4B\x4B\x43' \
    b'\x00\x74\x54\x78\x54\x5C' \
    b'\x00\x7E\x09\x7E\x49\x49' \
    b'\x00\x38\x46\x45\x46\x38' \
    b'\x00\x38\x45\x44\x45\x38' \
    b'\x00\x38\x45\x46\x44\x38' \
    b'\x00\x3C\x42\x41\x22\x7C' \
    b'\x00\x3C\x41\x42\x20\x7C' \
    b'\x00\x1C\xA1\xA0\xA1\x7C' \
    b'\x00\x3C\x43\x42\x43\x3C' \
    b'\x00\x3E\x41\x40\x41\x3E' \
    b'\x00\x38\x44\xC6\x44\x28' \
    b'\x00\x48\x7E\x49\x49\x42' \
    b'\x00\x29\x2A\xFC\x2A\x29' \
    b'\x00\x7F\x09\x29\xF6\xA0' \
    b'\x00\x40\x88\x7E\x09\x02' \
    b'\x00\x20\x54\x56\x55\x78' \
    b'\x00\x00\x44\x7E\x41\x00' \
    b'\x00\x38\x44\x46\x45\x38' \
    b'\x00\x3C\x40\x42\x21\x7C' \
    b'\x00\x7C\x09\x05\x05\x78' \
    b'\x00\x7E\x0D\x19\x31\x7E' \
    b'\x00\x26\x29\x29\x27\x28' \
    b'\x00\x26\x29\x29\x26\x00' \
    b'\x00\x30\x48\x45\x40\x30' \
    b'\x00\x78\x08\x08\x08\x08' \
    b'\x08\x08\x08\x08\x78\x00' \
    b'\x00\x17\x08\x04\x6A\x58' \
    b'\x00\x17\x08\x34\x22\x70' \
    b'\x00\x00\x00\x7D\x00\x00' \
    b'\x08\x14\x22\x08\x14\x22' \
    b'\x22\x14\x08\x22\x14\x08' \
    b'\x11\x44\x11\x44\x11\x44' \
    b'\x55\xAA\x55\xAA\x55\xAA' \
    b'\xEE\xBB\xEE\xBB\xEE\xBB' \
    b'\x00\x00\x00\xFF\x00\x00' \
    b'\x08\x08\x08\xFF\x00\x00' \
    b'\x14\x14\x14\xFF\x00\x00' \
    b'\x08\x08\xFF\x00\xFF\x00' \
    b'\x08\x08\xF8\x08\xF8\x00' \
    b'\x14\x14\x14\xFC\x00\x00' \
    b'\x14\x14\xF7\x00\xFF\x00' \
    b'\x00\x00\xFF\x00\xFF\x00' \
    b'\x14\x14\xF4\x04\xFC\x00' \
    b'\x14\x14\x17\x10\x1F\x00' \
    b'\x08\x08\x0F\x08\x0F\x00' \
    b'\x14\x14\x14\x1F\x00\x00' \
    b'\x08\x08\x08\xF8\x00\x00' \
    b'\x00\x00\x00\x0F\x08\x08' \
    b'\x08\x08\x08\x0F\x08\x08' \
    b'\x08\x08\x08\xF8\x08\x08' \
    b'\x00\x00\x00\xFF\x08\x08' \
    b'\x08\x08\x08\x08\x08\x08' \
    b'\x08\x08\x08\xFF\x08\x08' \
    b'\x00\x00\x00\xFF\x14\x14' \
    b'\x00\x00\xFF\x00\xFF\x08' \
    b'\x00\x00\x1F\x10\x17\x14' \
    b'\x00\x00\xFC\x04\xF4\x14' \
    b'\x14\x14\x17\x10\x17\x14' \
    b'\x14\x14\xF4\x04\xF4\x14' \
    b'\x00\x00\xFF\x00\xF7\x14' \
    b'\x14\x14\x14\x14\x14\x14' \
    b'\x14\x14\xF7\x00\xF7\x14' \
    b'\x14\x14\x14\x17\x14\x14' \
    b'\x08\x08\x0F\x08\x0F\x08' \
    b'\x14\x14\x14\xF4\x14\x14' \
    b'\x08\x08\xF8\x08\xF8\x08' \
    b'\x00\x00\x0F\x08\x0F\x08' \
    b'\x00\x00\x00\x1F\x14\x14' \
    b'\x00\x00\x00\xFC\x14\x14' \
    b'\x00\x00\xF8\x08\xF8\x08' \
    b'\x08\x08\xFF\x08\xFF\x08' \
    b'\x14\x14\x14\xFF\x14\x14' \
    b'\x08\x08\x08\x0F\x00\x00' \
    b'\x00\x00\x00\xF8\x08\x08' \
    b'\xFF\xFF\xFF\xFF\xFF\xFF' \
    b'\xF0\xF0\xF0\xF0\xF0\xF0' \
    b'\xFF\xFF\xFF\x00\x00\x00' \
    b'\x00\x00\x00\xFF\xFF\xFF' \
    b'\x0F\x0F\x0F\x0F\x0F\x0F' \
    b'\x00\x38\x44\x44\x38\x44' \
    b'\x40\x7C\x02\x4A\x4A\x34' \
    b'\x00\x7F\x01\x01\x01\x01' \
    b'\x04\x7C\x04\x04\x7C\x04' \
    b'\x00\x63\x55\x49\x41\x41' \
    b'\x00\x38\x44\x44\x4C\x34' \
    b'\x00\xFC\x40\x40\x40\x7C' \
    b'\x00\x08\x04\x7C\x08\x04' \
    b'\x00\x1C\x63\x7F\x63\x1C' \
    b'\x00\x3E\x49\x49\x49\x3E' \
    b'\x00\x5E\x61\x01\x61\x5E' \
    b'\x00\x38\x46\x45\x45\x3A' \
    b'\x38\x44\x44\x38\x44\x38' \
    b'\x00\x38\xC4\x7C\x46\x38' \
    b'\x00\x1C\x2A\x49\x49\x00' \
    b'\x00\x7E\x01\x01\x01\x7E' \
    b'\x00\x2A\x2A\x2A\x2A\x2A' \
    b'\x00\x48\x48\x7E\x48\x48' \
    b'\x00\x00\xC1\xA2\x94\x88' \
    b'\x00\x88\x94\xA2\xC1\x00' \
    b'\x00\x00\x00\xFC\x02\x0C' \
    b'\x00\x30\x40\x3F\x00\x00' \
    b'\x00\x08\x08\x2A\x08\x08' \
    b'\x00\x24\x12\x24\x48\x24' \
    b'\x00\x06\x09\x09\x06\x00' \
    b'\x00\x00\x18\x18\x00\x00' \
    b'\x00\x00\x08\x00\x00\x00' \
    b'\x10\x20\x40\xFF\x01\x01' \
    b'\x00\x00\x0F\x02\x01\x0E' \
    b'\x00\x00\x09\x0D\x0A\x00' \
    b'\x00\x3C\x3C\x3C\x3C\x00' \
    b'\x00\x00\x00\x00\x00\x00')