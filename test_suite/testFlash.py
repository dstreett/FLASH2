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
                         ['fastqFiles/extendedFrags.fastq',
                          'fastqFiles/flash2_R1.fastq',
                          'fastqFiles/flash2_R2.fastq'])

    # copy this def to make new command tests
    def test_basic_input(self):
        """Should return that basic input works"""
        myR1file = " fastqFiles/flash2_R1.fastq"
        myR2file = " fastqFiles/flash2_R2.fastq"
        additFlags = " -M 150 -Q 20 -C 70"
        myShellCmd = "../flash2"
        myCommand = myShellCmd + myR1file + myR2file + additFlags
        self.assertIn("73.50%", sub_process(myCommand),
                      ("If this returns as an error then either "
                       "the output has changed or the input "
                       "has changed. This may indicate a change "
                       "in the algorithm since this tests for percentage "
                       "of combined."))

    def test_for_expected_output(self):
        """Should return that basic input works"""
        myR1file = " fastqFiles/flash2_R1.fastq"
        myR2file = " fastqFiles/flash2_R2.fastq"
        additFlags = " -M 150 -Q 20 -C 70"
        myShellCmd = "../flash2"
        myCommand = myShellCmd + myR1file + myR2file + additFlags
        self.assertIn("73.50%", sub_process(myCommand),
                      ("If this returns as an error then either "
                       "the output has changed or the input "
                       "has changed."))

    def test_find_output_files_exist(self):
        """Should return all fastq files, output and input"""
        self.assertEqual(find_fastq_files('.', '*.fastq'),
                         ['./.flash.extendedFrags.fastq',
                          './.flash.notCombined_1.fastq',
                          './.flash.notCombined_2.fastq',
                          './fastqFiles/extendedFrags.fastq',
                          './fastqFiles/flash2_R1.fastq',
                          './fastqFiles/flash2_R2.fastq',
                          './out.extendedFrags.fastq',
                          './out.notCombined_1.fastq',
                          './out.notCombined_2.fastq'])

    def test_item_from_one_exists_in_two(self):
        """Tests if the first entry in the expected output is in the input"""
        data01 = parse_fastq("fastqFiles/extendedFrags.fastq")
        data02 = parse_fastq("out.extendedFrags.fastq")
        self.assertTrue(data01.items()[0][0] in data02,
                        "The first entry was in expected output "
                        "is not found in the testcase")


if __name__ == '__main__':
    unittest.main()
