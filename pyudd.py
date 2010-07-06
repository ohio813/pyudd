# -*- coding: Latin-1 -*-
#!/usr/bin/env python

"""PyUdd, a python module for OllyDbg .UDD files

Ange Albertini 2010 Public domain
"""

__author__ = 'Ange Albertini'
__contact__ = 'ange@corkami.com'
__revision__ = "$Revision$"
__version__ = '0.1 r%d' % int(__revision__[11:-2])

import struct

format_ids = [
    "STRING",
    "DDSTRING",
    "MRUSTRING",
    "EMPTY",
    "VERSION",
    "DWORD",
    "DD2",
    "DD2STRING",
    "BIN",
    "NAME",
    "CRC2",
    ]

F_ = dict([(e, i) for i, e in enumerate(format_ids)])

udd_formats = [
    (11, "Module info file v1.1\x00"),
    (20, "Module info file v2.0\x00"),
    ]

UDD_FORMATS = dict(
    [(e[1], e[0]) for e in udd_formats] +
    udd_formats)

HDR_STRING = "Mod\x00"

#OllyDbg 1.1
chunk_types11 = [
    ("Header", HDR_STRING, F_["STRING"]),
    ("Footer", "\nEnd", F_["EMPTY"]),
    ("Filename", "\nFil", F_["STRING"]),
    ("Version", "\nVer", F_["VERSION"]),
    ("Size", "\nSiz", F_["DWORD"]),
    ("Timestamp", "\nTst", F_["DD2"]),
    ("CRC", "\nCcr", F_["DWORD"]),
    ("Patch", "\nPat", F_["BIN"]),
    ("Bpc", "\nBpc", F_["BIN"]),
    ("Bpt", "\nBpt", F_["BIN"]),
    ("HwBP", "\nHbr", F_["BIN"]),
    ("Save", "\nSva", F_["BIN"]), # sometimes 4, sometimes 5 ?
    ("AnalyseHint", "\nAht", F_["BIN"]),

    ("CMD_PLUGINS", "\nUs0", F_["DDSTRING"]), # multiline, needs escaping
    ("U_LABEL", "\nUs1", F_["DDSTRING"]),
    ("A_LABEL", "\nUs4", F_["DDSTRING"]),
    ("U_COMMENT", "\nUs6", F_["DDSTRING"]),
    ("BPCOND", "\nUs8", F_["DDSTRING"]),
    ("ApiArg", "\nUs9", F_["DDSTRING"]),
    ("USERLABEL", "\nUs1", F_["DDSTRING"]),
    ("Watch", "\nUsA", F_["DDSTRING"]),

    ("US2", "\nUs2", F_["BIN"]),
    ("US3", "\nUs3", F_["BIN"]),
    ("_CONST", "\nUs5", F_["BIN"]),
    ("A_COMMENT", "\nUs7", F_["BIN"]),
    ("FIND?", "\nUsC", F_["BIN"]),
    ("SOURCE?", "\nUsI", F_["BIN"]),


    ("MRU_Inspect","\nUs@", F_["MRUSTRING"]),
    ("MRU_Asm", "\nUsB", F_["MRUSTRING"]),
    ("MRU_Goto", "\nUsK", F_["MRUSTRING"]), #?
    ("MRU_Explanation", "\nUs|", F_["MRUSTRING"]), # logging bp explanation
    ("MRU_Expression", "\nUs{", F_["MRUSTRING"]), # logging bp expression
    ("MRU_Watch", "\nUsH", F_["MRUSTRING"]),
    ("MRU_Label", "\nUsq", F_["MRUSTRING"]), #?
    ("MRU_Comment", "\nUsv", F_["MRUSTRING"]), #?
    ("MRU_Condition", "\nUsx", F_["MRUSTRING"]), #?

    ("MRU_CMDLine", "\nCml", F_["STRING"]), #?


    ("LogExpression", "\nUs;", F_["DDSTRING"]), # logging bp expression
    ("ANALY_COMM", "\nUs:", F_["DDSTRING"]), #
    ("US?", "\nUs?", F_["DDSTRING"]), #?
    ("TracCond", "\nUsM", F_["DDSTRING"]), # tracing condition
    ("LogExplanation", "\nUs<", F_["DDSTRING"]), # logging bp explanation
    ("AssumedArgs", "\nUs=", F_["DDSTRING"]), # Assumed arguments
    ("CFA", "\nCfa", F_["DD2"]), #?
    ("CFM", "\nCfm", F_["DD2STRING"]), #?
    ("CFI", "\nCfi", F_["DD2"]), #?

    ("US>", "\nUs>", F_["BIN"]), #?
    ("ANC", "\nAnc", F_["BIN"]), #?
    ("JDT", "\nJdt", F_["BIN"]), #?
    ("PRC", "\nPrc", F_["BIN"]), #?
    ("SWI", "\nSwi", F_["BIN"]), #?
    ]

