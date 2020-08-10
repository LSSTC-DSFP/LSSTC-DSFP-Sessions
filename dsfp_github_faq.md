# DSFP GitHub Install Instructions

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

# Working on DSFP Notebooks

The [DSFP repo](https://github.com/LSSTC-DSFP/LSSTC-DSFP-Sessions) is constantly being updated, and this means you will frequently need to [update your fork of the repository](dsfp_github_faq.md#update-local-copy-of-dsfp-repo). A downside of jupyter notebooks is that this frequently leads to merge conflicts.  Inspired by @andreiacarrillo, below I (@adamamiller) provide an outline for two possible solutions to this issue: a simple one, and a more complicated but you will get better at using git/GitHub solution.

## Simple solution to prevent merge conflicts

For example purposes we will assume you now need to work on a notebook called IntroductionToMachineLearning.ipynb. First [pull from upstream](dsfp_github_faq.md#update-local-copy-of-dsfp-repo) to get the latest version of the repository in your master branch. 

Then, copy the new notebook to your own local version, something like:
    $ cp IntroductionToMachineLearning.ipynb IntroductionToMachineLearning_MyWork.ipynb

And try to solve the problems in the notebook in IntroductionToMachineLearning_MyWork.ipynb. Then, if there are later any updates, when you pull from upstream you will never have conflicts.

... Of course, this defeats the purpose of version control, as one of our goals is to avoid multiple versions of the same file with slightly different names proliferating on your computer

## "Better" solution –– fix merge conflicts

Full disclosure - merge conflicts in jupyter notebooks are annoying, because cell numbers don't always line up, etc, and it is possible to effectively "break" a notebook while editing it via a text editor such that it no longer renders correctly on the browser. But (but!) if you want to hone your git/GitHub skills this is something you should learn how to do (annoying as it may be). Here is an outline of how I (@adamamiller) would handle this:

    $ git checkout master
    $ git pull upstream master
    $ git checkout -b my_work
    
Those lines (i) move to your forked master branch, (ii) pull any new/changed notebooks from the primary DSFP repo, and (iii) create a new branch in your forked repo called `my_work`. [Note - the `-b` option is only needed the first time you run this command to create the branch, after that all you need is `git checkout my_work`.]

Now, work on the IntroductionToMachineLearning.ipynb notebook. Complete the problems, try new code, produce plots, etc. When you are done working:

    $ git add IntroductionToMachineLearning.ipynb
    $ git commit -m "ENH: add my solutions to problems 1, 2, 3ab"
    $ git push origin my_work

These lines have (i) staged the notebook for a commit, (ii) commited the changes in your repo, and (iii) pushed your local changes on the `my_work` branch to the cloud.

You are now free to throw your laptop out the window.*

*:warning:Do not throw your laptop out the window.

When there are new notebooks to grab then do the following: 

    $ git checkout master
    $ git pull upstream master
    $ git push origin master
    $ git checkout my_work
    $ git merge master

These lines (i) switch to *your* master branch, (ii) pulled new/changed notebooks from the primary DSFP repo, (iii) pushed *your* master branch to the cloud, (iv) switched to your `my_work` branch, and (v) merged *your* master branch by pulling the new/changed notebooks into the branch where you do your work. 

It is this last step that might result in merge conflicts. The advantage of this workflow is that *your* master branch is always up to date, and, in principle, should never be polluted by accidental or unwanted changes. The downside is you may need to deal with merge conflicts (which are annoying pretty much always, but especially when working on notebooks). However, those conflicts will only happen for changed notebooks, which is a relatively rare occurance (new notebooks will never present merge conflicts).

Another major advantage of this second workflow is that it will give you (a watered down) sense of what it is like to collaboratively develop software.
