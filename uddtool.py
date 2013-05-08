# -*- coding: Latin-1 -*-
#!/usr/bin/env python

"""UddTool, a PyUdd-based tool for common operations on OllyDbg UDD files.

Ange Albertini 2010-2013, Public domain
"""

import glob
import struct
import sys
import collections
import csv

import pyudd

actions = [
    (
    "import",
    "<infile> <outfile>",
    "import label and comments from a CSV to UDD"
    ),
    (
    "export",
    "<infile>",
    "export label and comments from a UDD file to a CSV file"
    ),
    (
    "extract",
    "<infile>",
    "extract user-entered information from a UDD file"
    ),
    (
    "create",
    "<outfile> [<targetfile>]",
    "create an empty UDD [referencing <targetfile>]"
    ),
    (
    "list",
    "[<filemask>]",
    "list the structure of (a) UDD file(s)",
    )
    ]

class StdoutWriter:
    def write(self, row):
        sys.stdout.write(row)

def rtfm():
    """display usage and exit"""
    usage = ["%s: <action> <arguments>\n" % sys.argv[0]]
    usage += ["actions: "+ ",".join([e[0] for e in actions]), ""]
    for i in actions:
        usage += ["%s %s:" % (i[0], i[1])]
        usage += ["    %s" % i[2], ""]

    print "\n".join(usage)
    sys.exit()


def extract_user_data(udd, format_):
    """extract user-entered MRUs from a UDD"""
    results = [",".join(["type", "text"])]
    if format_ == 11:
        found = udd.find_by_types(
            [pyudd.CHUNK_TYPES[11][i]
                for i in pyudd.CHUNK_TYPES[11]
                    if i.startswith("MRU_")])
        for i in found:
            chk = udd.get_chunk(i)
            type_ = pyudd.CHUNK_TYPES[11][chk[0]]
            text = pyudd.expand_chunk(chk, format_)["text"]
            results += [",".join([type_, text])]

    elif format_ == 20:
        for i in udd.find_by_types(
            [pyudd.CHUNK_TYPES[20][i]
                for i in ["Name", "LSA"]]):
            data = pyudd.expand_chunk(udd.get_chunk(i), format_)
            if data["category"] in  [
                'd', 'e', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'Y', 'Z', '[', '`', 'a', 'c'
                ]:
                type_ = pyudd.OLLY2CATS[data["category"]]
                text = data["name"]

                results += [",".join([type_, text])]

    print "\n".join(results)
    return

def export_labcoms(udd):
    """export labels and comments of a Udd as a CSV list"""
    # loading the UDD file
    #
    u = pyudd.Udd(udd)
    format_ = u.get_format()

    # getting all labels or comments chunks
    #
    types = [pyudd.CHUNK_TYPES[11][e] for e in "U_LABEL", "U_COMMENT"]

    labcoms = u.find_by_types(types)

    # collecting the information
    #

    #TODO: multi format
    format_ = 11

    d = collections.OrderedDict()
    for i in labcoms:
        ct, cd = u.get_chunk(i)

        data = pyudd.expand_chunk([ct, cd], format_)
        RVA, text = data["dword"], data["text"]
        if RVA not in d:
            d[RVA] = ["",""]
        if ct == pyudd.CHUNK_TYPES[format_]["U_LABEL"]:
            d[RVA][0] = text
        else:
            d[RVA][1] = text

    # outputting CSV information
    csvwriter = csv.writer(StdoutWriter())
    csvwriter.writerow(["RVA", "label", "comment"])

    for i in d:
        csvwriter.writerow(["%08X" % i, d[i][0], d[i][1]])

def main():
    """parse arguments then call relevant function"""
    arglen = len(sys.argv)

    if arglen < 2:
        rtfm()

    action = sys.argv[1].lower()
    if action not in (e[0] for e in actions):
        print "error: invalid action"
        rtfm()

    if action == "create":
        #TODO: turn that into a procedure
        if arglen < 2:
            rtfm()

        uddfile = sys.argv[2]

        #TODO: cleaner parameter reading
        format_ = 20 if "-O2" in sys.argv else 11

        u = pyudd.Udd()
        u.append_chunk([pyudd.HDR_STRING, pyudd.UDD_FORMATS[format_]])

        if arglen > 3:
            filename = sys.argv[3]
            time_, crc, size = pyudd.getFileInfo(filename)

            u.append_chunk(
                [pyudd.CHUNK_TYPES[format_]["Filename"], sys.argv[3]]
                )

            #TODO: QA for format 20
            u.append_chunk(
                [pyudd.CHUNK_TYPES[format_]["Size"], struct.pack("<I", size)]
                )
            u.append_chunk(
                [pyudd.CHUNK_TYPES[format_]["Timestamp"], time_]
                )
            u.append_chunk(
                [pyudd.CHUNK_TYPES[format_]["CRC"], struct.pack("<I", crc)]
                )

        u.append_chunk([pyudd.FTR_STRING, ""])
        u.save(uddfile)

        sys.exit()

    elif action == "list":
        #TODO: turn that into a procedure
        if arglen < 3:
            arg = "*.udd" #if not arg
        else:
            arg = sys.argv[2]

        for f in glob.glob(arg):
            print f
            u = pyudd.Udd(filename=f)
            print u

# old scanning code
#            chk = u.get_chunk(u.find_by_type(pyudd.CHUNK_TYPES[11]["CRC"])[0])
#            intCRC = pyudd.expand_chunk(chk,11)["dword"][0]
#
#            filename = u.get_chunk(u.find_by_type(pyudd.CHUNK_TYPES[11]["Filename"])[0])[1]
#            try:
#                myCRC = pyudd.getcrc(filename.strip('\0'))
#                print "OK" if myCRC == intCRC else "Error"
#            except IOError:
#                pass

    elif action == "import":
        #TODO: turn that into a procedure
        if arglen < 4:
            rtfm()

        csvfile, uddfile = sys.argv[2], sys.argv[3]

        # loading the UDD file
        #
        f = open(csvfile, "rt")
        u = pyudd.Udd(uddfile)
        csvreader = csv.reader(f)
        format_ = u.get_format()

        for d in csvreader:
            # skip the header
            #
            if d[0] == "RVA":
                continue

            # extract information
            #
            RVA, label, comment  = int(d[0],16), d[1], d[2]

            # save new information
            #
            if label != "":
                u.add_chunk(pyudd.make_label_chunk(
                    {"dword":RVA, "text":label}, format_)
                    )
            if comment != "":
                u.add_chunk(pyudd.make_comment_chunk(
                    {"dword":RVA, "text":comment}, format_)
                    )

        f.close()
        u.save(uddfile)

    elif action == "export":
        if arglen < 3:
            rtfm()
        uddfile = sys.argv[2]
        export_labcoms(uddfile)

    elif action == "extract":
        if arglen < 3:
            rtfm()
        uddfile = sys.argv[2]

        # loading the UDD file
        #
        u = pyudd.Udd(uddfile)

        extract_user_data(u, u.get_format())


if __name__ == '__main__':
    main()
