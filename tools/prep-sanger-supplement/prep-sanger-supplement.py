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
    untarred_dirs = []
    prefix = 'sanger'  # will be overwritten
    extra_info = {
        "description": "This TGZ file contains various intermediate data produced by Sanger variant calling pipeline.",
        "contents": []
    }
    for tar in args.result_tars:
        tar_name = os.path.basename(tar)
        prefix = tar_name.split('.')[0]
        tool_name = tar_name.split('.')[-2]

        # untar and remove unneeded files
        cmd = "mkdir %s && tar -xf %s -C %s && rm -fr %s/*.intermediates.tar.gz %s/*.bw" % \
             (tool_name, tar, tool_name, tool_name, tool_name)

        run_cmd(cmd)
        untarred_dirs.append(tool_name)

        description = {
            'caveman': 'Files prodived by CaVEMan tool',
            'pindel': 'Files prodived by Pindel tool',
            'ascat': 'Files prodived by ASCAT tool, bw files removed',
            'brass': 'Files prodived by BRASS tool, bw files and intermediates.tar.gz removed'
        }

        content = {
            "description": description[tool_name],
            "path": tool_name,
            "files": []
        }

        for f in sorted(glob.glob(f"{tool_name}/*")):
            content['files'].append(f.split(os.sep)[1])

        extra_info['contents'].append(content)

    extra_info_file = 'sanger.supplement.extra_info.json'
    with open (extra_info_file, 'w') as w:
        w.write(json.dumps(extra_info, indent=2))

    create_tar_cmd = 'tar -czf %s.supplement.tgz %s %s' % (prefix, ' '.join(untarred_dirs), extra_info_file)
    run_cmd(create_tar_cmd)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", dest="result_tars", nargs="+", required=True, help="Sanger result tars")
    args = parser.parse_args()

    main(args)
