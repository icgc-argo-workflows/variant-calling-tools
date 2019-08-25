cwlVersion: v1.1
class: CommandLineTool
id: generate-bas

requirements:
- class: InlineJavascriptRequirement
- class: ShellCommandRequirement
- class: InitialWorkDirRequirement
  listing:
    - $(inputs.input)
- class: DockerRequirement
  dockerPull: 'quay.io/wtsicgp/dockstore-cgpwgs:2.1.0'

baseCommand: [ '/opt/wtsi-cgp/bin/bam_stats' ]

arguments:
  - position: 0
    shellQuote: false
    valueFrom: >-
      '-o' '$(inputs.input.basename).bas'

inputs:
  input:
    type: File
    inputBinding:
      prefix: -i
  num_threads:
    type: int?
    default: 1
    inputBinding:
      prefix: --num_threads

outputs:
  bam_and_bas:
    type: File
    secondaryFiles: [ '.bas' ]
    outputBinding:
      glob: [ '*.bam', '*.cram' ]
