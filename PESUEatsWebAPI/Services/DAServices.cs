using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI.Services
{
    public class DAServices
    {
        public static List<DeliveryAgent> GetDeliveryAgentList()
        {
            List <DeliveryAgent> deliveryAgents = new List<DeliveryAgent>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM DELIVERY_AGENT ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                char[] name = new char[Helper.NAME_FIELD];
                char[] location = new char[Helper.LOCATION_FIELD];
                rdr.GetChars(2, 0, name, 0, Helper.NAME_FIELD);
                string? locations = null;
                if (!rdr.IsDBNull(3))
                {
                    rdr.GetChars(3, 0, location, 0, Helper.LOCATION_FIELD);
                    locations = Helper.charToString(location);
                }

                deliveryAgents.Add(new DeliveryAgent(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    Helper.charToString(name),
                    locations
                    ));
            }

            con.Close();

            return deliveryAgents;
        }
    }
}
