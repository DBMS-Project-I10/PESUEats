using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI.Services
{
    public class OrderManagerServices
    {

        public static List<FoodOrder> GetFoodOrderList()
        {
            List <FoodOrder> foodOrders = new List<FoodOrder>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM FOOD_ORDER ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                char[] status = new char[Helper.STATUS_FIELD];
                rdr.GetChars(6, 0, status, 0, Helper.STATUS_FIELD);

                foodOrders.Add(new FoodOrder(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    !rdr.IsDBNull(2) ? rdr.GetInt32(2) : null,
                    rdr.GetInt32(3),
                    rdr.GetInt32(4),
                    !rdr.IsDBNull(5) ? rdr.GetTimeStamp(5) : null,
                    Helper.charToString(status),
                    !rdr.IsDBNull(7) ? rdr.GetTimeStamp(7) : null
                    ));
            }

            con.Close();

            return foodOrders;
        }


        public static List<Cart> GetCartList()
        {
            List <Cart> carts = new List<Cart>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM CART ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                char[] status = new char[Helper.STATUS_FIELD];
                rdr.GetChars(2, 0, status, 0, Helper.STATUS_FIELD);

                carts.Add(new Cart(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    Helper.charToString(status),
                    !rdr.IsDBNull(3) ? rdr.GetFloat(3) : null,
                    !rdr.IsDBNull(4) ? rdr.GetFloat(4) : null,
                    !rdr.IsDBNull(5) ? rdr.GetFloat(5) : null
                    ));
            }

            con.Close();

            return carts;
        }
    }
}
