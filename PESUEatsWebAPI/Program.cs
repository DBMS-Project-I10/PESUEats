using Npgsql;
using PESUEatsSharedData.Models;

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

app.MapGet("/ls/restaurants", () =>
{
	List<Restaurant> restaurants = new List<Restaurant>();

	var cs = "Host=localhost;Username=postgres;Password=1234;Database=company";

	using var con = new NpgsqlConnection(cs);

	con.Open();

	using var cmd = new NpgsqlCommand();

	cmd.Connection = con;

	cmd.CommandText = "SELECT * FROM works_on";

	using NpgsqlDataReader rdr = cmd.ExecuteReader();

	char[] ssn = new char[9];

	while (rdr.Read())
	{
		rdr.GetChars(0, 0, ssn, 0, 9);
		restaurants.Add(new Restaurant(Convert.ToInt32(new String(ssn)), rdr.GetInt32(1), rdr.GetFloat(2)));
	}

    return restaurants;
})
.WithName("GetRestuarantsList");

app.Run();
