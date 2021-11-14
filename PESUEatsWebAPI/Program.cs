using PESUEatsWebAPI;

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

app.MapGet("/restaurants", RestaurantServices.GetRestuarantsList).WithName("GetRestuarantsList");
app.MapPost("/users/{username?}", DBMSServices.GetUsers).WithName("GetUsersList");
app.MapPost("/signup", DBMSServices.Signup).WithName("Signup");
//app.MapPost("/login", DBMSServices.GetUsers).WithName("Login");
app.MapGet("/setup", DBMSServices.Setup).WithName("Setup");

app.Run();
