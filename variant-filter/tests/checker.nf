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
    Linda Xiang (linda.xiang@oicr.on.ca)
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

include { variantFilter; getSecondaryFiles } from '../main'

workflow checker {
  take:
    input_file
    input_file_idx
    regions_file
    output_type
    apply_filters
    include
    exclude

  main:
    variantFilter(
      input_file,
      input_file_idx,
      regions_file,
      output_type,
      apply_filters,
      include,
      exclude
    )
}


workflow {
  checker(
      file(params.input_file),
      Channel.fromPath(getSecondaryFiles(params.input_file, ['tbi']), checkIfExists: true).collect(),
      file(params.regions_file),
      params.output_type,
      params.apply_filters,
      params.include,
      params.exclude
  )
}
