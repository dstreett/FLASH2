import unittest
import os
import fnmatch
import sys
import subprocess

# find all files, output names
def findFastqFiles(directory, pattern):
    """Walks the directory structure, appending filenames to an array"""
    filenames = []
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                filenames.append(filename)
    filenames.sort()
    return filenames

# basic call to the application we are testing
def sub_process(command):
    return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)


class TestCase(unittest.TestCase):

    def test_find_fastq_files_recursively(self):
        """Should return all fastq files from the sub directories"""
        self.assertEqual(findFastqFiles('fastqFiles', '*.fastq'),
                         ['fastqFiles/flash2_R1.fastq',
                          'fastqFiles/flash2_R2.fastq'])

    # copy this def to make new command tests
    def test_basic_input(self):
        """Should return that basic input works"""
        myR1file = " fastqFiles/flash2_R1.fastq "
        myR2file = " fastqFiles/flash2_R2.fastq "
        additFlags = ""
        myShellCmd = "../flash2"
        myCommand = myShellCmd+myR1file+myR2file+additFlags
        self.assertIn("2500",sub_process(myCommand))




if __name__ == '__main__':
    unittest.main()