#OllyDbg 2
chunk_types20 = [
    ("Header", HDR_STRING, F_["STRING"]),
    ("Footer", "\nEnd", F_["EMPTY"]),
    ("Filename", "\nFil", F_["STRING"]),

    ("Infos", "\nFcr", F_["CRC2"]), #?
    ("Name", "\nNam", F_["NAME"]), #?
    ("Data", "\nDat", F_["NAME"]), #?
    ("MemMap", "\nMba", F_["DDSTRING"]), #?

    ("LSA", "\nLsa", F_["NAME"]), # MRU entries

    ("JDT", "\nJdt", F_["BIN"]), #?
    ("PRC", "\nPrc", F_["BIN"]), #?
    ("SWI", "\nSwi", F_["BIN"]), #?

    ("CBR", "\nCbr", F_["BIN"]), #?
    ("LBR", "\nLbr", F_["BIN"]), #?
    ("ANA", "\nAna", F_["BIN"]), #?
    ("CAS", "\nCas", F_["BIN"]), #?
    ("PRD", "\nPrd", F_["BIN"]), #?
    ("Save", "\nSav", F_["BIN"]), #?
    ("RTC", "\nRtc", F_["BIN"]), #?
    ("RTP", "\nRtp", F_["BIN"]), #?
    ("Int3", "\nIn3", F_["BIN"]), #?
    ("MemBP", "\nBpm", F_["BIN"]), #?
    ("HWBP", "\nBph", F_["BIN"]), #?
    ]

CHUNK_TYPES11 = dict(
    [(e[1], e[0]) for e in chunk_types11] +
    [(e[0], e[1]) for e in chunk_types11]
    )

CHUNK_TYPES20 = dict(
    [(e[1], e[0]) for e in chunk_types20] +
    [(e[0], e[1]) for e in chunk_types20]
    )

CHUNK_TYPES = {
    11: CHUNK_TYPES11,
    20: CHUNK_TYPES20
    }

# no overlapping of formats yet so they're still merged
#
CHUNK_FORMATS = dict(
    [(e[2], e[0]) for e in chunk_types11] +
    [(e[0], e[2]) for e in chunk_types11] +

    [(e[2], e[0]) for e in chunk_types20] +
    [(e[0], e[2]) for e in chunk_types20]
    )

olly2cats = [
    # used in DATA and NAME
    #
    ('!', "UserLabel"),
    ('0', "UserComment"),
    ('1', "Import"),
    ('2', "APIArg"),
    ('3', "APICall"),
    ('4', "Member"),
    ('6', "Unk6"),
    ('*', "Struct"),

    # only used in LSA ?
    #
    ('`', 'mru_label'),
    ('a', 'mru_asm'),
    ('c', 'mru_comment'),
    ('d', 'watch'),
    ('e', 'mru_goto'),

    ('p', 'trace_condition1'),
    ('q', 'trace_condition2'),
    ('r', 'trace_condition3'),
    ('s', 'trace_condition4'),
    ('t', 'trace_command1'),
    ('u', 'trace_command2'),

    ('v', 'protocol_start'),
    ('w', 'protocol_end'),

    ('Q', 'log_explanation'),
    ('R', 'log_condition'),
    ('S', 'log_expression'),

    ('U', 'mem_explanation'),
    ('V', 'mem_condition'),
    ('W', 'mem_expression'),

    ('Y', 'hbplog_explanation'),
    ('Z', 'hbplog_condition'),
    ('[', 'hbplog_expression'),

    ]

