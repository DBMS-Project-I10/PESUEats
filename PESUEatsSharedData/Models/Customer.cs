using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class Customer
    {
		[JsonPropertyName("CustId")]
		public int id { get; set; }

		[JsonPropertyName("CustHasAWid")]
		public int walletid { get; set; }

		[JsonPropertyName("CustLoc")]
		public string? location { get; set; }

		[JsonPropertyName("CustPhone")]
		public string phoneNumebr { get; set; }

		[JsonPropertyName("CustAddr")]
		public string address { get; set; }

		[JsonPropertyName("CustName")]
		public string name { get; set; }

		[JsonPropertyName("CustEmail")]
		public string? email { get; set; }

		public Customer(int id, int walletid, string? location, string phoneNumebr, string address, string name, string? email)
		{
			this.id = id;
			this.walletid = walletid;
			this.location = location;
			this.phoneNumebr = phoneNumebr;
			this.address = address;
			this.name = name;
			this.email = email;
		}
	}
}
