using NpgsqlTypes;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace PESUEatsSharedData.Models
{
    public class FoodOrder
    {
		[JsonPropertyName("Oid")]
		public int id { get; set; }

		[JsonPropertyName("OfromRid")]
		public int fromRid { get; set; }

		[JsonPropertyName("ODAid")]
		public int? DAid { get; set; }

		[JsonPropertyName("OtoCartId")]
		public int OtoCartId { get; set; }

		[JsonPropertyName("OtoCartCustId")]
		public int OtoCartCustId { get; set; }

		[JsonPropertyName("OETA")]
		public NpgsqlDateTime? ETA { get; set; }

		[JsonPropertyName("OStatus")]
		public string status { get; set; }

		[JsonPropertyName("OPlacedDateTime")]
		public NpgsqlDateTime? placedDateTime { get; set; }


		public FoodOrder(int id, int fromRid, int? DAid, int OtoCartId, int OtoCartCustId, NpgsqlDateTime? ETA, string status, NpgsqlDateTime? placedDateTime)
        {
			this.id = id;
			this.fromRid = fromRid;
			this.DAid = DAid;
			this.OtoCartId = OtoCartId;
			this.OtoCartCustId = OtoCartCustId;
			this.ETA = ETA;
			this.status = status;
			this.placedDateTime = placedDateTime;
        }
	}
}
