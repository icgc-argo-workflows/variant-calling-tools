#!/usr/bin/env nextflow

/*
 * Copyright (c) 2020, Ontario Institute for Cancer Research (OICR).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

/*
 * author Linda Xiang <linda.xiang@oicr.on.ca>
 */

nextflow.preview.dsl=2

params.reference = "NO_FILE"
params.seq = ""
params.seq_idx = ""

include { generateBas; getBasSecondaryFiles } from '../generate-bas' params(params)

Channel
  .fromPath(getBasSecondaryFiles(params.reference), checkIfExists: false)
  .set { reference_fai }

// will not run when import as module
workflow {
  main:
    generateBas(
      file(params.seq),
      file(params.seq_idx),
      file(params.reference),
      reference_fai.collect()
    )
}
