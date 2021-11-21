# PESU Eats

## Steps to run

1. Open two terminals in the project root folder

2. Terminal 1: (This starts the PESUEats API)  

   ```shell
   cd PESUEatsFlaskAPI  
   sh run.sh
   ```

3. Terminal 2: (This starts the Web app that uses the API)
  
   ```shell
   cd PESUEats.WebFrontend/PESUEatsBlazorServer  
   sh run.sh
   ```

> You can use `dotnet watch` command if you are developing and want live changes

## Cloning

Note that while cloning, you'll need to ensure that the `PESUEats.WebFrontend` submodule is also cloned, using the command `git clone https://github.com/DBMS-Project-I10/PESUEats --recurse-submodules`.

In case you cloned it without the `--recurse-submodules` argument, simple execute `git submodule init` followed by `git submodule update`.
