#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
import subprocess
import vcfpy
import glob
import shutil

def run_cmd(cmd):
    stderr, p, success = '', None, True
    try:
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        stderr = p.communicate()[1].decode('utf-8')
    except Exception as e:
        print('Execution failed: %s' % e)
        success = False

    if p and p.returncode != 0:
        print('Execution failed, none zero code returned. \nSTDERR: %s' % repr(stderr), file=sys.stderr)
        success = False

    if not success:
        sys.exit(p.returncode if p.returncode else 1)

    return


def main(args):
    cwd = os.getcwd()

    # create fixed folder and out folder
    fixed_folder = os.path.join(cwd, 'fixed')
    if not os.path.exists(fixed_folder):
        os.mkdir(fixed_folder)
    out_folder = os.path.join(cwd, 'out')
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    # untar the input
    cmd = 'tar -xzf %s -C %s' % (args.input_tar, fixed_folder)
    run_cmd(cmd)

    for f in glob.glob(os.path.join(fixed_folder, '*.vcf.gz')):
        filename = os.path.basename(f)

        # Open input, add FILTER header, and open output file
        reader = vcfpy.Reader.from_path(f)

        fixed_file = os.path.join(cwd, filename)
        with open(fixed_file, "wb") as out:
            writer = vcfpy.Writer.from_stream(out, reader.header, use_bgzf=True)

            # Remove records having REF==ALT
            for record in reader:
                if record.REF == record.ALT[0].value: continue
                writer.write_record(record)
            writer.close()

        # generate index file
        cmd = 'tabix -f -p vcf %s' % fixed_file
        run_cmd(cmd)

        # mv the fixed file into fixed folder
        shutil.move(fixed_file, os.path.join(fixed_folder, filename))
        shutil.move(fixed_file+'.tbi', os.path.join(fixed_folder, filename+'.tbi'))

    # tarball the fixed results
    dest = os.path.join(out_folder, os.path.basename(args.input_tar))
    cmd = "tar -czf %s -C %s ." % (dest, fixed_folder)
    run_cmd(cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-tar", dest="input_tar")
    args = parser.parse_args()

    main(args)