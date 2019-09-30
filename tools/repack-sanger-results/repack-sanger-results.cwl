cwlVersion: v1.1
class: CommandLineTool
id: repack-sanger-results

requirements:
- class: InlineJavascriptRequirement
- class: ShellCommandRequirement
- class: DockerRequirement
  dockerPull: 'quay.io/icgc-argo/repack-sanger-results:repack-sanger-results.0.1.1'

baseCommand: [ 'repack-sanger-results.py' ]

inputs:
  input:
    type: File
    inputBinding:
      prefix: -i

  library_strategy:
    type: string
    inputBinding:
      prefix: -l

outputs:
  normal_contamination:
    type: ["null", File]
    outputBinding:
      glob: [ '*.normal.contamination.tgz' ]

  tumour_contamination:
    type: ["null", File]
    outputBinding:
      glob: [ '*.tumour.contamination.tgz' ]

  ascat:
    type: ["null", File]
    outputBinding:
      glob: [ '*.ascat.tgz' ]

  brass:
    type: ["null", File]
    outputBinding:
      glob: [ '*.brass.tgz' ]

  caveman:
    type: ["null", File]
    outputBinding:
      glob: [ '*.caveman.tgz' ]

  genotyped:
    type: ["null", File]
    outputBinding:
      glob: [ '*.genotyped.tgz' ]

  pindel:
    type: ["null", File]
    outputBinding:
      glob: [ '*.pindel.tgz' ]
