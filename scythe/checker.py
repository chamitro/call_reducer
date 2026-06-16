import functools
import os
import random
import shutil
import string
import subprocess
import tempfile


class PropertyChecker:

    def __init__(self, file_path: str, test_script: str, *, ext: str,
                 use_tempdir: bool = False, initial_tempdir: bool = False,
                 retry_markers=()):
        self.file_path = file_path
        self.test_script = os.path.abspath(test_script)
        self.ext = ext
        self.use_tempdir = use_tempdir
        self.initial_tempdir = initial_tempdir
        self.retry_markers = tuple(retry_markers)

    def run_test_script(self, file_path: str = None, cwd: str = None) -> int:
        command = ["bash", self.test_script, file_path or self.file_path]
        try:
            while True:
                result = subprocess.run(command, capture_output=True,
                                        text=False, cwd=cwd)
                if not self.retry_markers:
                    return result.returncode
                out = result.stdout.decode("utf-8")
                if any(m not in out for m in self.retry_markers):
                    return result.returncode
        except subprocess.CalledProcessError:
            return -1

    def run_oracle(self, content: str) -> int:
        name = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        fname = f"{name}.{self.ext}"
        workdir = tempfile.mkdtemp(prefix="scythe_") if self.use_tempdir else None
        full = os.path.join(workdir, fname) if workdir is not None else fname
        try:
            with open(full, "w") as f:
                f.write(content)
            return self.run_test_script(fname, cwd=workdir)
        finally:
            if workdir is not None:
                shutil.rmtree(workdir, ignore_errors=True)
            else:
                os.remove(full)

    def check_initial(self) -> int:
        workdir = tempfile.mkdtemp(prefix="scythe_") \
            if self.initial_tempdir else None
        try:
            return self.run_test_script(None, cwd=workdir)
        finally:
            if workdir is not None:
                shutil.rmtree(workdir, ignore_errors=True)


PROPERTY_CHECKERS = {
    "solidity": functools.partial(PropertyChecker, ext="sol"),
    "c": functools.partial(PropertyChecker, ext="c", use_tempdir=True,
                           retry_markers=("exit 3", "exit 4 ")),
    "java": functools.partial(PropertyChecker, ext="java", use_tempdir=True,
                              initial_tempdir=True),
}
