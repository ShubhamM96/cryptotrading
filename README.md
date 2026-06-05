This is the first version of my cryptotrading app.

Added an update


#ignore ds store:
rm .DS_Store
echo ".DS_Store" >> ~/.gitignore_global
git config --global core.excludesfile ~/.gitignore_global
git checkout main

or 
# Discard changes to .DS_Store (don't care about macOS metadata)
git restore .DS_Store

# Now switch branches
git checkout main