#!/usr/bin/env python

# a python module to manage OllyDbg .UDD files
#
# Ange Albertini 2010
# Public domain

__author__ = 'Ange Albertini'
__contact__ = 'ange@corkami.com'
__revision__ = "$Revision$"
__version__ = '0.1 r%d' % int(__revision__[11:-2])

import struct

F_STRING = 0
F_DDSTRING = 1
F_EMPTY = 2
F_VERSION = 3
F_DWORD = 4
F_DD2 = 5
F_DD2STRING = 6
F_BIN = 8
F_NAME = 9

# TODO: support both formats

chunk_types1 = [
    ("HEADER",      "Mod\x00", F_STRING),
    ("FOOTER",      "\nEnd", F_EMPTY),
    ("FILENAME",    "\nFil", F_STRING),
    ("VERSION",     "\nVer", F_VERSION),
    ("SIZE",        "\nSiz", F_DWORD),
    ("TIMESTAMP",   "\nTst", F_DD2),
    ("CRC",         "\nCcr", F_DWORD),
    ("PATCH",       "\nPat", F_BIN),
    ("=BPc",        "\nBpc", F_BIN),
    ("=BPt",        "\nBpt", F_BIN),
    ("=HWBP",       "\nHbr", F_BIN),
    ("SAVE",        "\nSva", F_BIN), # sometimes 4, sometimes 5 ?
    ("ANALYSEHINT", "\nAht", F_BIN),

    ("CMD_PLUGINS", "\nUs0", F_DDSTRING),
    ("USERLABEL",   "\nUs1", F_BIN),
    ("U_LABEL",     "\nUs1", F_DDSTRING),
    ("US2",         "\nUs2", F_BIN),
    ("US3",         "\nUs3", F_BIN),
    ("A_LABEL",     "\nUs4", F_DDSTRING),
    ("_CONST",      "\nUs5", F_BIN),
    ("U_COMMENT",   "\nUs6", F_DDSTRING),
    ("A_COMMENT",   "\nUs7", F_BIN),
    ("BPCOND",      "\nUs8", F_DDSTRING),
    ("KNOWN_ARG",   "\nUs9", F_DDSTRING),
    ("WATCH",       "\nUsA", F_DDSTRING),
    ("FIND?",       "\nUsC", F_BIN),
    ("SOURCE?",     "\nUsI", F_BIN),


    ("MRU_INSPECT","\nUs@", F_DDSTRING),
    ("MRU_ASM",    "\nUsB", F_DDSTRING),
    ("MRU_GOTO",   "\nUsK", F_DDSTRING), #?
    ("MRU_EXPL",   "\nUs|", F_DDSTRING), # logging breakpoint explanation
    ("MRU_EXPR",   "\nUs{", F_DDSTRING), # logging breakpoint expression
    ("MRU_WATCH",  "\nUsH", F_DDSTRING),
    ("MRU_LABEL",  "\nUsq", F_DDSTRING), #?
    ("MRU_COMM",   "\nUsv", F_DDSTRING), #?
    ("MRU_COND",   "\nUsx", F_DDSTRING), #?
    ("MRU_CMDLINE","\nCml", F_STRING), #?


    ("EXPR",        "\nUs;", F_DDSTRING), # logging breakpoint expression
    ("ANALY_COMM",  "\nUs:", F_DDSTRING), #
    ("US?",         "\nUs?", F_DDSTRING), #?
    ("US>",         "\nUs>", F_BIN), #?
    ("TRACCOND",    "\nUsM", F_DDSTRING), # tracing condition
    ("LOGEXP",      "\nUs<", F_DDSTRING), # logging breakpoint explanation
    ("ASSARG",      "\nUs=", F_DDSTRING), # Assumed arguments
    ("ANC",         "\nAnc", F_BIN), #?

    ("CFA",         "\nCfa", F_DD2), #?
    ("CFM",         "\nCfm", F_DD2STRING), #?
    ("CFI",         "\nCfi", F_DD2), #?
    ]

