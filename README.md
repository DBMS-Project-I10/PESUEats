# PESU Eats

## Steps to run

1. Open two terminals in the project root folder
2. Terminal 1: (This starts the PESUEats API)  
   ```
   cd PESUEatsWebAPI  
   dotnet run
   ```
3. Terminal 2: (This starts the Web app that uses the API)  
   ```
   cd PESUEatsBlazorServer  
   dotnet run
   ```

> You can use `dotnet watch` command if you are developing and want live changes

### Other method to run

You CAN use `tye` to run the app by using the command `tye run` in the terminal set to the project root folder.  
Make sure you have `tye` installed from https://www.nuget.org/packages/Microsoft.Tye/0.10.0-alpha.21420.1

