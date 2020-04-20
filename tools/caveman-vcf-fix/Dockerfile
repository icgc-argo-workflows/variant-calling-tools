FROM quay.io/icgc-argo/dna-seq-processing-tools:base-docker.0.2.0

# install htslib 1.10.2
RUN cd /tmp \
    && curl -sSL -o htslib-1.10.2.tar.bz2 --retry 10 https://github.com/samtools/htslib/releases/download/1.10.2/htslib-1.10.2.tar.bz2 \
    && bunzip2 -c htslib-1.10.2.tar.bz2 |tar xf - \
    && cd htslib-1.10.2 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install

RUN pip3 install vcfpy

RUN export HTSLIB_LIBRARY_DIR=/usr/local/lib
RUN export HTSLIB_INCLUDE_DIR=/usr/local/include

RUN pip3 install Cython --install-option="--no-cython-compile"
RUN pip3 install pysam

ENV PATH="/tools:${PATH}"

COPY *.py /tools/

CMD ["/bin/bash"]