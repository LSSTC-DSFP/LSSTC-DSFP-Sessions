# First things first

This subdirectory of the repo contains files you'll need for these sessions:  


 o  Coping with Streaming Data - ANTARES; G. Narayan [:octocat:](https://github.com/gnarayan)  

 o  Problem -- build mini-ANTARES; G. Narayan [:octocat:](https://github.com/gnarayan) & A. Miller [:octocat:](https://github.com/adamamiller)

---

There are two notebooks in this directory:  
`miniAntares_serial.ipynb`  
and  
`miniAntares_parallel.ipynb`

The parallel version is more complex, realistic, and harder to get running.  
It is what we are going to try to use.  
Because you all are badasses.  

The serial version is a fallback, but also something I'd like you to run later,
on your own. Just to get a comparison of how fast things are without parallel
processing.


1. MAKE SURE YOU ARE IN YOUR PREFERED PYTHON ENVIRONMENT 

`which python`

  All of this relies on you:  
  - installing packages in the right places  
  - initing things consistently within a single python environment  

If we don't get this right, _nothing_ else works.

---

2. Along with this notebook you'll need two tarballs that are sensibly named:  

Get them from [here](https://www.dropbox.com/sh/7vzhzrp3db42uel/AAD1oJqqVN5RBNsfiLDkJoEua?dl=0)  

`training_set_for_LSST_DSFP.tar.gz`  
`test_set_for_LSST_DSFP.tar.gz`  

Untar them.  

`tar -xzf training_set_for_LSST_DSFP.tar.gz`  
`tar -xzf test_set_for_LSST_DSFP.tar.gz`

---

3. Then we need an extra package to support parallel computation with ipython:

`conda install -y ipyparallel`

---

4. Next, we have to start up multiple python "engines" for our distributed computation

`ipcluster start -n 4`

---

5. Now, we want to be able to access and use those engines from within our jupyter notebook

`ipcluster nbextension enable [--user]`

If you are using anaconda (or even better, astroconda), then this should have
all gone smoothly, and you should not need the `--user`

---

6. Finally, we need to run our jupyter notebook using IPython parallel computing cluster we've created

`jupyter notebook`

Switch to the `IPython Clusters` tab.  
If everything went as planned, you should see the cluster you created.  
Hit `Start`

Then, switch back to the `Files` tab, find the notebook file, and start it up as usual.

---

We press on!
- GSN
