# DSFP GitHub Instructions

If you are interested in working on a local copy of the materials associated with the [LSSTC DSFP](https://astrodatascience.org/), you can do that with [git](https://git-scm.com/)/[GitHub](https://github.com/).


### Install local copy of DSFP repo
If you do not have a local copy of the DSFP repo, you will need to "fork" it. 

First navigate to https://github.com/LSSTC-DSFP/LSSTC-DSFP-Sessions

  -  Log in to your GitHub account.
  -  Click on the `Fork` box in the upper right hand corner. (This will take a second and navigate to a new webpage in *your* GitHub account)
  -  Click on the green `Clone or Download` button. Copy the link in the dropdown window. 

Open a terminal on your local machine, change to the directory where you would like for the material to be located, and type the following (note - the webaddress is the one you copied a moment ago)
    
    $ git clone https://github.com/<YOUR_USERNAME>/LSSTC-DSFP-Sessions.git

Connect your local repo to the main DSFP repo:
    
    $ git remote add upstream https://github.com/LSSTC-DSFP/LSSTC-DSFP-Sessions

Test that this has worked:
    
    $ git remote -v
    # Verify new remote
    > origin  https://github.com/<YOUR_USERNAME>/LSSTC-DSFP-Sessions.git (fetch)
    > origin  https://github.com/<YOUR_USERNAME>/LSSTC-DSFP-Sessions.git (push)
    > upstream https://github.com/LSSTC-DSFP/LSSTC-DSFP-Sessions.git (fetch)
    > upstream https://github.com/LSSTC-DSFP/LSSTC-DSFP-Sessions.git (push)`


### Update local copy of DSFP repo

If you have already forked the repo, and set up the main DSFP repo as upstream, then you can update your local copy to remain up-to-date with the following command:

    $ git pull upstream master