cwlVersion: v1.1
class: CommandLineTool
id: repack-sanger-results

requirements:
- class: InlineJavascriptRequirement
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/repack-sanger-results:repack-sanger-results.0.1.0'

baseCommand: [ 'repack-sanger-results.py' ]

inputs:
  input:
    type: File
    inputBinding:
      prefix: -i


outputs:
  normal_contamination:
    type: File
    outputBinding:
      glob: [ '*.normal.contamination.tgz' ]

  tumour_contamination:
    type: File
    outputBinding:
      glob: [ '*.tumour.contamination.tgz' ]

  ascat:
    type: File
    outputBinding:
      glob: [ '*.ascat.tgz' ]

  brass:
    type: File
    outputBinding:
      glob: [ '*.brass.tgz' ]

  cavemen:
    type: File
    outputBinding:
      glob: [ '*.cavemen.tgz' ]

  genotyped:
    type: File
    outputBinding:
      glob: [ '*.genotyped.tgz' ]

  pindel:
    type: File
    outputBinding:
      glob: [ '*.pindel.tgz' ]
