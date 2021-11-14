using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI.Services
{
    public class RestaurantServices
    {
        public static List<Restaurant> GetRestuarantsList()
        {
            List<Restaurant> restaurants = new List<Restaurant>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM restaurant ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();

            while (rdr.Read())
            {
                char[] name = new char[Helper.NAME_FIELD];
                char[] location = new char[Helper.LOCATION_FIELD];
                char[] cuisine = new char[Helper.NAME_FIELD];
                rdr.GetChars(2, 0, name, 0, Helper.NAME_FIELD);
                rdr.GetChars(3, 0, location, 0, Helper.LOCATION_FIELD);
                string? cuisines = null;
                if (!rdr.IsDBNull(5))
                {
                    rdr.GetChars(5, 0, cuisine, 0, Helper.NAME_FIELD);
                    cuisines = Helper.charToString(cuisine);
                }

                restaurants.Add(new Restaurant(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    Helper.charToString(name),
                    Helper.charToString(location),
                    !rdr.IsDBNull(4) ? rdr.GetFloat(4) : null,
                    cuisines
                    ));
            }

            con.Close();

            return restaurants;
        }

        public static List<MenuItem> GetMenuItemList()
        {
            List<MenuItem> menuItems = new List<MenuItem>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM MENU_ITEM ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                char[] name = new char[Helper.NAME_FIELD];
                char[] desc = new char[Helper.DESCRIPTION_FIELD];
                char[] cat = new char[Helper.NAME_FIELD];
                string? descs = null;
                string? cats = null;
                rdr.GetChars(2, 0, name, 0, Helper.NAME_FIELD);
                if (!rdr.IsDBNull(4))
                {
                    rdr.GetChars(4, 0, desc, 0, Helper.DESCRIPTION_FIELD);
                    descs = Helper.charToString(desc);
                }
                if (!rdr.IsDBNull(5))
                {
                    rdr.GetChars(5, 0, cat, 0, Helper.NAME_FIELD);
                    cats = Helper.charToString(cat);
                }

                menuItems.Add(new MenuItem(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    Helper.charToString(name),
                    rdr.GetFloat(3),
                    descs,
                    cats
                    ));
            }

            con.Close();

            return menuItems;
        }
    }
}