OLLY2CATS = dict(
    [(e[1], e[0]) for e in olly2cats] +
    olly2cats)

del(e, i)


def binstr(s):
    """binary rendering"""
    return " ".join(["%02X" % ord(c) for c in s])

def elbinstr(s):
    """ellipsed binary string display"""
    if len(s) < 10:
        return binstr(s)
    return "(%i) %s ... %s" % (len(s), binstr(s[:10]), binstr(s[-10:]))

class Error(Exception):
    """custom error class"""
    pass


def ReadNextChunk(f):
    """read next Udd chunk"""
    ct = f.read(4)
    size = struct.unpack("<I", f.read(4))[0]
    cd = f.read(size)

    return ct, cd


def WriteChunk(f, ct, cd):
    """write a chunk"""
    f.write(ct)
    f.write(struct.pack("<I", len(cd)))
    f.write(cd)
    return


def MakeChunk(ct, cd):
    """put together chunk types and data with a few checks"""
    if len(ct) != 4:
        raise Error("invalid chunk name length")
    if len(cd) > 255:
        raise Error("invalid chunk data length")

    return [ct, cd]


def BuildData(_format, info):
    """generate a chunk data depending on the format"""
    if _format == F_["DWORD"]:
        return "%s" % (struct.pack("<I", info["dword"]))
    if _format in [F_["DDSTRING"], F_["MRUSTRING"]]:
        return "%s%s\x00" % (struct.pack("<I", info["dword"]), info["text"])
    else:
        raise Error("format not supported for building")


# TODO: merge those 3 into a real MakeChunk or something - support format 2
#
def MakeCommentChunk(info, _format):
    """generate a user comment chunk depending on the format"""
    if _format == 11:
        return MakeChunk(
            CHUNK_TYPES[_format]["U_COMMENT"],
            BuildData(CHUNK_FORMATS["U_LABEL"], info)
            )
    else:
        raise Error("Not supported")

def MakeLabelChunk(info, _format):
    """generate a user label chunk depending on the format"""
    if _format == 11:
        return MakeChunk(
            CHUNK_TYPES[_format]["U_LABEL"],
            BuildData(CHUNK_FORMATS["U_LABEL"], info)
            )

    else:
        raise Error("Not supported")

def ExpandChunk(chunk, _format):
    """Extract information from the chunk data"""

    ct, cd = chunk
    if ct not in CHUNK_TYPES[_format]:
        return cd

    cf = CHUNK_FORMATS[CHUNK_TYPES[_format][ct]]
    if cf == F_["STRING"]:
        result = {"string": cd}

    elif cf in [F_["DDSTRING"], F_["MRUSTRING"]]:
        result = {
            "dword": struct.unpack("<I", cd[:4])[0],
            "text": cd[4:].rstrip("\x00").encode('string-escape')
            }

    elif cf == F_["NAME"]:
        #name can be null, no 00 in that case
        #if lptype is not present then no type
        RVA = cd[:4]
        _buffer = cd[4:]
        RVA = struct.unpack("<I", RVA)[0]
        _buffer = _buffer.rstrip("\x00")

        result = {"RVA": RVA, "category": _buffer[0]}

        _buffer = _buffer[1:]

        for i, c in enumerate(_buffer):
            if ord(c) >= 0x80:
                found = i
                break
        else:
            name = _buffer
            if _buffer:
                result["name"] = _buffer
            return result

        name = _buffer[:found]
        lptype = _buffer[found]
        _type = _buffer[found + 1:]

        # should be in rendering ?
        #
        name = name.rstrip("\x00")
        if name:
            result["name"] = name

        # should be in rendering ?
        #
        result["lptype"] = "*" if lptype == "\xa0" else "%i" % ord(lptype)

        result["type"] = _type

    elif cf == F_["DD2STRING"]:
        result = list(struct.unpack("<2I", cd[:8])) + [cd[8:].rstrip("\x00")]
    elif cf == F_["EMPTY"]:
        result = None
    elif cf == F_["CRC2"]:
        dwords = struct.unpack("<4I", cd)
        result = {
            "size":dwords[0],
            "timestamp": " ".join("%08X" % e for e in (dwords[1:3])),
            "unk": dwords[3]
            }
    elif cf == F_["VERSION"]:
        result = {"version":struct.unpack("<4I", cd)}
    elif cf == F_["DWORD"]:
        result = {"dword": struct.unpack("<I", cd)}
    elif cf == F_["DD2"]:
        result = {"dwords": struct.unpack("<2I", cd)}
    elif cf == F_["BIN"]:
        result = {"binary": cd}
    else:
        result = cd
    return result


