using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class Wallet
    {
		[JsonPropertyName("Wid")]
		public int id { get; set; }

		[JsonPropertyName("Wamount")]
		public float amount { get; set; }

		public Wallet(int id, float amount)
		{
			this.id = id;
			this.amount = amount;
		}
	}
}
