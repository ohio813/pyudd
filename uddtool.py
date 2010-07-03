#!/usr/bin/env python

# small pyudd based tool.
#
# Ange Albertini 2010
# Public domain

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

    # TODO: add different format support
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

    usage = ["%s: <action> <arguments>\n" % sys.argv[0]]
    usage += ["actions: "+ ",".join([e[0] for e in actions]), ""]
    for i in actions:
        usage += ["%s %s:" % (i[0], i[1])]
        usage += ["    %s" % i[2], ""]

    usage = "\n".join(usage)

    print usage
    sys.exit()

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

    u = pyudd.Udd()
    u.AppendChunk([pyudd.CHUNK_TYPES["HEADER"], "Module info file v1.1\x00"])

    if arglen > 3:
        u.AppendChunk([pyudd.CHUNK_TYPES["FILENAME"], sys.argv[3]])

    u.AppendChunk([pyudd.CHUNK_TYPES["FOOTER"], ""])
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
        u.Render()
        print

    sys.exit()

elif action == "import":
    if arglen < 4:
        rtfm()

    csvfile, uddfile = sys.argv[2], sys.argv[3]

    # loading the UDD file
    #
    f = open(csvfile, "rt")
    u = pyudd.Udd(uddfile)
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
            u.AppendChunk(pyudd.MakeLabelChunk(RVA, label))
        if comment != "":
            u.AppendChunk(pyudd.MakeCommentChunk(RVA, comment))

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
    labcoms = u.FindByTypes(pyudd.RVAINFO_TYPES)

    # collecting the information
    #
    d = {}
    for i in labcoms:
        ct, cd = u.GetChunk(i)
        RVA, text = pyudd.ReadInfo([ct, cd])
        if RVA not in d:
            d[RVA] = ["",""]
        if ct == pyudd.CHUNK_TYPES["U_LABEL"]:
            d[RVA][0] = text
        else:
            d[RVA][1] = text

    # outputting CSV information
    #
    print "RVA,label,comment"
    for i in d:
        print "%08x,%s" % (i, ",".join(d[i]))

    sys.exit()
