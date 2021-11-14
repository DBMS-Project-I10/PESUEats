using Npgsql;
using PESUEatsSharedData.Models;

namespace PESUEatsWebAPI
{
    public class DBMSServices
    {
        public static NpgsqlConnection CreateConnection(string username, string password, string database)
        {
            return new NpgsqlConnection($"Host=localhost;Username={username};Password={password};Database={database}");
        }

        public static string charToString(char[] arr)
        {
            List<char> s = new List<char>();
            foreach (char c in arr)
            {
                if (c != '\u0000') s.Add(c);
            }
            return new String(s.ToArray());
        }

        private static bool setupDB()
        {
            using var con = new NpgsqlConnection($"Host=localhost;Username=postgres;Password=1234;");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;

            cmd.CommandText = @"
                DROP DATABASE IF EXISTS pesu_eats;
                CREATE DATABASE pesu_eats;

                DROP USER IF EXISTS customer ;
                DROP USER IF EXISTS restaurant ;
                DROP USER IF EXISTS wallet ;
                DROP USER IF EXISTS DA ;
                DROP USER IF EXISTS OrderManager ;
            ";
            cmd.ExecuteNonQuery();

            con.Close();

            return true;
        }

        public static bool Setup()
        {
            setupDB();

            using var con = CreateConnection("postgres", "1234", "pesu_eats");
            con.Open();

            using var cmd = new NpgsqlCommand();
            cmd.Connection = con;
            //cmd.CommandText = "SELECT * FROM pg_catalog.pg_user;";

            string strText = File.ReadAllText(@"SQL\setup.sql", System.Text.Encoding.UTF8);
            cmd.CommandText = strText;
            cmd.ExecuteNonQuery();

            con.Close();

            return true;
        }

        private static bool checkIfAdmin(User user)
        {
            if (user.username.ToLower() == "admin" && user.password == "1234") return true;
            else return false;
        }

        public static IResult GetUsers(string? username, User user)
        {
            if (user != null && user.username.ToLower() == "admin" && user.password == "1234")
            {
                List<User> users = new List<User>();

                using var con = CreateConnection("postgres", "1234", "pesu_eats");
                con.Open();

                using var cmd = new NpgsqlCommand();
                cmd.Connection = con;
                cmd.CommandText = "SELECT * FROM app_users;";

                using NpgsqlDataReader rdr = cmd.ExecuteReader();


                while (rdr.Read())
                {
                    char[] uname = new char[15];
                    char[] passwd = new char[30];
                    char[] roles = new char[50];
                    rdr.GetChars(0, 0, uname, 0, 15);
                    rdr.GetChars(1, 0, passwd, 0, 30);
                    rdr.GetChars(2, 0, roles, 0, 50);
                    users.Add(new User(charToString(uname), charToString(passwd), charToString(roles).Split(",")));
                }

                con.Close();

                if (username != null)
                {
                    User? user1 = users.Where(u => u.username == username).FirstOrDefault();
                    if (user1 == null) return Results.NotFound();
                    else return Results.Ok(new List<User>() { user1 });
                }
                else
                {
                    return Results.Ok(users);
                }
                
            }
            else
            {
                return Results.Unauthorized();
            }
        }

        public static IResult Signup(Tuple<User, User> tupleUser)
        {
            User AuthUser = tupleUser.Item1;
            User SignupUser = tupleUser.Item2;
            if (AuthUser != null && checkIfAdmin(AuthUser))
            {
                using var con = CreateConnection("postgres", "1234", "pesu_eats");
                con.Open();

                using var cmd = new NpgsqlCommand();
                cmd.Connection = con;
                cmd.CommandText = @$"INSERT INTO app_users VALUES ('{SignupUser.username}' ,
                            '{SignupUser.password}' , '{string.Join(",", SignupUser.roles)}');";

                int success = cmd.ExecuteNonQuery();

                con.Close();

                if (success != -1)
                {
                    return Results.Ok();
                }
                else
                {
                    return Results.NotFound();
                }
            }
            else
            {
                return Results.Unauthorized();
            }
        }
    }
}
