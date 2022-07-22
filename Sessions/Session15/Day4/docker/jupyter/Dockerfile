FROM continuumio/miniconda3:4.12.0

RUN conda install -c conda-forge \
    numpy \
    pandas \
    matplotlib \
    psycopg2-binary \
    pymongo \
    jupyterlab

RUN pip install ipython-sql pgspecial SQLAlchemy

CMD ["jupyter-lab","--ip=0.0.0.0","--no-browser","--allow-root"]