chunk_types = [
    ("HEADER",      "Mod\x00", F_STRING),
    ("FOOTER",      "\nEnd", F_EMPTY),
    ("FILENAME",    "\nFil", F_STRING),

    ("JDT",         "\nJdt", F_BIN), #?
    ("PRC",         "\nPrc", F_BIN), #?
    ("SWI",         "\nSwi", F_BIN), #?

     #OllyDbg 2
    ("FCR",         "\nFcr", F_BIN), #?
    ("NAME",        "\nNam", F_NAME), #?
    ("DATA",        "\nDat", F_NAME), #?
    ("CBR",         "\nCbr", F_BIN), #?
    ("LBR",         "\nLbr", F_BIN), #?
    ("ANA",         "\nAna", F_BIN), #?
    ("CAS",         "\nCas", F_BIN), #?
    ("MBA",         "\nMba", F_DDSTRING), #?
    ("PRD",         "\nPrd", F_BIN), #?
    ("SAV",         "\nSav", F_BIN), #?
    ("RTC",         "\nRtc", F_BIN), #?
    ("RTP",         "\nRtp", F_BIN), #?
    ("LSA",         "\nLsa", F_NAME), #?
    ("IN3",         "\nIn3", F_BIN), #?
    ("BPM",         "\nBpm", F_BIN), #?
    ("BPH",         "\nBph", F_BIN), #?
    ]

CHUNK_TYPES = dict(
    [(e[1], e[0]) for e in chunk_types] +
    [(e[0], e[1]) for e in chunk_types]
    )

CHUNK_FORMATS = dict(
    [(e[2], e[0]) for e in chunk_types] +
    [(e[0], e[2]) for e in chunk_types]
    )

#RVAINFO_TYPES = [CHUNK_TYPES[e] for e in "U_LABEL", "U_COMMENT"]

def binstr(s):
    """binary rendering"""
    return " ".join(["%02X" % ord(c) for c in s])

def elbinstr(s):
    """ellipsed binary string display"""
    if len(s) < 10:
        return binstr(s)
    return "%s ... %s" % (binstr(s[:10]), binstr(s[-10:]))

def ReadNextChunk(f):
    ct = f.read(4)
    size = struct.unpack("<I", f.read(4))[0]
    cd = f.read(size)

    return ct, cd


def WriteChunk(f, ct, cd):
    f.write(ct)
    f.write(struct.pack("<I", len(cd)))
    f.write(cd)
    return


def MakeChunk(ct, cd):
    if len(ct) != 4:
        raise Exception("invalid chunk name length")
    if len(cd) > 255:
        raise Exception("invalid chunk data length")

    return [ct, cd]

# TODO: merge those 3 into a real MakeChunk or something - support format 2
#

def MakeRVAInfo(RVA, comment):
    return "%s%s\x00" % (struct.pack("<I", RVA), comment)


def MakeCommentChunk(RVA, comment):
    return MakeChunk(CHUNK_TYPES["U_COMMENT"], MakeRVAInfo(RVA, comment))


def MakeLabelChunk(RVA, comment):
    return MakeChunk(CHUNK_TYPES["U_LABEL"], MakeRVAInfo(RVA, comment))

# TODO: rename ReadInfo
#
def ReadInfo(chunk):
    ct, cd = chunk
    if ct not in CHUNK_TYPES:
        return cd

    cf = CHUNK_FORMATS[CHUNK_TYPES[ct]]
    if cf == F_STRING:
        return cd
    elif cf == F_DDSTRING:
        return [struct.unpack("<I", cd[:4])[0], cd[4:]]

    elif cf == F_NAME:
        #name can be null, no 00 in that case
        #if lptype is not present then no type
        RVA, buffer = cd[:4], cd[4:]
        RVA = struct.unpack("<I", RVA)[0]
        buffer = buffer.rstrip("\x00")

        result = {"RVA": RVA, "cat": buffer[0]}

        buffer = buffer[1:]

        for i, c in enumerate(buffer):
            if ord(c) >= 0x80:
                found = i
                break
        else:
            name = buffer
            if len(buffer):
                result["name"] = buffer
            return result

        name, lptype, _type = buffer[:found], buffer[found], buffer[found + 1:]

        # should be in rendering ?
        #
        name = name.rstrip("\x00")
        if len(name):
            result["name"] = name

        # should be in rendering
        #
        result["lptype"] = "*" if lptype == "\xa0" else "%i" % ord(lptype)

        result["type"] = _type

        return result


    elif cf == F_DD2STRING:
        return list(struct.unpack("<2I", cd[:8])) + [cd[8:].rstrip("\x00")]

    elif cf == F_EMPTY:
        return ""
    elif cf == F_VERSION:
        return struct.unpack("<4I", cd)
    elif cf == F_DWORD:
        print len(cd),
        return struct.unpack("<I", cd)
    elif cf == F_DD2:
        return struct.unpack("<2I", cd)
    elif cf == F_BIN:
        return cd
    else:
        return cd

