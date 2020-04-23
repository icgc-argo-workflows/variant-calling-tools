#!/usr/bin/env python3

import os
import sys
import json
import glob
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
    prefix = 'sanger'  # will be overwritten

    description = {
        'caveman': 'Files provided by CaVEMan tool',
        'pindel': 'Files provided by Pindel tool',
        'ascat': 'Files provided by ASCAT tool, bw files removed',
        'brass': 'Files provided by BRASS tool, bw files and intermediates.tar.gz removed',
        'timings': 'Files contain timing information for different processing steps'
    }
    for tar in args.result_tars:
        tar_name = os.path.basename(tar)
        prefix = tar_name.split('.')[0]
        if tar_name.endswith('.timings.tar.gz'):
            tool_name = tar_name.split('.')[-3]
        else:
            tool_name = tar_name.split('.')[-2]

        # untar and remove unneeded files
        if tool_name == 'timings':
            cmd = "tar -xf %s -C %s && rm -fr %s/*.brm.bam %s/*.brm.bam.bai %s/*.intermediates.tar.gz %s/*.bw" % \
                (tar, '.', tool_name, tool_name, tool_name, tool_name)
        else:
            cmd = "mkdir %s && tar -xf %s -C %s && rm -fr %s/*.intermediates.tar.gz %s/*.bw" % \
                (tool_name, tar, tool_name, tool_name, tool_name)

        run_cmd(cmd)

        extra_info = {
            "description": description[tool_name],
            "files": []
        }

        for f in sorted(glob.glob(f"{tool_name}/*")):
            extra_info['files'].append(f.split(os.sep)[1])


        extra_info_file = 'sanger.%s-supplement.extra_info.json' % tool_name
        with open (extra_info_file, 'w') as w:
            w.write(json.dumps(extra_info, indent=2))

        create_tar_cmd = 'tar -czf %s.%s-supplement.tgz %s %s' % (prefix, tool_name, tool_name, extra_info_file)
        run_cmd(create_tar_cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", dest="result_tars", nargs="+", required=True, help="Sanger result tars")
    args = parser.parse_args()

    main(args)