def PrintChunk(chunk, _format):
    """Pretty print chunk data after expansion"""

    ct, cd = chunk
    info = ExpandChunk(chunk, _format)
    if ct not in CHUNK_TYPES[_format]:
        return elbinstr(info)

    cf = CHUNK_FORMATS[CHUNK_TYPES[_format][ct]]

    if cf == F_["STRING"]:
        result = info["string"].rstrip("\x00")

    elif cf == F_["DDSTRING"]:
        result = "%(dword)08X %(text)s" % (info)

    elif cf == F_["MRUSTRING"]:
        result = "%(dword)i %(text)s" % (info)

    elif cf == F_["NAME"]:
        if info["category"] in OLLY2CATS:
            info["category"] = OLLY2CATS[info["category"]]
        result = ["%(RVA)08X (%(category)s)" % info]

        if "name" in info:
            result += ["%(name)s" % info]
        if "type" in info:
            result += ["type:%(lptype)s %(type)s" % info]

        result = " ".join(result)

    elif cf == F_["DD2STRING"]:
        result = "%08X %08X %s" % tuple(info)

    elif cf == F_["EMPTY"]:
        result = ""

    elif cf == F_["CRC2"]:
        result = "Size: %(size)i Time:%(timestamp)s unk:%(unk)08X" % info

    elif cf == F_["VERSION"]:
        result = "%i.%i.%i.%i" % info["version"]

    elif cf == F_["DWORD"]:
        result = "%08X" % info["dword"]

    elif cf == F_["DD2"]:
        result = "%08X %08X" % info["dwords"]

    elif cf == F_["BIN"]:
        result = elbinstr(info["binary"])
    else:
        result = cd
    return result


class Udd(object):

    def __init__(self, filename=None, _format=None):

        self.__data = {}
        self.__chunks = []
        self.__warnings = []

        self.__format = 11 if _format is None else _format

        if filename is not None:
            self.Load(filename)
        return


    def Load(self, filename):
        try:
            f = open(filename, "rb")
            ct, cd =  ReadNextChunk(f)

            if not (ct == HDR_STRING and
                cd in (e[1] for e in udd_formats)):
                raise Error("Invalid HEADER chunk")

            self.__format = UDD_FORMATS[cd]

            self.__chunks.append([ct, cd])
            while (True):
                ct, cd = ReadNextChunk(f)

                if ct not in CHUNK_TYPES[self.__format]:
                    self.__warnings.append(
                        "Warning (offset %08X) unknown chunk type: '%s' %s" %
                            (f.tell(), ct.lstrip("\n"), elbinstr(cd))
                        )
                self.__chunks.append([ct, cd])
                if (ct, cd) == (CHUNK_TYPES[self.__format]["Footer"] , ""):
                    break

        finally:
            f.close()
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
        """blindly append the chunk"""
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
        return found if found else None


    def __repr__(self):
        r = []
        for i in self.__chunks:
            if i[0] in CHUNK_TYPES[self.__format]:
                s = ["%s:" % CHUNK_TYPES[self.__format][i[0]]]
            else:
                s = ["UNK[%s]:" % i[0][1:4]]
            s += [PrintChunk(i, self.__format)]
            r += ["".join(s)]
        return "\n".join(r)