# TODO: rename Render
#
def RenderInfo(chunk):
    ct, cd = chunk
    info = ReadInfo(chunk)
    if ct not in CHUNK_TYPES:
        return elbinstr(info)

    cf = CHUNK_FORMATS[CHUNK_TYPES[ct]]

    if cf == F_STRING:
        return info.rstrip("\x00")

    elif cf == F_DDSTRING:
        return "%08X: %s" % (info[0], info[1].rstrip("\x00"))

    elif cf == F_NAME:
        result = ["%(RVA)08X: cat:%(cat)s" % info]

        if "name" in info:
            result += ["name:%(name)s" % info]
        if "type" in info:
            result += ["type:%(lptype)s %(type)s" % info]

        return " ".join(result)

    elif cf == F_DD2STRING:
        return "%08X %08X %s" % tuple(info)

    elif cf == F_EMPTY:
        return ""

    elif cf == F_VERSION:
        return "%i.%i.%i.%i" % info

    elif cf == F_DWORD:
        return "%08X" % info

    elif cf == F_DD2:
        return "%08X %08X" % info

    elif cf == F_BIN:
        return elbinstr(info)
    return cd

class Udd(object):

    def __init__(self, filename=None):
        self.__data = {}
        self.__chunks = []
        self.__format = None
        self.__warnings = []

        if filename is not None:
            self.Load(filename)

        return

    def Load(self, filename):
        try:
            f = open(filename, "rb")
            ct, cd =  ReadNextChunk(f)

            if not (ct == CHUNK_TYPES["HEADER"] and
                cd in [
                    "Module info file v1.1\x00",
                    "Module info file v2.0\x00"]):
                raise Exception("Invalid HEADER chunk")
            self.__chunks.append([ct, cd])
            self.__format = 1 if cd == "Module info file v1.1\x00" else 2
            while (True):
                ct, cd = ReadNextChunk(f)
                if ct not in CHUNK_TYPES:
                    self.__warnings.append(
                        "Warning (offset %08X) unknown chunk type: '%s' %s" % (f.tell(), ct.lstrip("\n"), elbinstr(cd))
                        )

                self.__chunks.append([ct, cd])
                if (ct, cd) == (CHUNK_TYPES["FOOTER"] , ""):
                    break

        finally:
            f.close()

        for w in self.__warnings:
            print w
        return


    def Save(self, filename):
        f = open(filename, "wb")
        for ct, cd in self.__chunks:
            WriteChunk(f, ct, cd)
        f.close()
        return


    def SetChunk(self, pos, chunk):
        self.__chunks[pos] = chunk
        return


    def GetChunk(self, pos):
        return self.__chunks[pos]


    def AddChunk(self, chunk):
        """appending the chunk before the final End chunk"""
        if not self.Find(chunk):
            self.__chunks.insert(-1, chunk)
        return

    def AppendChunk(self, chunk):
        """blindly the chunk"""
        self.__chunks.append(chunk)
        return

    def GetFormat(self):
        return self.__format


    def FindByType(self, type):
        found = []

        for i, c in enumerate(self.__chunks):
            if c[0] == type:
                found += i

        return found


    def FindByTypes(self, types):
        found = []

        for i, c in enumerate(self.__chunks):
            if c[0] in types:
                found += [i]

        return found


    def Find(self, chunk):
        found = []

        for i, c in enumerate(self.__chunks):
            if c == chunk:
                found += [i]

        return found if len(found) > 0 else None


    def FindByRVA(self, RVA):
        found = self.FindByTypes(RVAINFO_TYPES)

        result = []
        for i in found:
            foundRVA, data = ReadRVAInfo(self.__chunks[i][1])
            if foundRVA == RVA:
                type = CHUNK_TYPES[self.__chunks[i][0]]
                result += type, data

        return result


    def Render(self):
        for i in self.__chunks:
            if i[0] in CHUNK_TYPES:
                print "%s:" % CHUNK_TYPES[i[0]],
            else:
                print "UNK[%s] :" % i[0][1:4],
            print RenderInfo(i)
        return
