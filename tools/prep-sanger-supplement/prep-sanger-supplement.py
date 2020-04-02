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
    untarred_dirs = []
    prefix = 'sanger'  # will be overwritten
    for tar in args.result_tars:
        tar_name = os.path.basename(tar)
        prefix = tar_name.split('.')[0]
        tool_name = tar_name.split('.')[-2]

        # untar and remove unneeded files
        cmd = "mkdir %s && tar -xf %s -C %s && rm -fr %s/*.intermediates.tar.gz %s/*.bw" % \
             (tool_name, tar, tool_name, tool_name, tool_name)

        run_cmd(cmd)
        untarred_dirs.append(tool_name)

    create_tar_cmd = 'tar -czf %s.supplement.tgz %s' % (prefix, ' '.join(untarred_dirs))
    run_cmd(create_tar_cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", dest="result_tars", nargs="+", required=True, help="Sanger result tars")
    args = parser.parse_args()

    main(args)
