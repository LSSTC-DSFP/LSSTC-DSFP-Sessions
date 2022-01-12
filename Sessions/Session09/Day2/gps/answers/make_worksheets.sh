#!/bin/bash

# Copy notebooks up w/out "hidden" cells
NOTEBOOKS=*.ipynb
for f in $NOTEBOOKS
do
  echo "Processing $f..."
  jupyter nbconvert --to custom --template=custom_notebook.tpl $f --TagRemovePreprocessor.remove_cell_tags='{"hidden"}'
  base="${f%.*}"
  mv $base.txt ../$f
done

# Move datasets up
if [ -d data ]
then
  mv data ../
fi