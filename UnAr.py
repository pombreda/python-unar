import os
import json
import subprocess

class Archive(object):

    def __init__(self,
        filename,
        password=None,
        encoding=None,
        password_encoding=None,
        no_recursion=False
        ):

        self.filename = filename
        self.password = password
        self.encoding = encoding
        self.password_encoding = password_encoding

        self.info = json.loads(subprocess.check_output(["lsar", "-j", filename]))

        self.contents = []

        if "lsarError" in self.info:
            print("Error {} while opening the archive.".format(info["lsarError"]))
            sys.exit()

        for c in self.info["lsarContents"]:
            if c.get("XADIsDirectory", None) == 1:
                d = Directory(self, c)
                self.contents.append(d)
            else:
                f = File(self, c)
                self.contents.append(f)

    def extract(self,
        output_directory=None,
        force_overwrite=False,
        force_rename=False,
        force_skip=False,
        force_directory=False,
        no_directory=False,
        indexes=False,
        no_recursion=False,
        copy_time=False,
        files=None,
        ):

        if isinstance(files, (str,unicode)):
            files = [files,]
        elif isinstance(files, int):
            files = str(files)
            files = [files,]

        s = ["unar", ]
        if output_directory is not None:
            s.append("-output-directory")
            s.append("{}".format(output_directory))
        if force_overwrite:
            s.append("-force-overwrite")
        if force_rename:
            s.append("-force-rename")
        if force_skip:
            s.append("force-skip")
        if force_directory:
            s.append("-force-directory")
        if no_directory:
            s.append("-no-directory")
        if self.password is not None:
            s.append("-password {}".format(self.password))
        if self.encoding is not None:
            s.append("-encoding {}".format(self.encoding))
        if self.password_encoding is not None:
            s.append("-password-encoding {}".format(self.password_encoding))
        if indexes:
            s.append("-indexes")
        if no_recursion:
            s.append("-no-recursion")
        if copy_time:
            s.append("-copy-time")
        s.append(self.filename)
        if files:
            s += files

        output = subprocess.call(s)

class Directory(object):
    def __init__(self, archive, handle):
        self.archive = archive
        self.handle = handle
        self.idx = handle.get("XADIndex", 0)
        self.name = handle.get("XADFileName", "")

    def extract(self, *args, **kwargs):
        self.archive.extract(*args, files=self.idx, indexes=True, **kwargs)

class File(object):
    def __init__(self, a, f):
        self.archive = archive
        self.handle = handle
        self.idx = handle.get("XADIndex", 0)
        self.name = handle.get("XADFileName", "")
        self.size = handle.get("XADFileSize", 0)
        self.compressed_size = handle.get("XADCompressedSize", 0)

    def __enter__(self):
        self.extract(output_directory="/tmp", force_overwrite=True, no_directory=True)
        self.tmp_path = os.path.join("/tmp", self.name)
        return self.tmp_path

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.tmp_path)
        return False

    def extract(self, *args, **kwargs):
        self.archive.extract(*args, files=self.idx, indexes=True, **kwargs)

