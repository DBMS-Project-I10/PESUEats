using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI
{
    public class RestaurantServices
    {
        public static List<Restaurant> GetRestuarantsList()
        {
            List<Restaurant> restaurants = new List<Restaurant>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "company");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM works_on ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();

            char[] ssn = new char[9];

            while (rdr.Read())
            {
                rdr.GetChars(0, 0, ssn, 0, 9);
                restaurants.Add(new Restaurant(Convert.ToInt32(new String(ssn)), rdr.GetInt32(1), rdr.GetFloat(2)));
            }

            con.Close();

            return restaurants;
        }

    }
}
