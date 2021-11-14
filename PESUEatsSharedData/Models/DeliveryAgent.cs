using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class DeliveryAgent
    {
		[JsonPropertyName("DAid")]
		public int id { get; set; }

		[JsonPropertyName("DAhasWid")]
		public int walletid { get; set; }

		[JsonPropertyName("DAName")]
		public string name { get; set; }

		[JsonPropertyName("DALocation")]
		public string? location { get; set; }

		public DeliveryAgent(int id, int walletid, string name, string? location)
		{
			this.id = id;
			this.walletid = walletid;
			this.name = name;
			this.location = location;
		}
	}
}
