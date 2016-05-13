import unittest
import os
import fnmatch
import subprocess
import filecmp


# find all files, output names
def find_fastq_files(directory, pattern):
    """Walks the directory structure, appending filenames to an array"""
    filenames = []
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                filenames.append(filename)
    filenames.sort()
    return filenames


# basic call to the shell application we are testing
def sub_process(command):
    return subprocess.check_output(
        command, stderr=subprocess.STDOUT, shell=True)


def file_compare(command, expected, returned):
    # testing expected file output
    subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return filecmp.cmp(expected, returned)


def parse_fastq(filename):
    # output the file to a dictionary
    with open(filename) as f:
        lines = f.readlines()
    read = [item[:-1] for item in lines[1::4]]
    qual = [item[:-1] for item in lines[3::4]]
    return dict(zip(read, qual))


class TestCase(unittest.TestCase):

    def test_find_fastq_files_recursively(self):
        """Should return all fastq files from the sub directories"""
        self.assertEqual(find_fastq_files('fastqFiles', '*.fastq'),
                         ['fastqFiles/flash2_R1.fastq',
                          'fastqFiles/flash2_R2.fastq'])

    # copy this def to make new command tests
    def test_basic_input(self):
        """Should return that basic input works"""
        myR1file = " fastqFiles/flash2_R1.fastq"
        myR2file = " fastqFiles/flash2_R2.fastq"
        additFlags = " "
        myShellCmd = "../flash2"
        myCommand = myShellCmd + myR1file + myR2file + additFlags
        self.assertIn("2500", sub_process(myCommand))

    def test_basic_output(self):
        """Should return that basic output works"""
        myR1file = " fastqFiles/flash2_R1.fastq"
        myR2file = " fastqFiles/flash2_R2.fastq"
        additFlags = " "
        myShellCmd = "../flash2"
        myCommand = myShellCmd + myR1file + myR2file + additFlags
        self.assertIn("Innie pairs:   2180", sub_process(myCommand))

    def test_file_compare(self):
        """Should  return that two files match line for line"""
        myR1file = " fastqFiles/flash2_R1.fastq"
        myR2file = " fastqFiles/flash2_R2.fastq"
        additFlags = " "
        myShellCmd = "../flash2"
        myCommand = myShellCmd + myR1file + myR2file + additFlags
        myExpectedFile = "expected.hist"
        myReturnedFile = "out.hist"
        self.assertTrue(file_compare(
            myCommand, myExpectedFile, myReturnedFile))


if __name__ == '__main__':
    unittest.main()
