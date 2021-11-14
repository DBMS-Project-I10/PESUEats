using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI.Services
{
    public class CustomerServices
    {
        public static List<Customer> GetCustomerList()
        {
            List <Customer> customers = new List<Customer>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM CUSTOMER ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                char[] location = new char[Helper.LOCATION_FIELD];
                char[] phone = new char[Helper.PHONE_FIELD];
                char[] address = new char[Helper.ADDR_FIELD];
                char[] name = new char[Helper.NAME_FIELD];
                char[] email = new char[Helper.EMAIL_FIELD];

                string? locations = null;
                string? emails = null;
                if (!rdr.IsDBNull(2))
                {
                    rdr.GetChars(2, 0, location, 0, Helper.NAME_FIELD);
                    locations = Helper.charToString(location);
                }
                if (!rdr.IsDBNull(5))
                {
                    rdr.GetChars(5, 0, email, 0, Helper.EMAIL_FIELD);
                    emails = Helper.charToString(email);
                }

                rdr.GetChars(3, 0, phone, 0, Helper.PHONE_FIELD);
                rdr.GetChars(5, 0, address, 0, Helper.ADDR_FIELD);
                rdr.GetChars(5, 0, name, 0, Helper.NAME_FIELD);


                customers.Add(new Customer(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    locations,
                    Helper.charToString(phone),
                    Helper.charToString(address),
                    Helper.charToString(name),
                    emails
                    ));
            }

            con.Close();

            return customers;
        }

        public static List<MenuItemInCart> GetMenuItemInCartList()
        {
            List <MenuItemInCart> menuItemInCarts = new List<MenuItemInCart>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM MENU_ITEM_IN_CART ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                menuItemInCarts.Add(new MenuItemInCart(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    rdr.GetInt32(2),
                    rdr.GetInt32(3)
                    ));
            }

            con.Close();

            return menuItemInCarts;
        }
    }
}
