_PyUdd_ is a python module to manage (read/write) [OllyDbg](http://www.ollydbg.de/) .UDD files.

.UDD is the file format that OllyDbg uses to store information, like analysis, breakpoints, comments... It's automatically generated whenever you open a file in OllyDbg.

a simple script (_uddtool_) is included, for easy access to standard uses:
  * export comments, labels, MRUs... from a .UDD (ex: you spent a long time on the same executable in OllyDbg, and you want to backup the information you entered)
  * imports comments and labels (ex: you want to integrate an external tool to annotate disassembly)

Supported versions: 1.11, 2.00-2.01

Not all fields in a _UDD_ are understood and supported yet. They will be left unmodified, so _uddtool_ is safe to use.


---

# ChangeLog #

_in development_

---

# Usage example #
you have a great **helloworld.exe** and a very useful tool to give you information on it.

first, create the .udd:

`uddtool.py create helloworld.udd c:\helloworld.exe`

you can double-check the contents of your precious UDD (not required):

`uddtool.py list helloworld.udd`
```
helloworld.udd
Header:Module info file v1.1
Filename:c:\OllyDbg\helloworld.exe
Size:00002149
Timestamp:B5544FDA 01CB0CCF
CRC:41D984EB
Footer:
```
Separately, your tool created the following precious information, as CSV file:
```
RVA,label,comment
0000100a,my label,my comment
```
So now you can import this CSV to the existing UDD (it won't overwrite anything, just add information)

`uddtool.py import helloworld.csv helloworld.udd`

you can check the internal data is updated:

`uddtool.py list helloworld.udd`
```
helloworld.udd
Header:Module info file v1.1
Filename:c:\OllyDbg\helloworld.exe
Size:00002149
Timestamp:B5544FDA 01CB0CCF
CRC:41D984EB
USERLABEL:0000100A my label
U_COMMENT:0000100A my comment
Footer:
```
And now, enjoy a more documented disassembly in OllyDbg:
```
0040100A <my label> | CC            INT3    ;  my comment
```


After some changes in OllyDbg, you can still export the comment and labels:

`uddtool.py export helloworld.udd`
```
RVA,label,comment
0000100a,my new label,my new comment
```

---

# FAQ #
  * **Q**: the generated UDD doesn't load!
  * **A**: CRC might be incorrect in some complex cases. In this case, select _Ignore CRC/TimeStamp_ in the _Options/Security_ dialog

  * **Q**: the comments and labels don't work!
  * **A**: make sure the virtual addresses are _relative_