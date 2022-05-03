## how tf to clone

bcuz i use submodules :P

    git clone git@github.com:HenryFBP/algorithmic-trading.git --recurse-submodules

### i forgor to add `--recurse-submodules`

shame on you

now run 

    git submodule update --init --recursive
    git pull --recurse-submodules

## setup

    pip install poetry
    poetry install

## adding submodules

    cd myfolder/etc/etc2
    git submodule add --name <name> <url> <path> 