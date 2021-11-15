using PESUEatsWebAPI;
using PESUEatsWebAPI.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.MapGet("/restaurants", RestaurantServices.GetRestuarantsList).WithName("GetRestaurantList");
app.MapGet("/menuitems", RestaurantServices.GetMenuItemList).WithName("GetMenuitemList");
app.MapGet("/menuitemincarts", CustomerServices.GetMenuItemInCartList).WithName("GetMenuitemincartList");
app.MapGet("/carts", OrderManagerServices.GetCartList).WithName("GetCartList");
app.MapGet("/customers", CustomerServices.GetCustomerList).WithName("GetCustomerList");
app.MapGet("/deliveryagents", DAServices.GetDeliveryAgentList).WithName("GetDeliveryagentList");
app.MapGet("/foodorders", OrderManagerServices.GetFoodOrderList).WithName("GetFoodorderList");
app.MapGet("/wallets", WalletServices.GetWalletList).WithName("GetWalletList");
app.MapGet("/ordertransactions", WalletServices.GetOrderTransactionList).WithName("GetOrdertransactionList");

app.MapGet("/menuitemstest", RestaurantServices.GetMenuItemSubsetTestList).WithName("Test");

app.MapPost("/users/{username?}", DBMSServices.GetUsers).WithName("GetUsersList");

app.MapPost("/signup", DBMSServices.Signup).WithName("Signup");
//app.MapPost("/login", DBMSServices.GetUsers).WithName("Login");
app.MapGet("/setup", DBMSServices.Setup).WithName("Setup");

app.Run();
