#!/usr/bin/env python3

import os
import sys
from argparse import ArgumentParser
import subprocess


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

    results = args.input_tar
    results_prefix = os.path.basename(results).split(".")[0]
    sm_tumour, sm_normal = results_prefix.replace(args.library_strategy+'_', '').split("_vs_")

    #unpack the result tarball to workdir
    cmd = "tar -xzf %s -C %s" % (results, os.environ["TMPDIR"])
    run_cmd(cmd)

    #repack different types of results
    source = os.path.join(os.environ["TMPDIR"], args.library_strategy+'_'+sm_normal, 'contamination')
    if os.path.exists(source):
        dest = os.path.join(os.environ["HOME"], '.'.join([sm_normal, 'normal', 'contamination', 'tgz']))
        cmd = "tar -czf %s -C %s ." %( dest, source )
        run_cmd(cmd)

    source = os.path.join(os.environ["TMPDIR"], args.library_strategy+'_'+sm_tumour, 'contamination')
    if os.path.exists(source):
        dest = os.path.join(os.environ["HOME"], '.'.join([sm_tumour, 'tumour', 'contamination', 'tgz']))
        cmd = "tar -czf %s -C %s ." %( dest, source )
        run_cmd(cmd)

    for dtype in ['ascat', 'brass', 'caveman', 'genotyped', 'pindel']:
        if args.library_strategy == "WGS":
            source = os.path.join(os.environ["TMPDIR"], results_prefix, dtype)
        elif args.library_strategy == "WXS":
            source = os.path.join(os.environ["TMPDIR"], sm_tumour+"_vs_"+sm_normal, dtype)
        else:
            sys.exit("Unknown library_strategy!")
        if not os.path.exists(source): continue
        dest = os.path.join(os.environ["HOME"], '.'.join([results_prefix, dtype, 'tgz']))
        cmd = "tar -czf %s -C %s ." % (dest, source)
        run_cmd(cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input-tar", dest="input_tar")
    parser.add_argument("-l", "--library-strategy", dest="library_strategy", type=str, choices=['WXS', 'WGS'])
    args = parser.parse_args()

    main(args)