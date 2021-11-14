namespace PESUEatsWebAPI
{
    public class Helper
    {
        public const int NAME_FIELD = 25;
        public const int DESCRIPTION_FIELD = 50;
        public const int STATUS_FIELD = 10;
        public const int LOCATION_FIELD = 25;
        public const int PHONE_FIELD = 15;
        public const int ADDR_FIELD = 60;
        public const int EMAIL_FIELD = 30;


        public static string charToString(char[] arr)
        {
            List<char> s = new List<char>();
            foreach (char c in arr)
            {
                if (c != '\u0000' && c != 0) s.Add(c);
            }
            return new String(s.ToArray());
        }
    }
}
