using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI.Services
{
    public class WalletServices
    {
        public static List<Wallet> GetWalletList()
        {
            List <Wallet> wallets = new List<Wallet>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM WALLET ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                wallets.Add(new Wallet(
                    rdr.GetInt32(0),
                    rdr.GetFloat(1)
                    ));
            }

            con.Close();

            return wallets;
        }


        public static List<OrderTransaction> GetOrderTransactionList()
        {
            List <OrderTransaction> orderTransactions = new List<OrderTransaction>();

            using var con = DBMSServices.CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"SELECT * FROM ORDER_TRANSACTION ;";

            using NpgsqlDataReader rdr = cmd.ExecuteReader();


            while (rdr.Read())
            {
                orderTransactions.Add(new OrderTransaction(
                    rdr.GetInt32(0),
                    rdr.GetInt32(1),
                    rdr.GetInt32(2),
                    rdr.GetFloat(3),
                    !rdr.IsDBNull(4) ? rdr.GetTimeStamp(4) : null
                    ));
            }

            con.Close();

            return orderTransactions;
        }
    }
}
