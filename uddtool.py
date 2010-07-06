#!/usr/bin/env python
# -*- coding: Latin-1 -*-

"""UddTool, a PyUdd-based tool for common operations on OllyDbg UDD files.

Ange Albertini 201, Public domain
"""

import glob
import sys

import pyudd

actions = [
    (
    "import",
    "<infile> <outfile>",
    "import user information from a CSV to UDD"
    ),
    (
    "export",
    "<infile>",
    "export user information from a UDD file to a CSV file"
    ),

    # TODO: add different format support in cmdline
    #
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


def rtfm():
    """display usage and exit"""
    usage = ["%s: <action> <arguments>\n" % sys.argv[0]]
    usage += ["actions: "+ ",".join([e[0] for e in actions]), ""]
    for i in actions:
        usage += ["%s %s:" % (i[0], i[1])]
        usage += ["    %s" % i[2], ""]

    usage = "\n".join(usage)

    print usage
    sys.exit()

def ExtractUserData(udd, _format):
    if _format == 11:
        pass
    elif _format == 20:
        pass
def main():
    arglen = len(sys.argv)

    if arglen < 2:
        rtfm()

    action = sys.argv[1].lower()
    if action not in (e[0] for e in actions):
        print "error: invalid action"
        rtfm()

    if action == "create":
        if arglen < 2:
            rtfm()

        uddfile = sys.argv[2]

        # TODO: read format via command line

        _format = 11

        u = pyudd.Udd()
        u.AppendChunk(
            [pyudd.CHUNK_TYPES[_format]["HEADER"],
            pyudd.UDD_FORMATS[_format]]
            )

        if arglen > 3:
            u.AppendChunk(
                [pyudd.CHUNK_TYPES[_format]["FILENAME"], sys.argv[3]]
                )

        u.AppendChunk([pyudd.CHUNK_TYPES[_format]["FOOTER"], ""])
        u.Save(uddfile)

        sys.exit()

    elif action == "list":
        if arglen < 3:
            arg = "*.udd" #if not arg
        else:
            arg = sys.argv[2]

        for f in glob.glob(arg):
            print f
            u = pyudd.Udd(filename=f)
            print u

        sys.exit()

    elif action == "import":
        if arglen < 4:
            rtfm()

        csvfile, uddfile = sys.argv[2], sys.argv[3]

        # loading the UDD file
        #
        f = open(csvfile, "rt")
        u = pyudd.Udd(uddfile)
        _format = u.GetFormat()
        for l in f:

            # skip the header
            #
            if l.startswith("RVA"):
                continue

            # extract information
            #
            d = l.strip().split(",")
            RVA, label, comment  = int(d[0],16), d[1], d[2]

            # save new information
            #
            if label != "":
                u.AddChunk(pyudd.MakeLabelChunk(
                    {"dword":RVA, "text":label}, _format)
                    )
            if comment != "":
                u.AddChunk(pyudd.MakeCommentChunk(
                    {"dword":RVA, "text":comment}, _format)
                    )

        f.close()
        u.Save(uddfile)

        sys.exit()

    elif action == "export":
        if arglen < 3:
            rtfm()
        uddfile = sys.argv[2]

        # loading the UDD file
        #
        u = pyudd.Udd(uddfile)

        # getting all labels or comments chunks
        #
        types = [CHUNK_TYPES[11][e] for e in "U_LABEL", "U_COMMENT"]

        labcoms = u.FindByTypes(types)

        # collecting the information
        #

        # TODO: multi format
        _format = 11

        d = {}
        for i in labcoms:
            ct, cd = u.GetChunk(i)
            RVA, text = pyudd.ExpandChunk([ct, cd], _format)
            if RVA not in d:
                d[RVA] = ["",""]
            if ct == pyudd.CHUNK_TYPES[_format]["U_LABEL"]:
                d[RVA][0] = text
            else:
                d[RVA][1] = text

        # outputting CSV information
        #
        print "RVA,label,comment"
        for i in d:
            print "%08x,%s" % (i, ",".join(d[i]))

        sys.exit()

if __name__ == '__main__':
    main()
