#!/usr/bin/env cwl-runner

class: CommandLineTool

id: "sanger-wxs-variant-caller"

label: "CGP WXS analysis flow"

cwlVersion: v1.0

doc: |
  ![build_status](https://quay.io/repository/wtsicgp/dockstore-cgpwxs/status)
  A Docker container for the CGP WXS analysis flow. See the [dockstore-cgpwxs](https://github.com/cancerit/dockstore-cgpwxs/blob/master/README.md) website for more information.

  Please read the relevant [changes](https://github.com/cancerit/dockstore-cgpwxs/blob/master/CHANGES.md)
  when upgrading.

  Parameters for a CWL definition are generally described in a json file, but parameters can be provided on the command line.

  To see the parameters descriptions please run: cwltool --tool-help path_to.cwl

  WARNING: The usual setting for 'exclude' is 'NC_007605,hs37d5,GL%' (human GRCh37/NCBI37). Examples
  are configured to run as quickly as possible.

requirements:
  - class: DockerRequirement
    dockerPull: "quay.io/icgc-argo/sanger-wxs-variant-caller:sanger-wxs-variant-caller.3.1.6-1"

hints:
  - class: ResourceRequirement
    coresMin: $(inputs.num_threads)
    ramMin: 32000
    outdirMin: 20000

inputs:
  num_threads:
    type: int?
    default: 18
    inputBinding:
      prefix: -cores
      separate: true

  reference:
    type: File
    doc: "The core reference (fa, fai, dict) as tar.gz"
    inputBinding:
      prefix: -reference
      separate: true

  annot:
    type: File
    doc: "The VAGrENT cache files"
    inputBinding:
      prefix: -annot
      separate: true

  snv_indel:
    type: File
    doc: "Supporting files for SNV and INDEL analysis"
    inputBinding:
      prefix: -snv_indel
      separate: true

  tumour:
    type: File
    secondaryFiles:
    - .bas
    doc: "Tumour alignments file [bam|cram]"
    inputBinding:
      prefix: -tumour
      separate: true

  tumourIdx:
    type: File
    doc: "Tumour alignment file index [bai|csi|crai]"
    inputBinding:
      prefix: -tidx
      separate: true

  normal:
    type: File
    secondaryFiles:
    - .bas
    doc: "Normal alignments file [bam|cram]"
    inputBinding:
      prefix: -normal
      separate: true

  normalIdx:
    type: File
    doc: "Normal alignment file index"
    inputBinding:
      prefix: -nidx
      separate: true

  exclude:
    type: string
    doc: "Contigs to block during indel analysis"
    inputBinding:
      prefix: -exclude
      separate: true
      shellQuote: true

  species:
    type: string?
    doc: "Species to apply if not found in BAM headers"
    default: 'human'
    inputBinding:
      prefix: -species
      separate: true
      shellQuote: true

  assembly:
    type: string?
    doc: "Assembly to apply if not found in BAM headers"
    default: 'GRCh38'
    inputBinding:
      prefix: -assembly
      separate: true
      shellQuote: true

  skipannot:
    type: boolean?
    doc: "Disable Pindel and CaVEMan annotation steps"
    default: false
    inputBinding:
      prefix: -skipannot
      separate: true

outputs:
  run_params:
    type: File
    outputBinding:
      glob: run.params

  result_archive:
    type: File
    outputBinding:
      glob: WXS_*_vs_*.result.tar.gz

  # named like this so can be converted to a secondaryFile set once supported by dockstore cli
  timings:
    type: File
    outputBinding:
      glob: WXS_*_vs_*.timings.tar.gz


baseCommand: ["/opt/wtsi-cgp/bin/ds-cgpwxs.pl"]

$schemas:
  - http://schema.org/docs/schema_org_rdfa.html

$namespaces:
  s: http://schema.org/

s:codeRepository: https://github.com/cancerit/dockstore-cgpwxs
s:license: https://spdx.org/licenses/AGPL-3.0-only

s:author:
  - class: s:Person
    s:identifier: https://orcid.org/0000-0002-5634-1539
    s:email: mailto:cgphelp@sanger.ac.uk
    s:name: Keiran Raine
