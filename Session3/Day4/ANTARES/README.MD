## 0) First things first

* MAKE SURE YOU ARE IN YOUR PREFERED PYTHON ENVIRONMENT 

`which python`

  All of this relies on you:  
  - installing packages in the right places  
  - initing things consistently within a single python environment  

If we don't get this right, _nothing_ else works.

---

* Along with this notebook are two tarballs that are sensibly named:  

`training_set_for_LSST_DSFP.tar.gz`  
`test_set_for_LSST_DSFP.tar.gz`  

Untar them.  

`tar -xzf training_set_for_LSST_DSFP.tar.gz`
`tar -xzf test_set_for_LSST_DSFP.tar.gz`

---

* Then we need an extra package to support parallel computation with ipython:

`conda install -y ipyparallel`

---

* Next, we have to start up multiple python "engines" for our distributed computation

`ipcluster start -n 4`

---

* Finally, we want to be able to access and use those engines from within our jupyter notebook

`ipcluster nbextension enable [--user]`

If you are using anaconda (or even better, astroconda), then this should have
all gone smoothly, and you should not need the `--user`

---
