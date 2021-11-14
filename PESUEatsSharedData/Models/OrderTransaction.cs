using NpgsqlTypes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class OrderTransaction
    {
		[JsonPropertyName("Tid")]
		public int id { get; set; }

		[JsonPropertyName("TfromWid")]
		public int fromWalletid { get; set; }

		[JsonPropertyName("TtoWid")]
		public int toWalletid { get; set; }

		[JsonPropertyName("Tamount")]
		public float amount { get; set; }

		[JsonPropertyName("Tdatetime")]
		public NpgsqlDateTime? datetime { get; set; }

		public OrderTransaction(int id, int fromWalletid, int toWalletid, float amount, NpgsqlDateTime? datetime)
		{
			this.id = id;
			this.fromWalletid = fromWalletid;
			this.toWalletid = toWalletid;
			this.amount = amount;
			this.datetime = datetime;
		}
	}
}
