cwlVersion: v1.1
class: CommandLineTool
id: generate-bas

requirements:
- class: NetworkAccess
  networkAccess: true
- class: InlineJavascriptRequirement
- class: ShellCommandRequirement
- class: InitialWorkDirRequirement
  listing:
    - $(inputs.input)
- class: DockerRequirement
  dockerPull: 'quay.io/wtsicgp/dockstore-cgpwgs:2.1.0'

hints:
  - class: ResourceRequirement
    coresMin: $(inputs.num_threads)
    ramMin: 2000

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
    secondaryFiles: [.bai?, .crai?]
  num_threads:
    type: int?
    default: 18
    inputBinding:
      prefix: --num_threads
  ref_file:
    type: File?
    inputBinding:
      prefix: -r

outputs:
  bam_and_bas:
    type: File
    secondaryFiles: [ '.bas' ]
    outputBinding:
      glob: [ '*.bam', '*.cram' ]

  bai:
    type: File
    outputBinding:
      glob: [ '*.bai', '*.crai' ]