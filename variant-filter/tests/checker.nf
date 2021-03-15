#!/usr/bin/env nextflow

/*
  Copyright (C) 2021,  Ontario Institute for Cancer Research
  
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Affero General Public License for more details.
  
  You should have received a copy of the GNU Affero General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

  Authors:
    Linda Xiang
*/

/*
 This is an auto-generated checker workflow to test the generated main template workflow, it's
 meant to illustrate how testing works. Please update to suit your own needs.
*/

/********************************************************************/
/* this block is auto-generated based on info from pkg.json where   */
/* changes can be made if needed, do NOT modify this block manually */
nextflow.enable.dsl = 2
version = '0.1.0'  // package version

container = [
    'ghcr.io': 'ghcr.io/icgc-argo/variant-calling-tools.variant-filter'
]
default_container_registry = 'ghcr.io'
/********************************************************************/

// universal params
params.container_registry = ""
params.container_version = ""
params.container = ""

// tool specific params go here, add / change as needed
params.input_file = ""
params.regions_file = "NO_FILE_regions"
params.output_type = ""
params.apply_filters = ""
params.include = ""
params.exclude = ""
params.expected_output = ""

include { variantFilter } from '../main'
include { getSecondaryFiles as getSec } from './wfpr_modules/github.com/icgc-argo/data-processing-utility-tools/helper-functions@1.0.0/main.nf'


process file_smart_diff {
  container "${params.container ?: container[params.container_registry ?: default_container_registry]}:${params.container_version ?: version}"

  input:
    path output_file
    path expected_file

  output:
    stdout()

  script:
    """
    # Delete header lines before diff
    diff <( ([[ '${output_file}' == *.gz ]] && gunzip -c ${output_file} || cat ${output_file}) | sed '/^##/d' ) \
         <( ([[ '${expected_file}' == *.gz ]] && gunzip -c ${expected_file} || cat ${expected_file}) | sed '/^##/d' ) \
    && ( echo "Test PASSED" && exit 0 ) || ( echo "Test FAILED, output file mismatch." && exit 1 )
    """
}

workflow checker {
  take:
    input_file
    input_file_idx
    regions_file
    apply_filters
    include
    exclude
    output_type
    expected_output

  main:
    variantFilter(
      input_file,
      input_file_idx,
      regions_file,
      apply_filters,
      include,
      exclude,
      output_type
    )
  
    file_smart_diff(
      variantFilter.out.filtered_vcf,
      expected_output
    )
}


workflow {
  checker(
      file(params.input_file),
      Channel.fromPath(getSec(params.input_file, ['tbi']), checkIfExists: true).collect(),
      file(params.regions_file),
      params.apply_filters,
      params.include,
      params.exclude,
      params.output_type,
      file(params.expected_output)
  )
}
