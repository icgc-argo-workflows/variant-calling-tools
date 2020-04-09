#!/usr/bin/env python3

import os
import sys
import json
import glob
from argparse import ArgumentParser
import subprocess
import re
import tarfile
import csv


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

def get_bas_extra_info(file_path):
    extra_info = {}
    with open(file_path, 'r') as fp:
        Reader = csv.DictReader(fp, delimiter='\t')
        info = []
        for line in Reader:
            info.append(line)
    extra_info.update({'read_groups': info})
    return extra_info


def get_ascat_extra_info(file_path):
    extra_info = {}
    with open(file_path, 'r') as fp:
        for row in fp.readlines():
            cols = row.strip().split()
            extra_info.update({cols[0]: cols[1]})

    return extra_info


def get_contamination_extra_info(file_path):
    extra_info = {}
    with open(file_path, 'r') as fp:
        info = json.load(fp)
        for sample in info:
            extra_info.update({'sample_id': sample})
            extra_info['by_readgroup'] = []
            for rg in info[sample]['by_readgroup']:
                rg_value = {}
                rg_value.update({'read_group_id': rg})
                rg_value.update(info[sample]['by_readgroup'][rg])
                extra_info['by_readgroup'].append(rg_value)

    return extra_info

def get_genotyped_extra_info(file_path):
    with open(file_path, 'r') as fp:
        extra_info = json.load(fp)

    for element in extra_info['tumours']:
        element.update({'sample_id': element['sample']})
        element.pop('sample')

    return extra_info

def main(args):

    for f in args.qc_files:
        file_to_upload = []
        extra_info = {}
        tar_name = None
        if re.match(r'.+?\.bas', f):
            tar_name = os.path.splitext(f)[0] + '.bas_metrics.tgz'
            extra_info = get_bas_extra_info(f)
            file_to_upload.append(f)

        if re.match(r'.+?\.ascat.tgz', f):
            tar_name = os.path.splitext(f)[0] + '_metrics.tgz'
            cmd = 'rm -rf untar && mkdir -p untar && tar xzf %s -C untar' % f
            run_cmd(cmd)
            for member in glob.glob('untar/*.samplestatistics.txt'):
                extra_info = get_ascat_extra_info(member)
                file_to_upload.append(member)
                break

        if re.match(r'.+?\.contamination.tgz', f):
            tar_name = os.path.splitext(f)[0] + '_metrics.tgz'
            cmd = 'rm -rf untar && mkdir -p untar && tar xzf %s -C untar' % f
            run_cmd(cmd)
            for member in glob.glob('untar/*.*'):
                file_to_upload.append(member)
                if member.endswith('result.json'):
                    extra_info = get_contamination_extra_info(member)

        if re.match(r'.+?\.genotyped.tgz', f):
            tar_name = os.path.splitext(f)[0] + '_gender_metrics.tgz'
            cmd = 'rm -rf untar && mkdir -p untar && tar xzf %s -C untar' % f
            run_cmd(cmd)
            for member in glob.glob('untar/*.*'):
                file_to_upload.append(member)
                if member.endswith('result.json'):
                    extra_info = get_genotyped_extra_info(member)

        extra_json = os.path.splitext(tar_name)[0] + '.extra_info.json'
        with open(extra_json, 'w') as j:
            j.write(json.dumps(extra_info, indent=2))

        with tarfile.open(tar_name, 'w') as tar:
            tar.add(extra_json)
            for member in file_to_upload:
                tar.add(member, arcname=os.path.basename(member))

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-r", dest="qc_files", nargs="+", required=True, help="Sanger qc files")
    args = parser.parse_args()

    main(args)
