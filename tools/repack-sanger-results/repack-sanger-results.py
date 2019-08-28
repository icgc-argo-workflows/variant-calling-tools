#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
import subprocess


def run_cmd(cmd):
    stdout, stderr, p, success = '', '', None, True
    try:
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True)
        p.communicate()
    except Exception as e:
        print('Execution failed: %s' % e)
        success = False

    if p and p.returncode != 0:
        print('Execution failed, none zero code returned. %s' % p.returncode)
        success = False

    if not success:
        sys.exit(p.returncode if p.returncode else 1)

    return

def main(args):

    results = args.input_tar
    results_prefix = os.path.basename(results).split(".")[0]
    sm_tumour = results_prefix.split("_vs_")[0]
    sm_normal = results_prefix.split("_vs_")[1]

    #unpack the result tarball to workdir
    cmd = "tar -xzf %s -C %s" % (results, os.environ["TMPDIR"])
    run_cmd(cmd)

    #repack different types of results
    source = os.path.join(os.environ["TMPDIR"], sm_normal, 'contamination')
    if os.path.exists(source):
        dest = os.path.join(os.environ["HOME"], '.'.join([results_prefix, 'normal', 'contamination', 'tgz']))
        cmd = "tar -czf %s -C %s" %( dest, source )
        run_cmd(cmd)

    source = os.path.join(os.environ["TMPDIR"], sm_tumour, 'contamination')
    if os.path.exists(source):
        dest = os.path.join(os.environ["HOME"], '.'.join([results_prefix, 'tumour', 'contamination', 'tgz']))
        cmd = "tar -czf %s -C %s" %( dest, source )
        run_cmd(cmd)

    for dtype in ['ascat', 'brass', 'caveman', 'genotyped', 'pindel']:
        source = os.path.join(os.environ["TMPDIR"], results_prefix, dtype)
        if not os.path.exists(source): continue
        dest = os.path.join(os.environ["HOME"], '.'.join([results_prefix, dtype, 'tgz']))
        cmd = "tar -czf %s -C %s" % (dest, source)
        run_cmd(cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-tar", dest="input_tar")
    args = parser.parse_args()

    main(args)