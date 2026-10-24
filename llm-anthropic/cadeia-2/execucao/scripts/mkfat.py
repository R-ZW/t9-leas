# uso: python3 mkfat.py <saida> <thin1> <thin2>   (universal binary, alinhamento 2^14)
import struct, sys
out, *thins = sys.argv[1:]; datas = [open(p,'rb').read() for p in thins]
A = 1 << 14; off = A; ent = b''; lay = []
for d in datas:
    cpu, sub = struct.unpack('<ii', d[4:12])
    ent += struct.pack('>iiIII', cpu, sub, off, len(d), 14); lay.append((off, d))
    off += (len(d) + A - 1) // A * A
buf = bytearray(lay[-1][0] + len(lay[-1][1]))
hdr = struct.pack('>II', 0xCAFEBABE, len(datas)) + ent; buf[:len(hdr)] = hdr
for o, d in lay: buf[o:o+len(d)] = d
open(out, 'wb').write(bytes(buf))
